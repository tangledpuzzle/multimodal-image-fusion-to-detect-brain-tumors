import os
from datetime import datetime
from flask import Flask, render_template, request, url_for

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import cv2
import imageio
import scipy.ndimage as ndi

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def convertToIntList(arr):
    result=[]
    for q in arr.strip(']][[').split('],['):
        x=[]
        for i in q.split(','):
            x.append(int(i,10))
        result.append(x)
    return result

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)

    mri_file=request.files['mri']
    ct_file=request.files['ct']

    destination1 = "/".join([target, "mri.jpg"])
    mri_file.save(destination1)

    destination2 = "/".join([target, "ct.jpg"])
    ct_file.save(destination2)
    
    points = request.form["points"] #no of points

    return render_template("registration.html", points=points)

@app.route("/register",methods=['POST'])
def register():
    global mriCoord, ctCoord
    mriCoord=convertToIntList(request.form['mriCoord'])
    ctCoord=convertToIntList(request.form['ctCoord'])
    return "something"

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    app.run(debug=True)