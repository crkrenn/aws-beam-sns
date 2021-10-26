#!/usr/bin/env python3

from publisher import list_topics
from typing import Callable
import os
import sys

project_id = os.environ.get('DEVSHELL_PROJECT_ID')
topic_id = "crkrenn-test"

topics = [topic.name.split('/')[-1] for topic in list_topics(project_id)]
if not topic_id in topics:
    print(f"ERROR: topic '{topic_id}' does not exist.")
    sys.exit()

def publish_messages_with_error_handler(project_id: str, topic_id: str) -> None:
    # [START pubsub_publish_with_error_handler]
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    from concurrent import futures
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []

    def get_callback(
        publish_future: pubsub_v1.publisher.futures.Future, data: str
    ) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback

    for i in range(10):
        data = None
        # When you publish a message, the client returns a future.
        publish_future = publisher.publish(
            topic_path, 
            "".encode("utf-8"),
            number=str(i),
            publisher="crkrenn"
        )
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")
    # [END pubsub_publish_with_error_handler]

publish_messages_with_error_handler(project_id, topic_id) 
