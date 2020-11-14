import json

from models import speech_to_text
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
