import json
from typing import List, Tuple

import speech_recognition as sr
from pydub import AudioSegment  #


def divide_chunks(sound, chunk_size):
    for i in range(0, len(sound), chunk_size):
        yield sound[i:i + chunk_size]


def process(file_path: str, chunk_size: int = 60000, apikey=None) -> List[Tuple[int, str]]:

    sound = AudioSegment.from_mp3(file_path)
    chunks = list(divide_chunks(sound, chunk_size))

    r = sr.Recognizer()
    results = []
    wav_file_path = file_path.replace('.mp3', '.wav')

    for index, chunk in enumerate(chunks):
        chunk.export(wav_file_path, format='wav')

        with sr.AudioFile(wav_file_path) as source:
            audio = r.record(source)
        if apikey:
            s = r.recognize_google_cloud(audio, language="pl-PL", credentials_json=apikey)
            words_per_second = len(s.split()) / 60
            word_counter = 1
            for word in s.split():
                results.append((int((index * 60) + word_counter / words_per_second), word))
                word_counter += 1
        else:
            s = r.recognize_google(audio, language="pl-PL")
            results.append((index*5, s))

    return results


def main():
    for filename in ['/Users/ag283qj/code/Skyhack-3/second-task/storage/Jesteśmy zgubieni.mp3']:
        results = process(filename)
        text = ' '.join([text for _, text in results])
        print(f'File path: {filename}')
        print(f'Predicted content: {text}')


if __name__ == "__main__":
    main()
