import json
import numpy as np
from scipy.signal import resample


def decode_and_resample(audio_data, original_sample_rate, target_sample_rate):
    """Decode and resample audio data."""
    # Decode 16-bit PCM data to numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate the number of samples after resampling
    num_original_samples = len(audio_np)
    num_target_samples = int(
        num_original_samples * target_sample_rate / original_sample_rate
    )

    # Resample the audio
    resampled_audio = resample(audio_np, num_target_samples)
    return resampled_audio.astype(np.int16).tobytes()


def process_bytes(message):
    """Process audio bytes."""
    metadata_length = int.from_bytes(message[:4], byteorder="little")
    metadata_json = message[4 : 4 + metadata_length].decode("utf-8")
    metadata = json.loads(metadata_json)
    sample_rate = metadata["sampleRate"]
    chunk = message[4 + metadata_length :]
    resampled_chunk = decode_and_resample(chunk, sample_rate, 16000)
    return resampled_chunk
