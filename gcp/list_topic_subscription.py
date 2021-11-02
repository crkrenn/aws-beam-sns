#!/usr/bin/env python3

from publisher import list_topics
from subscriber import list_subscriptions_in_topic
import os
import sys

project_id = os.environ.get('DEVSHELL_PROJECT_ID')
topic_id = "crkrenn-test"
subscription_id = "crkrenn-test-sub"

topics = [topic.name.split('/')[-1] for topic in list_topics(project_id)]
print(f"topics:\n{topics}")
subscriptions = ( [subscription.split('/')[-1] 
    for subscription in list_subscriptions_in_topic(project_id, topic_id)])
print(f"subscriptions:\n{subscriptions}")
