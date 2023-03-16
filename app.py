from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
from keras.models import load_model
# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model.h5'

# Load your trained model
model = load_model(MODEL_PATH)

from tensorflow.keras.utils import load_img, img_to_array


def model_predict(img_path, model):

  img = image.load_img(img_path, target_size=(64, 64))

  img_array = image.img_to_array(img)

  img_array = np.expand_dims(img_array, axis=0)

  preds = model.predict(img_array)
  preds = np.argmax(preds, axis=1)

  print(preds)
  class_count = {
    0: 'Apple_scab(Apple)',
    1: 'Black_rot(Apple)',
    2: 'Cedar_apple_rust(Apple)',
    3: 'No(Apple)',
    4: 'No(Blubery)',
    5: 'Powdery_mildew(Cherry(including_sour))',
    6: 'No(Cherry(including_sour))',
    7: 'Cercospora_leaf_spot Gray_leaf_spot(Corn(maize))',
    8: 'Common_rust(Corn(maize))',
    9: 'Northern_Leaf_Blight(Corn(maize))',
    10: 'No(Corn(maize))',
    11: 'Black_rot(Grape)',
    12: 'Esca(Black_Measles)(Grape)',
    13: 'Leaf_blight(Isariopsis_Leaf_Spot)(Grape)',
    14: 'No(Grape)',
    15: 'Haunglongbing(Citrus_greening)(Orange)',
    16: 'Bacterial_spot(Peach)',
    17: 'No(Peach)',
    18: 'Bacterial_spot(Pepper_bell)',
    19: 'No(Pepper_bell)',
    20: 'Early_blight(Potato)',
    21: 'Late_blight(Potato)',
    22: 'No(Potato)',
    23: 'No(Raspberry)',
    24: 'No(Soybean)',
    25: 'Powdery_mildew(Squash)',
    27: 'Leaf_scorch(Straberry)',
    28: 'No(Straberry)',
    29: 'Bacterial_spot(Tomato)',
    31: 'Early_blight(Tomato)',
    32: 'Late_blight(Tomato)',
    33: 'Leaf_Mold(Tomato)',
    34: 'Septoria_leaf_spot(Tomato)',
    35: 'Spider_mites Two-spotted_spider_mite(Tomato)',
    36: 'Target_Spot(Tomato)',
    37: 'Yellow_Leaf_Curl_Virus(Tomato)',
    38: 'Mosaic_virus(Tomato)',
    39: 'No(Tomato)'
  }
  precau = {
    0:
    'Causes: Fungal disease. Precautions: Remove and destroy infected leaves, and treat with a fungicide.',
    1:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide. ',
    2:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    3: 'Healthy',
    4: 'Healthy',
    5:
    'Causes:Fungal disease. Precautions: Ensure good air circulation around plants, avoid over-watering, and use fungicides when necessary',
    6: 'Healthy',
    7:
    'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
    8:
    'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
    9:
    'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
    10: 'Healthy',
    11:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    12:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    13:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    14: 'Healthy',
    15:
    'Causes: Bacterial disease. Precautions: Remove and destroy infected trees, and control the insect vector.',
    16:
    'Causes: Bacterial disease. Precautions: Remove infected plant parts, and treat with a bactericide.',
    17: 'Healthy',
    18:
    'Causes: Bacterial disease. Precautions: Remove infected plant parts, and treat with a bactericide.',
    19: 'Healthy',
    20:
    'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
    21:
    'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
    22: 'Healthy',
    23: 'Healthy',
    24: 'Healthy',
    25:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    26:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    27:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    28: 'Healthy',
    29:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    30:
    'Causes: Bacterial disease. Precautions: Remove infected plant parts, and treat with a bactericide.',
    31:
    'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
    32:
    'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
    33:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    34:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    35:
    'Causes: Pest infestation. Precautions: Use insecticidal soap or predatory mites.',
    36:
    'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
    37:
    'Causes: Viral disease. Precautions: Control the insect vector and remove infected plants.',
    38:
    'Causes: Viral disease. Precautions: Use virus-free seed and control the insect vector.',
    39: 'Healthy'
  }

  x = preds
  preds = class_count[int(preds)]
  precaution = precau[int(x)]
  print(precaution)

  return [preds, precaution]


@app.route('/', methods=['GET'])
def index():
  # Main page
  return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    # Get the file from post request
    f = request.files['file']

    # Save the file to ./uploads
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
    f.save(file_path)

    # Make prediction
    preds = model_predict(file_path, model)
    result = preds
    return result
  return None


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
