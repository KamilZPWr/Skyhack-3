import io

import pandas as pd
from google.cloud import videointelligence
from google.oauth2 import service_account


def process(video_path: str) -> pd.DataFrame:
    my_credentials = service_account.Credentials.from_service_account_file('apikey.json')
    video_client = videointelligence.VideoIntelligenceServiceClient(credentials=my_credentials)
    features = [videointelligence.enums.Feature.LABEL_DETECTION]

    with io.open(video_path, "rb") as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        features=features, input_content=input_content
    )
    result = operation.result(timeout=90)

    results = pd.DataFrame(columns=['label', 'category', 'start_time', 'end_time', 'confidence'])

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
            confidence = shot.confidence
            results = results.append(
                {
                    'label': label,
                    'category': category,
                    'start_time': start_time,
                    'end_time': end_time,
                    'confidence': confidence
                },
                ignore_index=True
            )

    return results


if __name__ == '__main__':
    process("/Users/ag283qj/code/Skyhack-3/Jesteśmy zgubieni.mp4")
