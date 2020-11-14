import datetime
import os
import uuid

from flask import Blueprint, send_file
from flask_restplus import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage

from service.storage_manager import CREATE_DATETIME, LAST_UPDATE, JOB_STATUS, Storage, \
    load_history, update_history, JobStatus, check_job_exists

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_blueprint,
    version='1.0',
    title='More Powerful Web Service',
    description='The best Web Service in the Word ever.',
)

name_space = api.namespace('', description='More Powerful namespace')


@name_space.route('/jobs/<string:job_id>')
class Jobs(Resource):
    @api.doc(
        responses={200: 'Job found', 404: 'Job not found'},
        description='Create new job'
    )
    def get(self, job_id):
        history = load_history()

        if not check_job_exists(history, job_id):
            return 'Job not found', 404

        return history[job_id]


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
        responses={201: 'File added'},
        description='Add new document'
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
        file.save(os.path.join(Storage.get_input_path(job_id), file.filename))
        update_history(job_id, job)

        # TODO: call celery task to process ai model

        return job_id, 201


@name_space.route('/jobs/download/<string:job_id>')
class Results(Resource):
    @api.doc(
        responses={
            200: 'Job found',
            404: 'Job not found'
        },
        description='Download results'
    )
    def get(self, job_id):
        history = load_history()

        if not check_job_exists(history, job_id):
            return 'Job not found', 404

        results_path = Storage.get_results_path(job_id)
        return send_file(results_path, as_attachment=True)
