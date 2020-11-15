from typing import List, Tuple

import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment

from models.labels_matcher import get_similar_label, EXPECTED_LABELS


def divide_chunks(sound, chunk_size):
    for i in range(0, len(sound), chunk_size):
        yield sound[i:i + chunk_size]


def process(file_path: str, chunk_size: int = 60000, apikey=None) -> Tuple[List[Tuple[int, str]], int]:

    sound = AudioSegment.from_mp3(file_path)
    seconds = sound.duration_seconds
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
            print(index)
        else:
            s = r.recognize_google(audio, language="pl-PL")
            results.append((index*5, s))

    return results, seconds


def assign_label(chunks: List[Tuple[int, str]], max_second) -> pd.DataFrame:
    results = pd.DataFrame(data={'second': list(range(1, int(max_second)))})
    results[EXPECTED_LABELS] = 0

    for chunk in chunks:
        labels = get_similar_label(chunk[1])
        results.loc[results['second'] == chunk[0], labels] = 1

    return results


def main():
    for filename in ['/Users/ag283qj/code/Skyhack-3/second-task/storage/Jesteśmy zgubieni.mp3']:
        results = process(filename)
        text = ' '.join([text for _, text in results])
        print(f'File path: {filename}')
        print(f'Predicted content: {text}')


if __name__ == "__main__":
    main()
