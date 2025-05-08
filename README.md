# 🗣️ Story2Audio

**Convert any story text into expressive, multi-style speech using gRPC, REST, and Gradio UI.**

## 📁 Project Structure

```
story2audio/
├── proto/               # gRPC definitions
├── server/              # gRPC server, TTS engine & REST gateway
├── frontend/            # Gradio UI
├── tests/               # Tests and benchmarks
├── postman/             # Postman collection for REST API
├── perf_graphs/         # Performance graphs (latency, concurrency, etc.)
└── Dockerfile           # Containerized server
```

---
🎥 **[Watch Demo Video](https://youtu.be/aKpjBG2RPDY)**

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/story2audio.git
cd story2audio
```

---

### 2. Run with Docker (gRPC only)

```bash
docker build -t story2audio .
docker run -p 50051:50051 story2audio
```

---

### 3. Run Locally (gRPC + Gradio UI)

**gRPC Server**

```bash
cd server
pip install -r requirements.txt
python main.py
```

**Gradio Frontend**

```bash
cd frontend
pip install -r requirements.txt
python app.py
```

Open your browser at: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

### 4. REST ↔ gRPC via FastAPI

```bash
cd server
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Then send a `POST` request to: `http://localhost:8000/generate`

**Sample JSON:**

```json
{
  "story_text": "Once upon a time…",
  "voice": "Thomas",
  "speed": 1.0,
  "emotion": "happy"
}
```

---

## 🧠 Architecture

- `proto/story2audio.proto`: gRPC message & service definitions
- `server/main.py`: Async gRPC server
- `server/tts_engine.py`: Parler-TTS model wrapper
- `server/api.py`: FastAPI REST → gRPC gateway
- `frontend/app.py`: Gradio UI
- `tests/`: Unit, integration, and performance tests

---

## 📊 Performance

Tested on **RTX 3060 Ti (8 GB)**:

| Concurrency | Avg Latency (s) | P95 Latency (s) |
|-------------|------------------|------------------|
| 1           | 7.5              | 7.5              |
| 5           | 30.2             | 31.6             |
| 10          | 63.5             | 66.1             |
| 20          | 115.0            | 120.7            |

📈 See:  
![Latency Plot](perf_graphs/avg_latency.png)
![Latency Plot](perf_graphs/p95_latency.png)

---


## 🔬 Testing

```bash
pytest tests/test_server.py           # Unit tests
pytest tests/test_integration.py      # Integration tests
python tests/tests.py > perf.csv      # Performance
```

---

## 📌 Features

- Multi-voice & emotion speech synthesis
- REST, gRPC, and Gradio interfaces
- Chunked synthesis for long text
- FastAPI REST gateway
- Docker-compatible
- Postman API collection

---

## 🎤 Voices & Emotions

- **Voices**: Jerry, Thomas, Elisabeth, Talia  
- **Emotions**: e.g. “happy”, “sad”, “angry”, “laughing”, etc.

---

## 📄 License

- **Code**: MIT License  
- **Model Weights**: [CC-BY-NC](https://creativecommons.org/licenses/by-nc/4.0/)  
- **Model**: [Parler-TTS Mini Expresso](https://huggingface.co/parler-tts/parler-tts-mini-expresso)

---

Happy storytelling! 🌟
