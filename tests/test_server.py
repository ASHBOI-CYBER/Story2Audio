import sys, os, tempfile

# Make sure the project root and the generated proto folder are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "proto"))
sys.path.insert(0, proto_dir)

import asyncio
import io
import wave

import pytest
from google.protobuf import empty_pb2

import story2audio_pb2
import story2audio_pb2_grpc
from server.main import Story2AudioServicer


class DummyContext:
    def __init__(self):
        self._code = None
        self._details = None

    def set_code(self, code):
        self._code = code

    def set_details(self, details):
        self._details = details


@pytest.mark.asyncio
async def test_generate_returns_valid_wav():
    servicer = Story2AudioServicer()
    # Use a very short prompt
    req = story2audio_pb2.AudioRequest(story_text="Hello world")
    ctx = DummyContext()

    resp = await servicer.Generate(req, ctx)

    # Should have succeeded
    assert resp.status_code == 200
    assert resp.audio_data, "audio_data should be non-empty"

    # audio_data should be a valid WAV file
    wav_io = io.BytesIO(resp.audio_data)
    with wave.open(wav_io, "rb") as wf:
        # A mono, 16-bit PCM WAV
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() > 0
        frames = wf.readframes(10)
        assert frames, "WAV should contain at least some frames"
