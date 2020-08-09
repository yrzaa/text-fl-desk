import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras


#import keras.backend.tensorflow_backend as tb
#keras.backend.tensorflow_backend._SYMBOLIC_SCOPE.value = True

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow_hub as hub

# Some utilites
import numpy as np
from util import base64_to_pil
import requests

#Desktop implementation
import webview
import threading


# Declare a flask app
app = Flask(__name__)


# You can use pretrained model from Keras
# Check https://keras.io/applications/
'''
from keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')
'''
#print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'models/imdb.h5'

# Load your own trained model
model = load_model(MODEL_PATH,custom_objects={'KerasLayer':hub.KerasLayer})
#model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')


def model_predict(review, model):
    x=[review]
    preds = model.predict(x)
    if preds>=0:            #encode prediction to binary
        preds=1
    else:
        preds=0
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        

        
        # Make prediction
        
        img=request.json['input']                           #input
        preds = model_predict(img, model)
        data={"success":True}
        data["result"]=preds
        print("procesed")
        # Serialize the result
        return jsonify(result=preds)

    return None

#run server
def serverth():
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

def onClosed():
    sys.exit()


if __name__ == '__main__':

    #start server
    t = threading.Thread(target=serverth)
    t.daemon = True
    t.start()

    #define window
    window=webview.create_window("ImDB review classifier","http://127.0.0.1:5000/",width=1600, height=900, \
                      x=None, y=None, resizable=True, fullscreen=False, \
                      min_size=(200, 100), hidden=False, frameless=False, \
                      minimized=False, on_top=False, confirm_close=False, \
                      background_color='#1cfff0', text_select=False)
    window.closed+=onClosed
    #start window
    webview.start(debug=True,gui='cef')
   
    #window
    
    