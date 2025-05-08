import sys, os, tempfile

# Make sure the project root and the generated proto folder are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "proto"))
sys.path.insert(0, proto_dir)

import grpc
import gradio as gr
import story2audio_pb2, story2audio_pb2_grpc

# gRPC channel options to allow large payloads
opts = [
    ("grpc.max_send_message_length", 100 * 1024 * 1024),
    ("grpc.max_receive_message_length", 100 * 1024 * 1024),
]

# Available speakers
VOICES = ["Thomas", "Jerry", "Elisabeth", "Talia"]

def generate_audio(story_text, voice, speed, emotion):
    # Build and send the AudioRequest with all four fields
    with grpc.insecure_channel("localhost:50051", options=opts) as chan:
        stub = story2audio_pb2_grpc.Story2AudioStub(chan)
        req = story2audio_pb2.AudioRequest(
            story_text=story_text,
            voice=voice,
            speed=speed,
            emotion=emotion
        )
        resp = stub.Generate(req)

    # Write the returned bytes to a temp WAV file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(resp.audio_data)
    tmp.flush()
    tmp.close()
    return tmp.name

# Gradio UI
demo = gr.Interface(
    fn=generate_audio,
    inputs=[
        gr.Textbox(lines=5, placeholder="Enter your story…", label="Story Text"),
        gr.Dropdown(choices=VOICES, value="Thomas", label="Voice"),
        gr.Slider(minimum=0.5, maximum=2.0, step=0.1, value=1.0, label="Speed"),
        gr.Textbox(
            lines=1,
            placeholder="e.g. 'speaks slowly in a sad tone with emphasis'",
            label="Emotion Descriptor"
        ),
    ],
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="Story2Audio – Parler-TTS Expresso",
    description="Choose a speaker, speed and describe the emotion. Then enter your story text."
)

if __name__ == "__main__":
    demo.launch()