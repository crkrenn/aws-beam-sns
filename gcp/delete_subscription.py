#!/usr/bin/env python3

from publisher import list_topics
from subscriber import (
    list_subscriptions_in_topic, create_subscription, delete_subscription)
import os
import sys
import google.api_core.exceptions

project_id = os.environ.get('DEVSHELL_PROJECT_ID')
topic_id = "crkrenn-test"
subscription_id = "crkrenn-test-sub"

topics = [topic.name.split('/')[-1] for topic in list_topics(project_id)]
if not topic_id in topics:
    print(f"ERROR: topic '{topic_id}' does not exist.")
    sys.exit()

subscriptions = ( [subscription.split('/')[-1] 
    for subscription in list_subscriptions_in_topic(project_id, topic_id)])
print(f"subscriptions: {subscriptions}")
if subscription_id in subscriptions:
    delete_subscription(project_id, subscription_id)
else:
    print(f"ERROR: subscription '{subscription_id}' does not exist.")