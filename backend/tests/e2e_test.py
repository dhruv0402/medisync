import requests
import threading
import time
from statistics import mean

BASE_URL = "http://127.0.0.1:5000"

TEST_EMAIL = f"p5_{int(time.time())}@test.com"
TEST_PASSWORD = "123"
TOKEN = None

DOCTOR_ID = 1
SLOT_ID = 50


# -------------------------------
# AUTH
# -------------------------------
def ensure_test_user():
    res = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "name": "Test User",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "role": "patient",
        },
    )

    if res.status_code not in [200, 201, 400, 409]:
        raise Exception(f"User creation failed: {res.status_code} {res.text}")


def get_token():
    global TOKEN
    if TOKEN:
        return TOKEN

    res = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
    )

    if res.status_code != 200:
        print("⚠️ Login failed, retrying once...")
        time.sleep(1)

        res = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        )

        if res.status_code != 200:
            raise Exception(f"Login failed: {res.status_code} {res.text}")

    TOKEN = res.json().get("access_token")
    return TOKEN


def get_headers():
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }


# -------------------------------
# RESET SLOT
# -------------------------------
def reset_slot():
    res = requests.post(
        f"{BASE_URL}/api/appointments/cancel_all_for_testing",
        json={"slot_id": SLOT_ID},
    )

    if res.status_code != 200:
        print(
            "⚠️ Slot reset failed (endpoint missing or error):",
            res.status_code,
            res.text,
        )
    else:
        print("🔄 Slot reset successful")


# -------------------------------
# BOOK APPOINTMENT
# -------------------------------
def book_once():
    res = requests.post(
        f"{BASE_URL}/api/appointments/book",
        headers=get_headers(),
        json={"doctor_id": DOCTOR_ID, "slot_id": SLOT_ID},
    )

    try:
        return res.status_code, res.json()
    except Exception:
        return res.status_code, {"error": res.text}


# -------------------------------
# COMPLETE APPOINTMENT
# -------------------------------
def complete_appointment(appointment_id):
    res = requests.put(
        f"{BASE_URL}/api/appointments/complete/{appointment_id}",
        headers=get_headers(),
    )

    print("COMPLETE:", res.status_code, res.json())


# -------------------------------
# GET INVOICES
# -------------------------------
def get_invoices():
    res = requests.get(
        f"{BASE_URL}/api/invoices/my",
        headers=get_headers(),
    )

    if res.status_code != 200:
        print("❌ Failed to fetch invoices:", res.status_code, res.text)
        return []

    data = res.json()
    print("INVOICES:", data)
    return data.get("invoices", [])


# -------------------------------
# PAY INVOICE
# -------------------------------
def pay_invoice(invoice_id):
    res = requests.put(
        f"{BASE_URL}/api/invoices/pay/{invoice_id}",
        headers=get_headers(),
    )

    print("PAY:", res.status_code, res.json())


# -------------------------------
# REFUND INVOICE
# -------------------------------
def refund_invoice(invoice_id):
    res = requests.post(
        f"{BASE_URL}/api/invoices/refund/{invoice_id}",
        headers=get_headers(),
    )

    print("REFUND:", res.status_code, res.json())


# -------------------------------
# CONCURRENCY TEST
# -------------------------------
def test_concurrent_booking():
    print("\n=== CONCURRENT TEST ===")

    reset_slot()
    time.sleep(0.5)

    results = []
    latencies = []

    def worker(i):
        start = time.time()
        res = requests.post(
            f"{BASE_URL}/api/appointments/book",
            headers=get_headers(),
            json={"doctor_id": DOCTOR_ID, "slot_id": SLOT_ID},
        )

        latency = time.time() - start

        latencies.append(latency)
        results.append((i, res.status_code, res.json()))

    threads = []

    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success = sum(1 for r in results if r[1] == 201)

    for r in results:
        print(f"Thread {r[0]} -> {r[1]} -> {r[2]}")

    print("\n=== SUMMARY ===")
    print("Success:", success)
    print("Fail:", len(results) - success)

    print("\n=== LATENCY ===")
    print("Avg:", mean(latencies))
    print("Max:", max(latencies))
    print("Min:", min(latencies))


# -------------------------------
# FULL BILLING FLOW TEST
# -------------------------------
def test_billing_flow():
    print("\n=== BILLING FLOW TEST ===")

    reset_slot()
    time.sleep(0.5)

    status, booking = book_once()
    print("BOOK:", status, booking)

    if status != 201:
        print("Booking failed, skipping billing test")
        return

    appointment_id = booking["appointment"]["appointment_id"]

    # Complete appointment
    complete_appointment(appointment_id)

    # Wait for worker
    print("Waiting for billing worker...")
    time.sleep(3)

    invoices = get_invoices()

    if not invoices:
        print("No invoices found ❌")
        return

    invoice_id = invoices[0]["invoice_id"]

    # Pay
    pay_invoice(invoice_id)

    # Refund
    refund_invoice(invoice_id)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    ensure_test_user()

    test_billing_flow()
    test_concurrent_booking()
