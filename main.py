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
    return data

@app.get('/nutrisi/{nama_makanan}')
async def get_specific_data(nama_makanan: str):
    data={}
    # Get data from the database
    data = func.filter_data(nama_makanan)

    # Return the data as JSON response
    if data: 
        return data
    else:
        return {"message": "No data found"}

@app.get('/nutrisi-specific/{nama_makanan}')
async def get_one_data(nama_makanan: str):
    data={}
    if nama_makanan.lower() == "bakso":
        nama_makanan = "Bakso daging sapi"
        # Get data from the database
        data = func.filter_data_one_output(nama_makanan)
    if nama_makanan.lower() == "sate":
        nama_makanan = "Sate ayam"
        # Get data from the database
        data = func.filter_data_one_output(nama_makanan)
    if nama_makanan.lower() == "rendang":
        nama_makanan = "Rendang sapi masakan"
        # Get data from the database
        data = func.filter_data_one_output(nama_makanan)
    if nama_makanan.lower() == "gado":
        nama_makanan = "Gado-gado"
        # Get data from the database
        data = func.filter_data_one_output(nama_makanan)
    else:
        # Get data from the database
        data = func.filter_data_one_output(nama_makanan)

    # Return the data as JSON response
    if data: 
        return data
    else:
        return {"message": "No data found"}

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8080))
	run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)