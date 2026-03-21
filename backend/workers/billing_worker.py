import requests
import threading
import time
import uuid
from statistics import mean

BASE_URL = "http://127.0.0.1:5000/api"

# -------------------------------
# HELPERS
# -------------------------------


def unique_user():
    uid = str(uuid.uuid4())[:8]
    return {
        "email": f"patient_{uid}@example.com",
        "password": "123456",
        "name": "Test User",
        "phone": "9999999999",  # added (likely required)
    }


def register_user(user):
    res = requests.post(f"{BASE_URL}/auth/register", json=user)
    if res.status_code not in [200, 201]:
        raise Exception(f"Register failed: {res.status_code} {res.text}")
    return res


def login_user(user):
    res = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": user["email"], "password": user["password"]},
    )
    if res.status_code != 200:
        raise Exception(f"Login failed: {res.status_code} {res.text}")
    return res.json()["token"]


def get_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def get_available_slot():
    res = requests.get(f"{BASE_URL}/slots")
    if res.status_code != 200:
        raise Exception(f"Failed to fetch slots: {res.text}")

    slots = res.json()

    for slot in slots:
        if not slot.get("is_booked", False):
            return slot["id"]

    raise Exception("No available slots")


def book_slot(token, slot_id):
    res = requests.post(
        f"{BASE_URL}/appointments/book",
        headers=get_headers(token),
        json={
            "slot_id": slot_id,
            "reason": "General Checkup",  # added (likely required)
        },
    )
    return res


# -------------------------------
# TESTS
# -------------------------------


def test_full_flow():
    print("\n=== FULL FLOW TEST ===")

    user = unique_user()

    register_user(user)
    token = login_user(user)

    slot_id = get_available_slot()

    res = book_slot(token, slot_id)
    if res.status_code != 201:
        raise Exception(f"Booking failed: {res.status_code} {res.text}")

    data = res.json()
    appointment_id = data["appointment"]["appointment_id"]

    print("✅ Booking success:", appointment_id)

    return appointment_id


def test_double_booking():
    print("\n=== DOUBLE BOOK TEST ===")

    user = unique_user()
    register_user(user)
    token = login_user(user)

    slot_id = get_available_slot()

    res1 = book_slot(token, slot_id)
    res2 = book_slot(token, slot_id)

    print("Attempt 1:", res1.status_code, res1.text)
    print("Attempt 2:", res2.status_code, res2.text)

    assert res1.status_code == 201
    assert res2.status_code in [400, 409]


def test_concurrent_booking():
    print("\n=== CONCURRENT TEST ===")

    user = unique_user()
    register_user(user)
    token = login_user(user)

    slot_id = get_available_slot()

    results = []
    latencies = []

    def worker(i):
        start = time.time()
        res = book_slot(token, slot_id)
        latency = time.time() - start

        latencies.append(latency)
        results.append(res.status_code)

        try:
            print(f"Thread {i} -> {res.status_code} -> {res.json()}")
        except:
            print(f"Thread {i} -> {res.status_code} -> {res.text}")

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success = results.count(201)
    fail = len(results) - success

    print("\n=== SUMMARY ===")
    print("Success:", success)
    print("Fail:", fail)

    print("\n=== LATENCY ===")
    print("Avg:", mean(latencies))
    print("Max:", max(latencies))
    print("Min:", min(latencies))

    assert success == 1, "Race condition detected"


def test_billing_flow():
    print("\n=== BILLING FLOW TEST ===")

    user = unique_user()
    register_user(user)
    token = login_user(user)

    slot_id = get_available_slot()

    res = book_slot(token, slot_id)

    if res.status_code != 201:
        print("Booking failed:", res.text)
        return

    appointment_id = res.json()["appointment"]["appointment_id"]

    print("📌 Appointment created:", appointment_id)

    import redis
    import json

    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    job = json.dumps({"appointment_id": appointment_id})
    r.rpush("billing_queue", job)

    print("📤 Job pushed to queue")

    time.sleep(5)

    res = requests.get(f"{BASE_URL}/billing/invoice/{appointment_id}")

    if res.status_code == 200:
        print("✅ Invoice created:", res.json())
    else:
        print("⚠️ Invoice check failed:", res.status_code, res.text)


# -------------------------------
# RUN ALL
# -------------------------------

if __name__ == "__main__":
    test_full_flow()
    test_double_booking()
    test_concurrent_booking()
    test_billing_flow()
