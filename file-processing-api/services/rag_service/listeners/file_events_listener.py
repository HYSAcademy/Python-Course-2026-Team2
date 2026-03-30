import json

from loguru import logger
from redis_client.client import r
from rq import Queue


q = Queue("rag", connection=r)


def start_listener():
    pubsub = r.pubsub()
    pubsub.subscribe("files_uploaded")
    logger.info(f"LISTEN {pubsub.listen()}")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            event = json.loads(message["data"])
            q.enqueue("services.rag_service.services.event_handler.process_file_event",event)
        except Exception as e:
            print(f"Error processing event: {e}")



