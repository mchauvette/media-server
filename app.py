from flask import Flask, render_template, send_file
import os, subprocess, math
from PIL import Image

app = Flask(__name__)


def get_mimetype(filename):
    mimetype = None
    if len(filename) >= 4:
        if filename[-4:] == ".mp4":
            mimetype = 'video/mp4'
        elif filename[-4:] == ".jpg":
            mimetype = 'image/jpg'
        elif filename[-4:] == ".png":
            mimetype = 'image/png'
    return mimetype


class Picture(object):

    def __init__(self, filename):
        self.filename = filename

        im = Image.open('pictures/' + filename)
        self.width, self.height = im.size
    
    @staticmethod
    def isPicture(filename):
        try:
            Image.open('pictures/' + filename)
            return True
        except:
            return False


class Video(object):

    def __init__(self, dirname):
        # Only supports .mp4 at the moment with .jpg thumbnails
        self.title = dirname.replace("_", " ")
        self.dirname = dirname
        self.filename = "videos/" + dirname + "/" + dirname + ".mp4"
        self.thumbnail = "videos/" + dirname + "/Thumbnail.jpg"
        duration = Video.get_length(self.filename)
        self.hours = math.floor(duration / 60 / 60)
        self.minutes = math.floor(duration / 60) % 60
    
    @staticmethod
    def hasVideo(dirname):
        if os.path.isdir("videos/" + dirname):
            if os.path.isfile("videos/" + dirname + "/" + dirname + ".mp4"):
                return True
        return False
    
    @staticmethod
    def get_length(filename):
        # Obtained from https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        return float(result.stdout)


@app.route('/')
def index():
    # Load the pictures
    if os.path.exists('pictures'):
        pictures = [Picture(f) for f in os.listdir('pictures') if Picture.isPicture(f)]
        picture_rows = []
        for index in range(0, len(pictures), 4):
            picture_rows += [pictures[index:min(index+4, len(pictures))]]
    else:
        picture_rows = []
    
    # Load the videos
    if os.path.exists('videos'):
        videos = [Video(d) for d in os.listdir('videos') if Video.hasVideo(d)]
    else:
        videos = []

    return render_template('index.html', picture_rows=picture_rows, videos=videos)

@app.route('/pictures/<string:filename>')
def pictures(filename):
    mimetype = get_mimetype(filename)
    return send_file('pictures/' + filename, mimetype=mimetype)

@app.route('/videos/<string:dirname>/<string:filename>')
def videos(dirname, filename):
    mimetype = get_mimetype(filename)
    return send_file('videos/' + dirname + "/" + filename, mimetype=mimetype)

@app.route('/view/pictures/<string:filename>')
def view(filename):
    if not Picture.isPicture(filename):
        return "Sorry, picture does not exist! <a href=\"/\">Return?</a>"
    picture = Picture(filename)
    return render_template('view.html', picture=picture)

@app.route('/watch/videos/<string:dirname>')
def watch(dirname):
    if not Video.hasVideo(dirname):
        return "Sorry, video does not exist! <a href=\"/\">Return?</a>"
    video = Video(dirname)
    return render_template('watch.html', video=video)


if __name__ == "__main__":
    app.run(debug=True)
