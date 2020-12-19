from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER

media = Blueprint('media', __name__)

from PIL import Image
import os, subprocess, math

ROW_WIDTH = 6  # Number of images per row


def get_mimetype(filename):
    mimetype = None
    if len(filename) >= 4:
        if filename[-4:] == ".gif":
            mimetype = 'image/gif'
        elif filename[-4:] == ".jpg":
            mimetype = 'image/jpeg'
        elif filename[-4:] == ".jpeg":
            mimetype = 'image/jpeg'
        elif filename[-4:] == ".png":
            mimetype = 'image/png'
    return mimetype


class Picture(object):

    def __init__(self, filename, user_dir):
        self.filename = filename
        self.filepath = os.path.join(user_dir, filename)
        im = Image.open(self.filepath)
        self.width, self.height = im.size
    
    @staticmethod
    def isPicture(filename, user_dir):
        try:
            Image.open(os.path.join(user_dir, filename))
            return True
        except:
            return False


# obtained from https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_dir():
    return os.path.join(UPLOAD_FOLDER, current_user.email)

@media.route('/pictures')
@login_required
def pictures():
    # Load the pictures
    user_dir = get_user_dir()
    print("user_dir {}".format(user_dir))
    if os.path.exists(user_dir):
        print("test")
        pictures = [Picture(f, user_dir) for f in os.listdir(user_dir) if Picture.isPicture(f, user_dir)]
        picture_rows = []
        for index in range(0, len(pictures), ROW_WIDTH):
            picture_rows += [pictures[index:min(index+ROW_WIDTH, len(pictures))]]
    else:
        print("test2")
        picture_rows = []
    return render_template('pictures.html', name=current_user.name, picture_rows=picture_rows)

@media.route('/picture/<string:filename>')
@login_required
def picture(filename):
    mimetype = get_mimetype(filename)
    user_dir = get_user_dir()
    return send_file(os.path.join(user_dir, filename), mimetype=mimetype)

@media.route('/view/pictures/<string:filename>')
@login_required
def view_picture(filename):
    user_dir = get_user_dir()
    if not Picture.isPicture(filename, user_dir):
        return redirect(url_for('media.pictures'))
    picture = Picture(filename, user_dir)
    return render_template('picture.html', name=current_user.name, picture=picture)

@media.route('/delete/picture/<string:filename>')
@login_required
def delete_picture(filename):
    user_dir = get_user_dir()
    if Picture.isPicture(filename, user_dir):
        os.remove(os.path.join(user_dir, filename))
    return redirect(url_for('media.pictures'))

@media.route('/upload')
@login_required
def upload():
    return render_template('upload.html', name=current_user.name)

@media.route('/upload', methods=['POST'])
@login_required
def upload_post():
    # obtained from https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        user_dir = get_user_dir()
        filename = secure_filename(file.filename)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        file.save(os.path.join(user_dir, filename))
        return redirect(url_for('media.pictures'))
    return redirect(request.url)
