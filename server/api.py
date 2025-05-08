# serverapi.py

import base64
import grpc
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import sys, os

# Ensure project root and generated proto folder are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "proto"))
sys.path.insert(0, proto_dir)

# Import generated gRPC modules
import story2audio_pb2
import story2audio_pb2_grpc

app = FastAPI(title="Story2Audio REST -> gRPC gateway")

# Define REST input schema matching the proto
class GenerateRequest(BaseModel):
    story_text: str
    voice: str = "Thomas"
    speed: float = 1.0
    emotion: str = "neutral"

# Define REST output schema
class GenerateResponse(BaseModel):
    audio_base64: str
    status_code: int
    message: str

# Reuse the same gRPC channel and stub
_channel = None
_stub = None

def get_stub():
    global _channel, _stub
    if _stub is None:
        _channel = grpc.insecure_channel(
            "localhost:50051",
            options=[
                ("grpc.max_send_message_length", 100 * 1024 * 1024),
                ("grpc.max_receive_message_length", 100 * 1024 * 1024),
            ]
        )
        _stub = story2audio_pb2_grpc.Story2AudioStub(_channel)
    return _stub

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    stub = get_stub()

    grpc_req = story2audio_pb2.AudioRequest(
        story_text=req.story_text,
        voice=req.voice,
        speed=req.speed,
        emotion=req.emotion,
    )

    try:
        grpc_resp = stub.Generate(grpc_req)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())

    b64_audio = base64.b64encode(grpc_resp.audio_data).decode("ascii")

    return GenerateResponse(
        audio_base64=b64_audio,
        status_code=grpc_resp.status_code,
        message=grpc_resp.message,
    )

if __name__ == "__main__":
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, log_level="info")

