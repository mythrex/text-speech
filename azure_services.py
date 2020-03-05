import azure.cognitiveservices.speech as speechsdk
from keys import SPEECH_KEY_1
import os
import requests
import uuid
import json
from keys import TEXT_ANALYTICS_KEY_1

speech_key, service_region = SPEECH_KEY_1, "westus"

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)


def listen(lang='en-IN'):
    speech_config.speech_recognition_language = lang
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return ("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            return ("Error details: {}".format(cancellation_details.error_details))
        return ("Speech Recognition canceled: {}".format(cancellation_details.reason))


def transcribe(filename, lang='en-IN'):
    speech_config.speech_recognition_language = lang
    audio_filename = filename
    audio_input = speechsdk.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return ("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            return ("Error details: {}".format(cancellation_details.error_details))
        return ("Speech Recognition canceled: {}".format(cancellation_details.reason))


def get_sentiment(input_text, input_language='en'):
    subscription_key = TEXT_ANALYTICS_KEY_1
    base_url = 'https://westcentralus.api.cognitive.microsoft.com/text/analytics'
    path = '/v2.0/sentiment'
    constructed_url = base_url + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    input_text = input_text.split(".")
    # You can pass more than one object in body.
    body = {'documents': []}
    for i, text in enumerate(input_text):
        if(len(text)):
            obj = {
                'language': input_language,
                'id': str(i+1),
                'text': text
            }
            body['documents'].append(obj)

    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
