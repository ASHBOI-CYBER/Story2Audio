# Story2Audio Microservice

**Convert any story text into expressive, multi-style speech via gRPC, REST, and Gradio.**

---

## 📁 Repository Layout

story2audio/
├── proto/ # gRPC definitions
│ └── story2audio.proto
├── server/ # gRPC server, TTS engine & REST gateway
│ ├── main.py # gRPC server entrypoint
│ ├── tts_engine.py # Parler-TTS Expresso wrapper
│ ├── api.py # FastAPI REST → gRPC gateway
│ └── requirements.txt
├── frontend/ # Gradio UI
│ ├── app.py
│ └── requirements.txt
├── tests/ # Unit, integration & performance benchmarks
│ ├── test_server.py
│ ├── test_integration.py
│ └── tests.py # performance runner
├── postman/ # Postman collection
│ └── Story2Audio.postman_collection.json
├── Dockerfile # Build & run gRPC server
├── perf_graphs/ # (optional) generated latency plots
│ └── concurrency_vs_latency.png
└── README.md # ← you are here

---

## 🚀 Quickstart

### 1. Clone & enter

```bash
git clone <your-repo-url>
cd story2audio
2. Docker (gRPC only)
bash
Copy
Edit
docker build -t story2audio .
docker run -p 50051:50051 story2audio
# server listens on :50051
3. Run gRPC + Gradio locally
In one shell, start the gRPC server:

bash
Copy
Edit
cd server
pip install -r requirements.txt
python main.py
In another shell, launch the frontend:

bash
Copy
Edit
cd frontend
pip install -r requirements.txt
python app.py
Open your browser at http://127.0.0.1:7860 to try it.

📡 REST ↔ gRPC Gateway (Postman)
Start the FastAPI gateway:

bash
Copy
Edit
cd server
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
Import postman/Story2Audio.postman_collection.json into Postman.

Send a POST to http://localhost:8000/generate with JSON body:

json
Copy
Edit
{
  "story_text": "Once upon a time…",
  "voice": "Thomas",
  "speed": 1.0,
  "emotion": "happy"
}
The response contains:

audio_base64: Base64-encoded WAV data

status_code, message

🛠️ Development Setup
You can also run everything locally without Docker:

bash
Copy
Edit
# (Optional) create & activate venv
python -m venv venv
source venv/bin/activate    # macOS/Linux
.\venv\Scripts\activate     # Windows

# Install server dependencies & generate gRPC code
pip install -r server/requirements.txt
python -m grpc_tools.protoc -I./proto \
  --python_out=./proto --grpc_python_out=./proto \
  proto/story2audio.proto

# Install frontend dependencies
pip install -r frontend/requirements.txt
📖 Architecture
proto/story2audio.proto
gRPC service and messages: supports story_text, voice, speed, emotion.

server/main.py
Asynchronous gRPC server that routes requests to Story2AudioServicer.

server/tts_engine.py
Wraps the Parler-TTS Mini Expresso model for multi-speaker, multi-emotion synthesis, with sentence-level chunking for long inputs.

server/api.py
FastAPI app exposing a JSON/REST endpoint which forwards to gRPC.

frontend/app.py
Gradio interface, lets users type text, pick voice & emotion, and play back the generated audio.

tests/

test_server.py & test_integration.py: unit and integration tests

tests.py: performance benchmark script (outputs CSV)

postman/
Story2Audio Postman collection for manual API testing.

📈 Performance
Benchmarks on RTX 3060 Ti (8 GB):

Concurrency	Avg Latency (s)	P95 Latency (s)
1	7.5	7.5
5	30.2	31.6
10	63.5	66.1
20	115.0	120.7

(See perf_graphs/concurrency_vs_latency.png for a plotted curve.)

📝 Limitations
VRAM: ~7–8 GB GPU memory during inference; we free cache after each story.

Input length: Supports up to ~1 000 words via paragraph & sentence chunking.

Voices & Emotions:

Voices: Jerry, Thomas, Elisabeth, Talia

Emotions: any descriptor (e.g. “sad”, “happy”, “confused”, “laughing”)

🔗 Model & License
Model: Parler-TTS Mini Expresso (parler-tts/parler-tts-mini-expresso on HuggingFace)

Code License: MIT

Model Weights License: CC-BY-NC

✅ Testing
Unit tests: pytest tests/test_server.py

Integration: pytest tests/test_integration.py

Performance:

bash
Copy
Edit
python tests/tests.py > perf.csv

Happy storytelling!
