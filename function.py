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
import mysql.connector

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
    msg = None
    try:
        # Make the prediction
        prediction = model.predict(image)
        predicted_class = np.argmax(prediction)

        class_name = class_names[predicted_class]
        probability = np.max(prediction) * 100
    except Exception as e:
        msg = response(status="error", e=e)
    else:
        # Return the predicted class
        msg = response(class_name=class_name, probability=probability, status="success")
    finally:
        return msg

def response(status, e = None, class_name = None, probability = None):
    msg = None
    if status == "success":
        msg = {
        "status" : str(status),
        "data" : {
            "post" : { "class" : str(class_name), "probability" : probability}
            }
        }
    if status == "error":
        msg =  {
            "status" : str(status),
            "message" : str(e)
            }
    return msg

def get_data_from_database():
    # Connect to MySQL database
    cnx = mysql.connector.connect(
        host='34.101.96.36',
        user='mathys-seilatu',
        password='_ISJXQ@:#_/FjC,Y',
        database='nutriary'
    )

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Execute SQL query to fetch data
    query = "SELECT * FROM nutrisi"
    cursor.execute(query)

    # Fetch all rows from the result
    rows = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    cnx.close()

    # Create a list to store the JSON data
    json_data = []

    # Iterate over the rows and convert each row to a dictionary
    for row in rows:
        data = {
            'kode': row[0],
            'nama_bahan_makanan': row[1],
            'energi_kal': row[2],
            'protein_g': row[3],
            'lemak_g': row[4],
            'karbohidrat_g': row[5],
            'serat_g': row[6],
            'kalsium_mg': row[7],
            'besi_mg': row[8],
            'natrium_mg': row[9]
            # Add more columns as needed
        }
        json_data.append(data)

    return json_data