import sys, os, asyncio, grpc
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..")))

import story2audio_pb2, story2audio_pb2_grpc
from tts_engine import TTSEngine

class Story2AudioServicer(story2audio_pb2_grpc.Story2AudioServicer):
    def __init__(self):
        self.engine = TTSEngine()

    async def Generate(self, request, context):
        try:
            audio = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.engine.text_to_audio(
                    request.story_text,
                    voice=request.voice or "Thomas",
                    emotion=request.emotion or "neutral"
                )
            )
            return story2audio_pb2.AudioResponse(
                audio_data=audio,
                status_code=200,
                message="OK",
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return story2audio_pb2.AudioResponse(
                status_code=500, message=str(e)
            )

async def serve():
    server = grpc.aio.server(options=[
        ("grpc.max_send_message_length", 100*1024*1024),
        ("grpc.max_receive_message_length",100*1024*1024),
    ])
    story2audio_pb2_grpc.add_Story2AudioServicer_to_server(
        Story2AudioServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    print("Server listening on 50051…")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())