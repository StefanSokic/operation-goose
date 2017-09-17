#!flask/bin/python
from flask import Flask, jsonify, request, redirect, url_for, flash, request, \
    abort
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav', 'avi'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            #filepath = os.path.join(current_app.root_                       app.config['UPLOAD_FOLDER']filename)
            #file.save(filepath)
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.system("bash process_video.sh " + '/uploads/' + filename)
            log = open('./output/log.txt', 'r')
            log_r = log.read()
            vid_log = ""
            for i in log_r:
                if i == "[":
                    vid_log += "<br>["
                else:
                    vid_log += i

            return vid_log
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
