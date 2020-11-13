import requests
import json
from csv import reader
import io
import os
from google.cloud import proto
from google.oauth2 import service_account # Instantiates a client
my_credentials = service_account.Credentials.from_service_account_file('apikey.json')
client = proto.speech.SpeechClient(credentials=my_credentials)
config = proto.speech.RecognitionConfig(
    encoding=proto.speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=44100,
    language_code="pl-PL",
)
storage_uri = "gs://audio_skyhacks/710458.mp3"
audio = {"uri": storage_uri}
operation = client.long_running_recognize(config=config, audio=audio)
response = operation.result()
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))

