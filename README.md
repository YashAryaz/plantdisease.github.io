#Plant Disease Detector
This is a machine learning project that uses a CNN (Convolutional Neural Network) model for image classification to detect plant diseases. The model is trained on a dataset of images of plants with different diseases and healthy plants. The goal is to accurately identify the disease affecting the plant based on an input image.

Dataset
The dataset used to train the model contains images of the following plants and their corresponding diseases:

Apple: Apple_scab, Black_rot, Cedar_apple_rust, Healthy
Blueberry: Healthy
Cherry (including sour): Powdery_mildew, Healthy
Corn (maize): Cercospora_leaf_spot Gray_leaf_spot, Common_rust, Northern_Leaf_Blight, Healthy
Grape: Black_rot, Esca(Black_Measles), Leaf_blight(Isariopsis_Leaf_Spot), Healthy
Orange: Haunglongbing(Citrus_greening)
Peach: Bacterial_spot, Healthy
Pepper_bell: Bacterial_spot, Healthy
Potato: Early_blight, Late_blight, Healthy
Raspberry: Healthy
Soybean: Healthy
Squash: Powdery_mildew
Strawberry: Leaf_scorch, Healthy
Tomato: Bacterial_spot, Early_blight, Late_blight, Leaf_Mold, Septoria_leaf_spot, Spider_mites Two-spotted_spider_mite, Target_Spot, Yellow_Leaf_Curl_Virus, Mosaic_virus, Healthy
Model
The CNN model used for image classification is trained on the dataset mentioned above. The model is a deep learning architecture that consists of multiple convolutional layers and pooling layers followed by fully connected layers. The model is trained on a GPU to speed up the training process and improve the accuracy.

Flask Deployment
This project uses Flask to deploy the trained model for inference. Flask is a micro web framework written in Python that allows us to serve a web application using a Python script. The web application created for this project allows the user to upload an image of a plant and get a prediction of the disease affecting the plant.

Limitations
This model can only classify the diseases mentioned above for the only above plants and disease
It has an accuracy of 94% so there must be chancse thst it will predict wrong disease.
#Requirements:
Flask
tensorflow
python >3.9
