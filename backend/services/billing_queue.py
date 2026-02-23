import json
import redis
from datetime import datetime

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

BILLING_QUEUE = "billing_queue"


def enqueue_billing_job(appointment_id):
    job = {
        "appointment_id": appointment_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    redis_client.rpush(BILLING_QUEUE, json.dumps(job))