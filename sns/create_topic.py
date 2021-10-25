#!/usr/bin/env python3
from sns_basics import SnsWrapper
import boto3

sns_wrapper = SnsWrapper(boto3.resource('sns'))

topic = 'crkrenn-test'
print([topic for topic in sns_wrapper.list_topics()])
print(sns_wrapper.create_topic("crkrenn-test"))
print([topic for topic in sns_wrapper.list_topics()])
