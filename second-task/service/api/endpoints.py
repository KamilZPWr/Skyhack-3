import datetime
import os
import uuid

import pandas as pd
from flask import Blueprint
from flask_restplus import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage

from service.celery_tasks.celery_task import process_speech_to_text, process_video_to_labels
from service.storage_manager import CREATE_DATETIME, LAST_UPDATE, JOB_STATUS, Storage, \
    update_history, JobStatus, update_status

MP4 = 'mp4'

MP3 = 'mp3'

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_blueprint,
    version='1.0',
    title='More Powerful Web Service',
    description='The best Web Service in the Word ever.',
)

name_space = api.namespace('', description='More Powerful namespace')
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    required=True
)


@name_space.route('/jobs/file/process')
@api.expect(upload_parser)
class Files(Resource):
    @api.doc(
        responses={201: 'Process started'},
        description=('Upload mp3 or mp4 file to start labels detection, '
                     'as result you will receive link to the dashboard which will present results')
    )
    def post(self):
        job_id = str(uuid.uuid1())
        now = str(datetime.datetime.now())
        job = {
            CREATE_DATETIME: now,
            LAST_UPDATE: now,
            JOB_STATUS: JobStatus.created.name,
        }

        for directory in Storage.get_job_paths(job_id):
            if not os.path.exists(directory):
                os.makedirs(directory)

        args = upload_parser.parse_args()
        file = args['file']
        file_type = MP3 if '.mp3' in file.filename else MP4
        file_name = f'input.{file_type}'
        file.save(os.path.join(Storage.get_input_path(job_id), file_name))
        update_history(job_id, job)

        if file_type == MP3:
            process_speech_to_text.delay(job_id)
        else:
            process_video_to_labels.delay(job_id)
        update_status(job_id, JobStatus.in_progress)

        results_tracker = pd.read_csv(Storage.get_tracker_path())
        results_tracker = results_tracker.append(
            {
                'run_id': job_id,
                'run_datetime': now,
                'results_path': Storage.get_results_path(job_id),
                'run_type': 'audio' if file_type == MP3 else 'video'
            },
            ignore_index=True
        )
        results_tracker.to_csv(Storage.get_tracker_path(), index=False)

        return job_id, 201
