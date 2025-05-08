# tests/test_integration.py
# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import pytest
import grpc

# 1) Make sure your project root and the generated proto folder are on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "proto"))

import story2audio_pb2
import story2audio_pb2_grpc
from server.main import Story2AudioServicer  # now importable

@pytest.mark.asyncio
async def test_integration_generate_returns_wav():
    # 2) Spin up the server on a random free port
    server = grpc.aio.server(
        options=[
            ("grpc.max_send_message_length", 100 * 1024 * 1024),
            ("grpc.max_receive_message_length", 100 * 1024 * 1024),
        ]
    )
    servicer = Story2AudioServicer()
    story2audio_pb2_grpc.add_Story2AudioServicer_to_server(servicer, server)
    port = server.add_insecure_port("[::]:0")  # pick any free port
    await server.start()
    # give it a moment
    await asyncio.sleep(0.1)

    # 3) Create a channel & stub
    channel = grpc.aio.insecure_channel(f"localhost:{port}")
    stub = story2audio_pb2_grpc.Story2AudioStub(channel)

    # 4) Call Generate
    req = story2audio_pb2.AudioRequest(
        story_text="Once upon a time...",
        voice="Thomas",
        speed=1.0,
        emotion="neutral",
    )
    resp = await stub.Generate(req)

    # 5) Assertions
    assert resp.status_code == 200
    # WAV files start with the ASCII "RIFF"
    assert resp.audio_data[:4] == b"RIFF"

    # teardown
    await channel.close()
    await server.stop(0)
