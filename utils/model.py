import logging
import torch


class ModelConfig:
    """Model configuration for the AudioToTextRecorder."""

    # Model sizes for transcription.
    class ModelSize:
        TINY = "tiny"
        TINY_EN = "tiny.en"
        BASE = "base"
        BASE_EN = "base.en"
        SMALL = "small"
        SMALL_EN = "small.en"
        MEDIUM = "medium"
        MEDIUM_EN = "medium.en"
        LARGE_V1 = "large-v1"
        LARGE_V2 = "large-v2"

    def __init__(
        self,
        model=ModelSize.MEDIUM,
        realtime_model_type=ModelSize.BASE_EN,
        on_realtime_transcription_stabilized=None,
        on_recording_start=None,
        on_recording_stop=None,
    ) -> None:

        ## General Parameters

        # Model size or path for transcription.
        self.MODEL = model

        # Language code for transcription. If left empty, the model will try to auto-detect the language.
        self.LANGUAGE = "en"

        # Specifies the type of computation to be used for transcription.
        # More info: https://opennmt.net/CTranslate2/quantization.html
        self.COMPUTE_TYPE = "auto"

        # Device for model to use. Can either be "cuda" or "cpu".
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        # A callable function triggered when recording starts.
        self.ON_RECORDING_START = on_recording_start

        # A callable function triggered when recording ends.
        self.ON_RECORDING_STOP = on_recording_stop

        # Ensures that every sentence detected by the algorithm starts with an uppercase letter.
        self.ENSURE_SENTENCE_STARTING_UPPERCASE = True

        # Ensures that every sentence that doesn't end with punctuation such as "?", "!" ends with a period.
        self.ENSURE_SENTENCE_ENDS_WITH_PERIOD = True

        # Usage of local microphone for transcription. Set to False if you want to provide chunks with feed_audio method.
        self.USE_MICROPHONE = False

        # Provides a spinner animation text with information about the current recorder state.
        self.SPINNER = False

        # Logging level.
        self.LEVEL = logging.WARNING

        # The beam size to use for beam search decoding.
        self.BEAM_SIZE = 5

        # Initial prompt to be fed to the transcription models.
        self.INITIAL_PROMPT = None

        # Tokens to be suppressed from the transcription output.
        self.SUPPRESS_TOKENS = [-1]

        # If set, the system prints additional debug information to the console.
        self.DEBUG_MODE = False

        ## Real-time Transcription Parameters

        # Enables or disables real-time transcription of audio.
        self.ENABLE_REALTIME_TRANSCRIPTION = True

        # If set to True, the main transcription model will be used for both regular and real-time transcription.
        # If False, a separate model specified by realtime_model_type will be used for real-time transcription.
        # Using a single model can save memory and potentially improve performance, but may not be optimized for real-time processing.
        # Using separate models allows for a smaller, faster model for real-time transcription while keeping a more accurate model for final transcription.
        self.USE_MAIN_MODEL_FOR_REALTIME = False

        # Specifies the size or path of the machine learning model to be used for real-time transcription.
        self.REALTIME_MODEL_TYPE = realtime_model_type

        # Specifies the time interval in seconds after a chunk of audio gets transcribed.
        # Lower values will result in more "real-time" (frequent) transcription updates
        # but may increase computational load.
        self.REALTIME_PROCESSING_PAUSE = 0.2

        # A callback function that is triggered whenever there's an update in the real-time transcription
        # and returns a higher quality, stabilized text as its argument.
        self.ON_REALTIME_TRANSCRIPTION_STABILIZED = on_realtime_transcription_stabilized

        # The beam size to use for real-time transcription beam search decoding.
        self.BEAM_SIZE_REALTIME = 3

        ## Voice Activation Parameters

        # Sensitivity for Silero's voice activity detection ranging from 0 (least sensitive) to 1 (most sensitive).
        self.SILERO_SENSITIVITY = 0.1

        # Sensitivity for the WebRTC Voice Activity Detection engine ranging from 0 (least aggressive / most sensitive) to 3 (most aggressive, least sensitive).
        self.WEBRTC_SENSITIVITY = 3

        # Duration in seconds of silence that must follow speech before the recording is considered to be completed.
        self.POST_SPEECH_SILENCE_DURATION = 0.7

        # Specifies the minimum time interval in seconds that should exist between the end of one recording session and the beginning of another to prevent rapid consecutive recordings.
        self.MIN_GAP_BETWEEN_RECORDINGS = 0

        # Specifies the minimum duration in seconds that a recording session should last to ensure meaningful audio capture,
        # preventing excessively short or fragmented recordings.
        self.MIN_LENGTH_OF_RECORDING = 0

        # The time span, in seconds, during which audio is buffered prior to formal recording.
        # This helps counterbalancing the latency inherent in speech activity detection,
        # ensuring no initial audio is missed.
        self.PRE_RECORDING_BUFFER_DURATION = 0.2

        ## Wake Word Parameters

        # Sensitivity level for wake word detection (0 for least sensitive, 1 for most sensitive).
        self.WAKE_WORDS_SENSITIVITY = 0

    def to_dict(self):
        """Convert the configuration to a dictionary."""
        return {
            "model": self.MODEL,
            "language": self.LANGUAGE,
            "compute_type": self.COMPUTE_TYPE,
            "device": self.DEVICE,
            "on_recording_start": self.ON_RECORDING_START,
            "on_recording_stop": self.ON_RECORDING_STOP,
            "ensure_sentence_starting_uppercase": self.ENSURE_SENTENCE_STARTING_UPPERCASE,
            "ensure_sentence_ends_with_period": self.ENSURE_SENTENCE_ENDS_WITH_PERIOD,
            "use_microphone": self.USE_MICROPHONE,
            "spinner": self.SPINNER,
            "level": self.LEVEL,
            "beam_size": self.BEAM_SIZE,
            "initial_prompt": self.INITIAL_PROMPT,
            "suppress_tokens": self.SUPPRESS_TOKENS,
            "debug_mode": self.DEBUG_MODE,
            "enable_realtime_transcription": self.ENABLE_REALTIME_TRANSCRIPTION,
            "use_main_model_for_realtime": self.USE_MAIN_MODEL_FOR_REALTIME,
            "realtime_model_type": self.REALTIME_MODEL_TYPE,
            "realtime_processing_pause": self.REALTIME_PROCESSING_PAUSE,
            "on_realtime_transcription_stabilized": self.ON_REALTIME_TRANSCRIPTION_STABILIZED,
            "beam_size_realtime": self.BEAM_SIZE_REALTIME,
            "silero_sensitivity": self.SILERO_SENSITIVITY,
            "webrtc_sensitivity": self.WEBRTC_SENSITIVITY,
            "post_speech_silence_duration": self.POST_SPEECH_SILENCE_DURATION,
            "min_gap_between_recordings": self.MIN_GAP_BETWEEN_RECORDINGS,
            "min_length_of_recording": self.MIN_LENGTH_OF_RECORDING,
            "pre_recording_buffer_duration": self.PRE_RECORDING_BUFFER_DURATION,
            "wake_words_sensitivity": self.WAKE_WORDS_SENSITIVITY,
        }
