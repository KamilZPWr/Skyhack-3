import json

import speech_recognition as sr
from pydub import AudioSegment  # sudo apt-get install ffmpeg


def process(filename, chunksize=5000):
    sound = AudioSegment.from_mp3(filename)
    # split

    def divide_chunks(sound, chunksize):
        for i in range(0, len(sound), chunksize):
            yield sound[i:i + chunksize]

    chunks = list(divide_chunks(sound, chunksize))
    r = sr.Recognizer()
    results = []
    # convert to wav
    for index, chunk in enumerate(chunks):
        chunk.export(f'{filename}.wav', format='wav')
        # recognize
        with sr.AudioFile(f'{filename}.wav') as source:
            audio = r.record(source)
        try:
            with open("apikey.json", ) as f:
                apikey = json.load(f)
                apikey = json.dumps(apikey)
            s = r.recognize_google_cloud(audio, language="pl-PL", credentials_json=apikey)
            results.append((index*5, s))
        except:
            # Darmowa metoda, można sprawdzić do 60 requestów jakby cos z kluczem do API nie dzialalo
            s = r.recognize_google(audio, language="pl-PL")
            results.append((index*5, s))

    return results


if __name__ == "__main__":
    for filename in ['/Users/ag283qj/code/Skyhack-3/second-task/storage/Jesteśmy zgubieni.mp3']:
        results = process(filename)
        text = ' '.join([text for _, text in results])
        print(f'Nazwa pliku: {filename}')
        print(f'Treść: {text}')
