import os

from app import app
from config import basedir
from flask import request
from flask_uploads import UploadSet, configure_uploads, AllExcept, SCRIPTS, EXECUTABLES, IMAGES
from flask_restful import abort, Resource
from PIL import Image
from resizeimage import resizeimage

uploads = UploadSet('uploads', AllExcept(SCRIPTS + EXECUTABLES))
interactions_upload_set = UploadSet('interactions', AllExcept(SCRIPTS + EXECUTABLES))
photos_sub = 'photos'
photos = UploadSet(photos_sub, IMAGES)

interactions_sub = 'interactions'

dest = os.path.join(basedir, 'app', 'static')

app.config['UPLOADS_DEFAULT_DEST'] = dest
configure_uploads(app, photos)
configure_uploads(app, interactions_upload_set)


class Upload(Resource):
    """HTML for this requst should look something like,

    <form method=POST enctype=multipart/form-data action=something>
    ...
    <input type=file name=upload>
    ...
    </form>
    """

    def post(self):
        print request.files
        if 'photos' in request.files:
            # Remove the previous file if it exists
            path = os.path.join(dest, photos_sub, request.files['photos'].filename)
            if os.path.exists(path):
                os.remove(path)
            # Resize the image passed in
            with Image.open(request.files['photos']) as image:
                image = resizeimage.resize_cover(image, [128, 128], validate=False)
                image.save(path, image.format)
            #filename = photos.save(request.files['photos'])
            return "Success", 201
        elif 'interactions' in request.files:
            print "In interactions!!"
            print request.form
            interaction_id = request.form.get('interaction_id')
            dir_path = os.path.join(dest, interactions_sub, interaction_id)
            print "Path is: " + dir_path
            if not os.path.exists(dir_path):
                print "making the dir!"
                os.makedirs(dir_path)
            path = os.path.join(dir_path, request.files['interactions'].filename)
            if os.path.exists(path):
                os.remove(path)
            print request.files
            filename = interactions_upload_set.save(request.files.get('interactions'), interaction_id)
            print filename
            return "Success", 201
        else:
            msg = 'No file included in upload request'
            abort(400, message=msg)
        
class InteractionFiles(Resource):
    def get(self, id):
        filenames = self.getFileList(id);
        response = {"filenames": filenames}
        return response, 200
    
    # This will delete any files that are not in the posted list
    def post(self, id):
        path = os.path.join(dest, interactions_sub, id)
        existing_files = self.getFileList(id)
        posted_files = list(request.get_json())
        files_to_delete = [x for x in existing_files if x not in posted_files]
        for file in files_to_delete:
            file_path = os.path.join(path, file)
            if not os.path.exists(file_path):
                msg = "File not found"
                abort(401, message=msg)
            else:
                os.remove(file_path)
        return 204

    def getFileList(self, id):
        path = os.path.join(dest, interactions_sub, id)
        if not os.path.exists(path):
            filenames = []
        else:
            filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return filenames