from pydub import AudioSegment  # sudo apt-get install ffmpeg
import speech_recognition as sr
import json
import os


def process(filename, chunksize=60000):
    sound = AudioSegment.from_mp3(f'input_audio/{filename}')
    # split

    def divide_chunks(sound, chunksize):
        for i in range(0, len(sound), chunksize):
            yield sound[i:i + chunksize]
    chunks = list(divide_chunks(sound, chunksize))
    r = sr.Recognizer()
    joined_text = ''
    # convert to wav
    for index, chunk in enumerate(chunks):
        chunk.export(f'output_audio/{filename}.wav', format='wav')
        # recognize
        with sr.AudioFile(f'output_audio/{filename}.wav') as source:
            audio = r.record(source)
        try:
            with open("apikey.json", ) as f:
                apikey = json.load(f)
                apikey = json.dumps(apikey)
            s = r.recognize_google_cloud(audio, language="pl-PL", credentials_json=apikey)
        except:
            # Darmowa metoda, można sprawdzić do 60 requestów jakby cos z kluczem do API nie dzialalo
            s = r.recognize_google(audio, language="pl-PL")
        joined_text += f'{s} '
    return joined_text


if __name__ == "__main__":
    for filename in os.listdir('input_audio'):
        text = process(filename)
        print(f'Nazwa pliku: {filename}')
        print(f'Treść: {text}')
