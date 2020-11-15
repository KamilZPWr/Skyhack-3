import json
import os

from google.oauth2 import service_account

from models import speech_to_text, video_to_labels
from service.api import celery
from service.storage_manager import Storage, update_status, JobStatus


@celery.task
def process_speech_to_text(job_id: str):
    mp3_path = Storage.get_input_mp3_path(job_id).replace('../', './')
    results = speech_to_text.process(mp3_path)
    with open(mp3_path.replace('.mp3', '.json'), 'w+') as file:
        json.dump(results, file)
    # TODO: call pdf creation
    update_status(job_id, JobStatus.finished)


@celery.task
def process_video_to_labels(job_id: str):

    import os
    print(os.path.dirname(os.path.realpath(__file__)))

    mp4_path = Storage.get_input_mp4_path(job_id).replace('../', './')
    credentials_path = Storage.get_apikey_path()
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    labels = video_to_labels.process(mp4_path, credentials)
    results_path = os.path.join(Storage.get_job_root(job_id).replace('../', './'), 'results.csv')
    labels.to_csv(results_path, index=False)
    update_status(job_id, JobStatus.finished)
