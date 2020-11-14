import io

import cv2
import pandas as pd
from google.cloud import videointelligence
from google.oauth2 import service_account
from moviepy.video.io.VideoFileClip import VideoFileClip

from models.labels_matcher import EXPECTED_LABELS, get_similar_label


def extract_labels(video_path: str, credentials) -> pd.DataFrame:
    video_client = videointelligence.VideoIntelligenceServiceClient(credentials=credentials)
    features = [videointelligence.enums.Feature.LABEL_DETECTION]

    with io.open(video_path, "rb") as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        features=features, input_content=input_content
    )
    result = operation.result(timeout=90)

    results = pd.DataFrame(columns=['label', 'category', 'start_time', 'end_time'])

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        label = shot_label.entity.description

        category = shot_label.category_entities[0].description if shot_label.category_entities else None

        for shot in shot_label.segments:
            start_time = (
                shot.segment.start_time_offset.seconds
                + shot.segment.start_time_offset.nanos / 1e9
            )
            end_time = (
                shot.segment.end_time_offset.seconds
                + shot.segment.end_time_offset.nanos / 1e9
            )
            results = results.append(
                {
                    'label': label,
                    'category': category,
                    'start_time': start_time,
                    'end_time': end_time,
                },
                ignore_index=True
            )

    return results


def decrease_fps(video_path):
    new_path = video_path.replace('.mp4', '_5fps.mp4')
    clip = VideoFileClip(video_path)
    clip.write_videofile(new_path, fps=5)
    clip.reader.close()
    return new_path


def process(video_path: str, credentials):
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

    ffmpeg_extract_subclip(video_path, 0, 30, targetname=video_path.replace('.mp4', '_cuted.mp4'))
    video_path = video_path.replace('.mp4', '_cuted.mp4')
    video_path = decrease_fps(video_path)

    video = cv2.VideoCapture(video_path)
    video_seconds = int(video.get(cv2.CAP_PROP_FRAME_COUNT)/video.get(cv2.CAP_PROP_FPS))
    extracted_labels = extract_labels(video_path, credentials)

    results = pd.DataFrame(data={'second': list(range(1, video_seconds))})
    results[EXPECTED_LABELS] = 0

    for _, row in extracted_labels.iterrows():
        label = row['label']
        assigned_labels = get_similar_label(label, 0.55) if label else None

        for assigned_label in assigned_labels:
            results.loc[
                (row['start_time'] < results['second']) & (results['second'] <= row['end_time']),
                assigned_label
            ] = 1

    return results


if __name__ == '__main__':
    credentials = service_account.Credentials.from_service_account_file('/Users/ag283qj/code/Skyhack-3/apikey.json')
    k = process('/Users/ag283qj/code/Skyhack-3/20190829 zamek_ogrodzieniec_360_FINALNA_audiodeskrypcja_5fps.mp4', credentials)
    k.to_csv('inny.csv', index=False)
    p = 1
