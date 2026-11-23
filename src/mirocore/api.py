import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS").split(",")
ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS").split(",")
ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS").split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

@app.get("/api/health")
def delivery_health_check():
    return {
        "status": "ok",
        "message": "Hi, This is Miroc Core API."
    }