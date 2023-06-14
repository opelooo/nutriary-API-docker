import os
import io
import apis_config as config
import function as func
from PIL import Image
from starlette.responses import FileResponse 
from fastapi import UploadFile, File

app = config.app

# Defining path operation for root endpoint
@app.get('/')
def main():
    return {'message': 'Welcome to Nutriary Model test API!'}

# Defining path operation for /documentation endpoint
@app.get("/documentation")
async def read_index():
    return FileResponse('doc/index.html')
 
# Defining path operation for /predict endpoint
@app.post('/predict')
async def predict_image(file: UploadFile = File(...)):
    # Read and preprocess the image
    content = await file.read()
    try:
        image = Image.open(io.BytesIO(content))
    except Exception as e:
        return func.response(status="error", e=e)
    
    image = func.preprocess_image(image)

    prediction = func.predict(image)

    # Return the predicted class
    return prediction

@app.get('/nutrisi')
async def get_data():
    # Get data from the database
    data = func.get_all()

    # Return the data as JSON response
    return {"data": data}

@app.get('/nutrisi/{nama_makanan}')
async def get_data():
    # Get data from the database
    data = func.filter_data(nama_makanan)

    # Return the data as JSON response
    return {"data": data}

# @app.post('/nutrisi/{nama_makanan}')
# async def get_data():
#     # Get data from the database
#     data = func.filter_data(nama_makanan)

#     # Return the data as JSON response
#     return {"data": data}

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8080))
	run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)