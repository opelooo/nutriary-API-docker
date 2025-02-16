import os
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, Depends, status

ALLOWED_ORIGINS = ["https://example.com"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def check_origin(request: Request, call_next):
    origin = request.headers.get("origin")

    if origin and origin not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="CORS policy does not allow this origin")

    response = await call_next(request)
    return response

async def verify_referer(request: Request):
    referer = request.headers.get("referer")
    allowed_referers = [
        "example.com",
        "another-example.com"
    ]
    if referer not in allowed_referers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Invalid referer."
        )
        
@app.get("/", response_class=HTMLResponse, dependencies=[Depends(verify_referer)])
def read_index():
    index_path = "path/to/index.html"
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading index file: {e}")
    else:
        raise HTTPException(status_code=404, detail="Index file not found.")

