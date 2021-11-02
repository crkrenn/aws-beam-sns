#!/usr/bin/env python3

from publisher import list_topics
from subscriber import list_subscriptions_in_topic, create_subscription
import os
import sys

project_id = os.environ.get('DEVSHELL_PROJECT_ID')
topic_id = "crkrenn-test"
subscription_id = "crkrenn-test-sub"

topics = [topic.name.split('/')[-1] for topic in list_topics(project_id)]
if not topic_id in topics:
    print(f"ERROR: topic '{topic_id}' does not exist.")
    sys.exit()

subscriptions = ( [subscription.split('/')[-1] 
    for subscription in list_subscriptions_in_topic(project_id, topic_id)])
if not subscription_id in subscriptions:
    create_subscription(project_id, topic_id, subscription_id)
else:
    print(f"subscription '{subscription_id}' already exists.")