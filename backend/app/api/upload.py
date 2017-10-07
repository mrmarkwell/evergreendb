import os

from app import app
from config import basedir
from flask import request
from flask_uploads import UploadSet, configure_uploads, AllExcept, SCRIPTS, EXECUTABLES, IMAGES
from flask_restful import abort, Resource

uploads = UploadSet('uploads', AllExcept(SCRIPTS + EXECUTABLES))
photos = UploadSet('photos', IMAGES)


app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(basedir, 'app', 'static')
configure_uploads(app, photos)


class Upload(Resource):
    """HTML for this requst should look something like,

    <form method=POST enctype=multipart/form-data action=something>
    ...
    <input type=file name=upload>
    ...
    </form>
    """

    def post(self):
        if 'photos' in request.files:
            filename = photos.save(request.files['photos'])
            return filename, 201
        else:
            msg = 'No file included in upload request'
            abort(400, message=msg)


