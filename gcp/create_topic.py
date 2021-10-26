#!/usr/bin/env python3

from publisher import create_topic, list_topics
import os

project_id = os.environ.get('DEVSHELL_PROJECT_ID')
topic_id = "crkrenn-test"

topics = [topic.name.split('/')[-1] for topic in list_topics(project_id)]
if not topic_id in topics:
    create_topic(project_id, topic_id)
else:
    print(f"Topic {topic_id} has already been created.")
