from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_file
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow import expand_dims
from tensorflow.nn import softmax
import tensorflow as tf
from numpy import argmax
from numpy import max
from numpy import array
from json import dumps
from uvicorn import run
import numpy as np
from PIL import Image
import os
import io

class_names = ['bakso', 'gado', 'rendang', 'sate']

model_dir = "models/model-Bloss-1685804794.265851.h5"
model = load_model(model_dir)

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to match the input size of the model
    image_array = np.array(image)
    image_array = tf.keras.applications.xception.preprocess_input(image_array)
    image_array = np.expand_dims(image, axis=0)
    return image_array

def predict(image):
    try:
        # Make the prediction
        prediction = model.predict(image)
        predicted_class = np.argmax(prediction)

        class_name = class_names[predicted_class]
        probability = np.max(prediction) * 100
    except Exception as e:
        return {"error" : str(e)}
    
    return {"class" : str(class_name), "probability" : probability}