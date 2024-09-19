from fastapi import WebSocket, WebSocketDisconnect
from RealtimeSTT import AudioToTextRecorder
import threading
import asyncio
import json

from .model import ModelConfig
from .audio import process_bytes


class ClientConnection:
    """Handle a recorder and WebSocket connection for a client."""

    TYPE = "type"
    DATA = "data"

    REALTIME = "realtime"
    FULL_SENTENCE = "sentence"
    RECORDING_STATUS = "status"

    START = "start"
    STOP = "stop"

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.loop = asyncio.get_event_loop()
        self.recorder_ready = threading.Event()
        self.recorder_thread_active = True
        self.thread = threading.Thread(target=self.recorder_thread)
        self.thread.start()
        self.recorder_ready.wait()

    async def handle(self):
        """Handle WebSocket connections."""
        await self.websocket.accept()

        try:
            while True:
                message = await self.websocket.receive_bytes()
                resampled_chunk = process_bytes(message)
                self.recorder.feed_audio(resampled_chunk)

        except WebSocketDisconnect:
            pass
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.close()
            return

    def recorder_thread(self):
        """Thread for handling the recorder for this specific client."""
        try:
            print("Initializing RealtimeSTT...")
            config = ModelConfig(
                on_realtime_transcription_stabilized=self.text_detected,
                on_recording_start=self.on_recording_start,
                on_recording_stop=self.on_recording_stop,
            )
            self.recorder = AudioToTextRecorder(**config.to_dict())
            print("RealtimeSTT initialized")
            self.recorder_ready.set()

            while self.recorder_thread_active:
                full_sentence = self.recorder.text()
                if full_sentence:
                    asyncio.run_coroutine_threadsafe(
                        self.send_full_sentence(full_sentence),
                        self.loop,
                    )
        finally:
            if self.recorder:
                self.recorder.stop()

    async def send_to_client(self, message_type, data):
        """Send a message to the client."""
        if self.websocket and self.websocket.client_state != WebSocketDisconnect:
            await self.websocket.send_text(
                json.dumps({self.TYPE: message_type, self.DATA: data})
            )

    def text_detected(self, text):
        """Callback when text is detected for this specific client."""
        asyncio.run_coroutine_threadsafe(
            self.send_to_client(self.REALTIME, text), self.loop
        )

    async def send_full_sentence(self, full_sentence):
        """Send the full sentence to the client."""
        await self.send_to_client(self.FULL_SENTENCE, full_sentence)

    def on_recording_start(self):
        """Callback when recording starts."""
        asyncio.run_coroutine_threadsafe(
            self.send_to_client(self.RECORDING_STATUS, self.START), self.loop
        )

    def on_recording_stop(self):
        """Callback when recording stops."""
        asyncio.run_coroutine_threadsafe(
            self.send_to_client(self.RECORDING_STATUS, self.STOP), self.loop
        )

    async def close(self):
        """Close the connection with the client."""
        self.recorder_thread_active = False
        self.recorder.stop()
        self.recorder_ready.clear()
