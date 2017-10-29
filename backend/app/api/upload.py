import os

from app import app
from config import basedir
from flask import request
from flask_uploads import UploadSet, configure_uploads, AllExcept, SCRIPTS, EXECUTABLES, IMAGES
from flask_restful import abort, Resource

uploads = UploadSet('uploads', AllExcept(SCRIPTS + EXECUTABLES))
photos_sub = 'photos'
photos = UploadSet(photos_sub, IMAGES)

dest = os.path.join(basedir, 'app', 'static')

app.config['UPLOADS_DEFAULT_DEST'] = dest
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
            path = os.path.join(dest, photos_sub, request.files['photos'].filename)
            if os.path.exists(path):
                os.remove(path)
            filename = photos.save(request.files['photos'])
            return filename, 201
        else:
            msg = 'No file included in upload request'
            abort(400, message=msg)
