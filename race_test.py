import requests
import time
import threading

URL = "http://127.0.0.1:5000/api/appointments/book"

# ⚠️ Leave empty — we will dynamically fetch fresh tokens
TOKENS = []

DATA = {
    "doctor_id": 1,
    "slot_id": 41,  # ⚠️ ensure this is a FREE slot before running
}

results = []
import random

latencies = []

ITERATIONS = 50


def generate_tokens(n):
    tokens = []
    for i in range(n):
        email = f"race_user_{int(time.time())}_{i}@test.com"

        # register
        requests.post(
            "http://127.0.0.1:5000/api/auth/register",
            json={
                "name": f"RaceUser{i}",
                "email": email,
                "password": "123456",
                "role": "patient",
            },
        )

        # login
        res = requests.post(
            "http://127.0.0.1:5000/api/auth/login",
            json={
                "email": email,
                "password": "123456",
            },
        )

        token = res.json().get("access_token")
        if token:
            tokens.append(token)

    return tokens


def book_slot(thread_id):
    try:
        # wait until all threads are ready (true race)
        if start_barrier:
            start_barrier.wait()

        headers = {
            "Authorization": f"Bearer {TOKENS[thread_id]}",
            "Content-Type": "application/json",
        }

        start_time = time.time()
        response = requests.post(URL, json=DATA, headers=headers)
        latency = time.time() - start_time
        latencies.append(latency)

        results.append((thread_id, response.status_code, response.json()))
    except Exception as e:
        results.append((thread_id, "ERROR", str(e)))


NUM_THREADS = 10  # keep in sync with Barrier parties
start_barrier = None
TOKENS = generate_tokens(NUM_THREADS)

for iteration in range(ITERATIONS):
    start_barrier = threading.Barrier(parties=NUM_THREADS)
    print(f"\n===== ITERATION {iteration + 1} =====")

    threads = []
    results.clear()
    latencies.clear()

    for i in range(NUM_THREADS):
        t = threading.Thread(target=book_slot, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n=== RESULTS ===\n")

    success = 0
    fail = 0

    for r in sorted(results, key=lambda x: x[0]):
        print(f"Thread {r[0]} -> {r[1]} -> {r[2]}")
        if r[1] == 201:
            success += 1
        else:
            fail += 1

    print("\n=== SUMMARY ===")
    print(f"Success: {success}")
    print(f"Fail: {fail}")

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0

    print("\n=== LATENCY METRICS ===")
    print(f"Avg latency: {avg_latency:.4f}s")
    print(f"Max latency: {max_latency:.4f}s")
    print(f"Min latency: {min_latency:.4f}s")
