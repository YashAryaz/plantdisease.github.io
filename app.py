
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
MODEL_PATH ='model.h5'

# Load your trained model
model = load_model(MODEL_PATH)


datagen = ImageDataGenerator(
    rotation_range=25,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    rescale=1/255.0,
    fill_mode='nearest',
    validation_split=0.1)

from tensorflow.keras.utils import load_img,img_to_array

    

def model_predict(img_path, model):
      
    img = image.load_img(img_path, target_size=(64, 64))

    # Preprocess the image using the same ImageDataGenerator
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    img_generator = ImageDataGenerator(
        rotation_range=25,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        fill_mode='nearest',
        horizontal_flip=True
    )
    img_processed = img_generator.standardize(img_array)
    preds=model.predict(img_processed)
    preds=np.argmax(preds, axis=1)
    
    print(preds)
    class_count = {
0: 'Apple_scab(Apple)',
1: 'Black_rot(Apple)',
2: 'Cedar_apple_rust(Apple)',
3: 'Healthy(Apple)',
4: 'Healthy(Blubery)',
5: 'Healthy(Cherry(including_sour))',
6: 'Powdery_mildew(Cherry(including_sour))',
7: 'Cercospora_leaf_spot Gray_leaf_spot(Corn(maize))',
8: 'Common_rust(Corn(maize))',
9: 'Northern_Leaf_Blight(Corn(maize))',
10: 'Healthy(Corn(maize))',
11: 'Black_rot(Grape)',
12: 'Esca(Black_Measles)(Grape)',
13: 'Leaf_blight(Isariopsis_Leaf_Spot)(Grape)',
14: 'Healthy(Grape)',
15: 'Haunglongbing(Citrus_greening)(Orange)',
16: 'Bacterial_spot(Peach)',
17: 'Healthy(Peach)',
18: 'Healthy(Pepper_bell)',
19: 'Early_blight(Potato)',
20: 'Late_blight(Potato)',
21: 'Healthy(Potato)',
22: 'Healthy(Raspberry)',
23: 'Healthy(Soybean)',
24: 'Powdery_mildew(Squash)',
25: 'Leaf_scorch(Straberry)',
26: 'Healthy(Straberry)',
27: 'Rust(Straberry)',
28: 'Bacterial_spot(Tomato)',
29: 'Early_blight(Tomato)',
30: 'Late_blight(Tomato)',
31: 'Leaf_Mold(Tomato)',
32: 'Septoria_leaf_spot(Tomato)',
33: 'Spider_mites Two-spotted_spider_mite(Tomato)',
34: 'Target_Spot(Tomato)',
35: 'Yellow_Leaf_Curl_Virus(Tomato)',
36: 'Mosaic_virus(Tomato)',
37: 'Healthy(Tomato)'
}
    precau={0: 'Causes: Fungal disease. Precautions: Remove and destroy infected leaves, and treat with a fungicide.',
1: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide. ',
2: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
3: 'Healthy',
4: 'Healthy',
5: 'Healthy',
6: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
7: 'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
8: 'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
9: 'Causes: Fungal disease. Precautions: Use resistant varieties and crop rotation.',
10: 'Healthy',
11: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
12: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
13: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
14: 'Healthy',
15: 'Causes: Bacterial disease. Precautions: Remove and destroy infected trees, and control the insect vector.',
16: 'Causes: Bacterial disease. Precautions: Remove infected plant parts, and treat with a bactericide.',
17: 'Healthy',
18: 'Healthy',
19: 'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
20: 'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
21: 'Healthy',
22: 'Healthy',
23: 'Healthy',
24: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
25: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
26: 'Healthy',
27: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
28: 'Causes: Bacterial disease. Precautions: Remove infected plant parts, and treat with a bactericide.',
29: 'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
30: 'Causes: Fungal disease. Precautions: Use disease-free seed and crop rotation.',
31: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
32: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
33: 'Causes: Pest infestation. Precautions: Use insecticidal soap or predatory mites.',
34: 'Causes: Fungal disease. Precautions: Remove infected plant parts, and treat with a fungicide.',
35: 'Causes: Viral disease. Precautions: Control the insect vector and remove infected plants.',
36: 'Causes: Viral disease. Precautions: Use virus-free seed and control the insect vector.',
37: 'Healthy'
    }
    x=preds
    preds=class_count[int(preds)]
    precaution=precau[int(x)]
    print(precaution)
    
    return [preds,precaution]


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
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
