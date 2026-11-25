import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from fastapi import HTTPException
from mirocore.terminal_robot.search import (
    search_memory,
    extract_search_keywords
)
from mirocore.terminal_robot.write_read import (
    read_user_local_json
)

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

@app.get("/api/memory/search")
def search_memory_api(user_name: str, query: str):
    try:
        data = read_user_local_json(user_name)
        if data is None:
            raise HTTPException(status_code=404, detail="記憶ファイルが存在しません。")
        memories = data.get("memories", [])
        if not isinstance(memories, list):
            raise HTTPException(status_code=500, detail="記憶データの形式が不正です。")
        # keywords = extract_search_keywords(query, memories)
        keywords = extract_search_keywords(query)
        results = search_memory(memories, keywords)
        return {
            "keywords": keywords,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e