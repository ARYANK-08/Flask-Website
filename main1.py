import cv2
from flask import Flask , render_template, Response,session,request
from age1 import VideoCam
from final1 import Final
from test4 import VideoCamera
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)

            


@app.route('/')
def index():
    return render_template('lol.html')



@app.route('/a')

def a():
    return render_template('a.html')

def gen(age1):
    while True:
        #get camera frame
        frame = age1.try1()
        yield (b'--frame\r\n'
            b'Content-Type: video/mp4\r\n\r\n' + frame + b'\r\n')
        
@app.route('/b')

def b():
    return render_template('b.html')

def gen1(final1):
    while True:
        #get camera frame
        frame2 = final1.main3()
        yield (b'--frame2\r\n'
            b'Content-Type: video/mp4\r\n\r\n' + frame2 + b'\r\n')


@app.route('/video_feed1')
def video_feed1():
    return Response(gen1(Final()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen(VideoCam()), mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/lol')
def lol():
    return render_template('lol.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/create')
def create():
    return render_template('create.html')

#upload image to this folder :
app.config['UPLOAD_FOLDER'] = "C:\\Users\\kyath\\OneDrive\\Desktop\\Start Fresh (2)\\Start Fresh\\images"

@app.route('/index3')

def index3():
    return render_template('index3.html')

def gen3(test4):
    while True:
        frame4=test4.try4()
        yield(b'--frame\r\n'
              b'Content-Type : video/mp4\r\n\r\n'+ frame4
              + b'\r\n\r\n')
        

@app.route('/video_feed')
def video_feed3():
    return Response(gen3(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/uploader" , methods=['GET', 'POST'])
def uploader():
   
    if request.method=='POST':
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return "Uploaded successfully!"


if __name__ == '__main__' :
    app.run(host='0.0.0.0',port='5000',debug=True)

if __name__ == '__main__':
    app.run(debug=True)