from RealtimeSTT import AudioToTextRecorder

from .model import ModelConfig


def init():
    """Initialize the RealtimeSTT weights."""
    config = ModelConfig()
    recorder = AudioToTextRecorder(**config.to_dict())
    recorder.stop()
    del recorder
