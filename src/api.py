from flask import Flask, flash, request, redirect, url_for, send_from_directory,jsonify
from werkzeug.utils import secure_filename
import os

from createTextFile import createTextFromImages
from plag import checkPlagFunc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A-Z1-9' #<--- SECRET_KEY must be set in config to access session

UPLOAD_FOLDER = '../input-images'
TEXT_OUTPUT_FOLDER = '../output-files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEXT_OUTPUT_FOLDER'] = TEXT_OUTPUT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome'

@app.route('/upload_file/<topic>', methods=['GET', 'POST'])
def upload_file(topic):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('No Selected file')
            return redirect(request.url)
        imageFolder = app.config['UPLOAD_FOLDER'] + '/' + topic
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(imageFolder):
                os.makedirs(imageFolder)

            print(imageFolder, filename)
            file.save(os.path.join(imageFolder, filename))

            text = createTextFromImages(imageFolder, filename,topic)
            data = {'success':bool('true'),'message':'Uploaded Successfully','recognized_text':text}
            return jsonify(data), 200
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/check_plag/<topic>', methods=['GET'])
def check_plag(topic):
    output = checkPlagFunc(app.config['TEXT_OUTPUT_FOLDER']+'/'+topic)
    if output == False:
        return jsonify({'success':False,'message':'Minimum Two files required to check plagarisim'})

    data = {'success':'true','output':output}
    return jsonify(data),200


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

if __name__ == '__main__':
    app.run()
