from fastapi import FastAPI

description = """
Nutriary API helps you do clasiffiing indonesian foods. 🚀

## Items

You can go to /documentation for more information and how to use it.

## Users

You will be able to:

* **Send Image and Predict** (Implemented).
"""

tags_metadata = [
    {
        "name" : "predict",
        "description": "Predict an image"
    }
]

app = FastAPI(
    title="Nutriary-API",
    description=description,
    version="2.1.1",
    contact={
        "name": "C23-PC673",
        "url": "https://github.com/BangkitC23-PC673",
        "email": "mathys.alberino@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/mit/",
    },
    openapi_tags=tags_metadata
)