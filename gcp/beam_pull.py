#!/usr/bin/env python3

import argparse
from datetime import datetime
import logging
import random

from apache_beam import DoFn, GroupByKey, io, ParDo, Pipeline, PTransform, WindowInto, WithKeys
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows
from apache_beam.io.textio import ReadAllFromText, WriteToText

def run(input_topic, output_path, window_size=1.0, num_shards=5, pipeline_args=None):
    # Set `save_main_session` to True so DoFns can access globally imported modules.
    pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True
    )

    with Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            # Because `timestamp_attribute` is unspecified in `ReadFromPubSub`, Beam
            # binds the publish time returned by the Pub/Sub server for each message
            # to the element's timestamp parameter, accessible via `DoFn.TimestampParam`.
            # https://beam.apache.org/releases/pydoc/current/apache_beam.io.gcp.pubsub.html#apache_beam.io.gcp.pubsub.ReadFromPubSub
            | "Read from Pub/Sub" >> io.ReadFromPubSub(topic=input_topic)
            | "Window into" >> WindowInto(
                FixedWindows(10),
                trigger=Repeatedly(
                    AfterAny(AfterCount(10), AfterProcessingTime(10))),
                accumulation_mode=AccumulationMode.DISCARDING)
f            # | "Write to GCS" >> ParDo(WriteToGCS(output_path))
            | 'write' >> WriteToText(
                'stream_out.txt')
        )