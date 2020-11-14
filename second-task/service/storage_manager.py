import json
import os
from enum import Enum

from filelock import FileLock

JOB_STATUS = 'job_status'
LAST_UPDATE = 'last_update'
CREATE_DATETIME = 'create_datetime'
LOCK_TIMEOUT = os.environ.get('JOBS_FILE_LOCK_TIMEOUT')


class JobStatus(Enum):
    created = 0
    in_progress = 1
    finished = 2


class Storage:
    @staticmethod
    def get_jobs_path():
        return os.path.join(os.environ.get('STORAGE_PATH'), 'jobs.json')

    @staticmethod
    def get_job_root(job_id):
        return os.path.join(os.environ.get('STORAGE_PATH'), f'data/{job_id}')

    @staticmethod
    def get_results_path(job_id):
        return os.path.join('..', Storage.get_job_root(job_id), 'results.pdf')

    @staticmethod
    def get_input_path(job_id):
        return os.path.join(Storage.get_job_root(job_id), 'input')

    @staticmethod
    def get_job_paths(job_id):
        return \
            Storage.get_job_root(job_id), \
            Storage.get_input_path(job_id)


def load_history(timeout=LOCK_TIMEOUT):
    jobs_path = Storage.get_jobs_path()
    lock = FileLock(f'{jobs_path}.lock')

    try:
        with lock.acquire(timeout=timeout):
            with open(Storage.get_jobs_path(), 'r') as file:
                return json.load(file)
    finally:
        lock.release()


def check_job_exists(history, job_id):
    return job_id in history


def update_history(job_id, job, timeout=LOCK_TIMEOUT):
    jobs_path = Storage.get_jobs_path()
    history = load_history()
    lock = FileLock(f'{jobs_path}.lock')
    try:
        with lock.acquire(timeout=timeout):
            with open(Storage.get_jobs_path(), 'w') as file:
                history[job_id] = job
                json.dump(history, file)
    finally:
        lock.release()
