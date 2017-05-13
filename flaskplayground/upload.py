import os

from app import app
from config import basedir
from flask import request
from flask_uploads import UploadSet, configure_uploads, AllExcept, SCRIPTS, EXECUTABLES
from flask_restful import abort, Resource

uploads = UploadSet('uploads', AllExcept(SCRIPTS + EXECUTABLES))

app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(basedir, 'uploads')
configure_uploads(app, uploads)


class Upload(Resource):
    """HTML for this requst should look something like,

    <form method=POST enctype=multipart/form-data action=something>
    ...
    <input type=file name=upload>
    ...
    </form>
    """

    def post(self):
        if 'upload' in request.files:
            filename = uploads.save(request.files['upload'])
            return filename, 201
        else:
            msg = 'No file included in upload request'
            abort(400, message=msg)


