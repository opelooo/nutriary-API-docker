# Deployment Documentation

## Using GCP console

- You need to setup the Dockerfile first
- Use port 8080
- run `gcloud builds submit --tag gcr.io/{project name}/{container name}`
- then run `gcloud run deploy --image gcr.io/{project name}/{container name} --platform manage`
- select `asia-southeast2 server`
- turn on `Allow unauthenticated invocations`
- use `CPU is only allocated during request processing`
- and then set the Execution environment to `second gen`

for example
```
gcloud builds submit --tag gcr.io/nutriary-api/test
gcloud run deploy --image gcr.io/nutriary-api/test --platform managed
```


# Nutriary API Documentation

Welcome to the Nutriary API documentation. This API allows you to classify Indonesian food images using TensorFlow, providing information about the predicted food class and its corresponding probability.

## Introduction

The Nutriary API is designed to assist users in identifying and categorizing Indonesian food items from images. By leveraging the power of TensorFlow, a popular deep learning framework, the API can accurately classify food images and provide valuable insights into their nutritional value.

## Getting Started

To get started with the Nutriary API, follow these steps:

- Make sure to use the full HTTPS URL to access the API, for example `https://nutriary-api.up.railway.app`
- use `POST /predict` to submit an image for classification. This endpoint accepts image files as input and returns the predicted food class along with the probability.
- Set the request content type to `multipart/form-data`.
- Include the food image file in the request payload with a key named `file`.
- Send the request and wait for the response.
- Receive the response from the API, which will contain the predicted class and probability of the food item.
- Process and utilize the classification results according to your application's requirements.

## Usage

### `POST /predict`

Submit an image file for classification. The request should be made using the `multipart/form-data` content type, with the image file attached as `file` field.

Example Request:
```http
POST /predict HTTP/1.1
Content-Type: multipart/form-data;
Content-Disposition: form-data; name="file"; filename="food_image.jpg"
Content-Type: image/jpeg
1/1 [==============================] - ETA: 0s
1/1 [==============================] - 0s 32ms/step
```

Example Response:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "class": "rendang",
    "probability": 95.85497379302979
}
```

### Error Handling

In case of an error, the API will respond with an appropriate HTTP status code and an error message in the response body. Please refer to the response codes and messages to identify and handle errors correctly.
