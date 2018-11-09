from flask import Flask,jsonify,request,redirect,render_template
import os
from PIL import Image 
import numpy as np
import cv2
import pickle 
from werkzeug.utils import secure_filename
import pickle

face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

ALLOWED_EXTENSIONS = ['bmp']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/static/uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(BASE_DIR,app.config['UPLOAD_FOLDER'],filename)
            print (file_path)
            file.save(file_path)
            image = cv2.imread(file_path)
            while (True):
                #capture frame by frame
                ret,frame = image.read()
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for (x,w,y,h) in faces:
                    #print(x,y,w,h)
                    roi_gray = gray[y:y+h,x:x+w]
                    roi_color = frame[y:y+h,x:x+w]
                    id_,conf  = recognizer.predict(roi_gray)
                    if conf >=45 and conf <=85:
                        print (id_)
                    img_item = file.filename 
                    cv2.imwrite(img_item,roi_gray)
                    color = (255,0,0)
                    stroke = 2 
                    end_cord_x = x + w 
                    end_cord_y = y + h 


    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')