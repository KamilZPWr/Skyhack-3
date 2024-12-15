from google.oauth2 import service_account

from models import speech_to_text, video_to_labels
from models.speech_to_text import assign_label
from models.translator import translate_list_of_chunks
from service.api import celery
from service.storage_manager import Storage, update_status, JobStatus


@celery.task
def process_speech_to_text(job_id: str):
    mp3_path = Storage.get_input_mp3_path(job_id).replace('../', './')
    labels, seconds = speech_to_text.process(mp3_path)
    translated_labels = translate_list_of_chunks(labels, Storage.get_apikey_path())
    results = assign_label(translated_labels, seconds)
    results_path = Storage.get_results_path(job_id)
    print(results_path)
    print(results.head())
    results.to_csv(results_path, index=False)
    update_status(job_id, JobStatus.finished)


@celery.task
def process_video_to_labels(job_id: str):
    mp4_path = Storage.get_input_mp4_path(job_id).replace('../', './')
    credentials_path = Storage.get_apikey_path()
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    labels = video_to_labels.process(mp4_path, credentials)
    results_path = Storage.get_results_path(job_id)
    print(labels.head())
    labels.to_csv(results_path, index=False)
    update_status(job_id, JobStatus.finished)
