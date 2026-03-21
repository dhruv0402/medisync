import json
import redis
from datetime import datetime
from time import sleep

# Redis client with better reliability settings
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)

BILLING_QUEUE = "billing_queue"


def enqueue_billing_job(appointment_id):
    """
    Push a billing job into Redis queue.

    Improvements:
    - Strong validation
    - Retry with exponential backoff
    - Connection health check (ping)
    - Structured logging
    """

    if not isinstance(appointment_id, int) or appointment_id <= 0:
        raise ValueError("Invalid appointment_id")

    job = {
        "appointment_id": appointment_id,
        "timestamp": datetime.utcnow().isoformat(),
    }

    max_retries = 3
    base_delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            # Ensure Redis is reachable
            redis_client.ping()

            redis_client.rpush(BILLING_QUEUE, json.dumps(job))

            print(f"📥 Billing job queued | appointment_id={appointment_id}")
            return

        except redis.exceptions.RedisError as e:
            delay = base_delay * (2**attempt)
            print(
                f"❌ Redis push failed (attempt {attempt + 1}/{max_retries}) | "
                f"error={str(e)} | retrying in {delay}s"
            )
            sleep(delay)

    # If all retries fail
    raise Exception(
        f"Failed to enqueue billing job after {max_retries} attempts | appointment_id={appointment_id}"
    )
