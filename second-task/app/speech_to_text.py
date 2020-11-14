from pydub import AudioSegment # sudo apt-get install ffmpeg
import speech_recognition as sr
import json

from pathlib import Path
#from pydub.silence import split_on_silence
#import io
#from pocketsphinx import AudioFile, Pocketsphinx

# Opening JSON file
with open("apikey.json", ) as f:
    apikey = json.load(f)
    apikey = json.dumps(apikey)

def process(filepath, chunksize=60000):
    #0: load mp3
    sound = AudioSegment.from_mp3(filepath)

    #1: split file into 60s chunks
    def divide_chunks(sound, chunksize):
        # looping till length l
        for i in range(0, len(sound), chunksize):
            yield sound[i:i + chunksize]
    chunks = list(divide_chunks(sound, chunksize))
    print(f"{len(chunks)} chunks of {chunksize/1000}s each")

    r = sr.Recognizer()
    #2: per chunk, save to wav, then read and run through recognize_google()
    string_index = {}
    for index,chunk in enumerate(chunks):
        #TODO io.BytesIO()
        chunk.export(f'output_audio/{filepath}.wav', format='wav')
        with sr.AudioFile(f'output_audio/{filepath}.wav') as source:
            audio = r.record(source)
        # Darmowa metoda
        # s = r.recognize_google(audio, language="pl-PL")

        s = r.recognize_google_cloud(audio, language="pl-PL", credentials_json=apikey)
        print(s)
        string_index[index] = s
        break
    return string_index

text = process('710458.mp3')