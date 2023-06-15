from fastapi import FastAPI, UploadFile, File, HTTPException
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
    try:
        # Make the prediction
        prediction = model.predict(image)
        predicted_class = np.argmax(prediction)

        class_name = class_names[predicted_class]
        probability = np.max(prediction) * 100
    except Exception as e:
        return {"error" : str(e)}
    
    return {"class" : str(class_name), "probability" : probability}

def get_all():
    return Querying_filter("SELECT * FROM nutrisi")

def filter_data(nama_makanan):
    return Querying_filter(f"SELECT * FROM nutrisi WHERE nama_bahan_makanan LIKE \"%{str(nama_makanan)}%\"")

def filter_data_one_output(nama_makanan):
    return Querying_filter(f"SELECT * FROM nutrisi WHERE nama_bahan_makanan LIKE \"{str(nama_makanan)}\"")

def send_query(qry):
    try:
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
        query = qry
        cursor.execute(query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        
    except Exception as e:
        # Tangani kesalahan jika terjadi
        return str(e)
    finally:
        # Close the cursor and database connection
        cursor.close()
        cnx.close()

    return rows

def Querying_filter(qry):

    rows = send_query(qry)

    # Create a list to store the JSON data
    json_data = []

    # Iterate over the rows and convert each row to a dictionary
    for row in rows:
        data = {
            'kode': str(row[0]),
            'nama_bahan_makanan': str(row[1]),
            'energi_kal': str(row[2]),
            'protein_g': str(row[3]),
            'lemak_g': str(row[4]),
            'karbohidrat_g': str(row[5]),
            'serat_g': str(row[6]),
            'kalsium_mg': str(row[7]),
            'besi_mg': str(row[8]),
            'natrium_mg': str(row[9]),
            'serving_size_g': str(row[10])
            # Add more columns as needed
        }
        json_data.append(data)
    
    return {"data": json_data}


