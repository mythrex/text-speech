from google.cloud import speech_v1
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.protobuf.json_format import MessageToJson
import io
import json


def sample_recognize(local_file_path, lang="en-US", model="phone_call"):
    """
    Transcribe a short audio file using a specified transcription model

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
      model The transcription model to use, e.g. video, phone_call, default
      For a list of available transcription models, see:
      https://cloud.google.com/speech-to-text/docs/transcription-model#transcription_models
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/hello.wav'
    # model = 'phone_call'

    # The language of the supplied audio
    config = {"model": model,
              "language_code": lang,
              "use_enhanced": True,
              "enable_automatic_punctuation": True,
              "audio_channel_count": 2,
              #               "enable_separate_recognition_per_channel": True,
              "diarization_config": {
                  "enable_speaker_diarization": True,
                  "min_speaker_count": 2,
                  "speaker_tag": 2
              }
              }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    serialized = MessageToJson(response)
    return json.loads(serialized)["results"][-1]["alternatives"]


def analyze_sentiment(text):
    # Instantiates a client
    client = language.LanguageServiceClient()
    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    # Detects the sentiment of the text
    sent = client.analyze_sentiment(document=document)
    serialized = MessageToJson(sent)
    return json.loads(serialized)
