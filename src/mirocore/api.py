from email.policy import HTTP
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
    read_user_local_json,
    specific_delete_user_local_json,
    write_user_local_json,
)
from mirocore.terminal_robot.reply import propose_memory

load_dotenv()
def split_csb(value: str | None) -> list[str]:
    if value is None:
        return []
    return [
        item.strip() for item in value.split(",") if item.strip()
    ]
ALLOW_ORIGINS = split_csb(os.getenv("CORS_ALLOW_ORIGINS"))
ALLOW_METHODS = split_csb(os.getenv("CORS_ALLOW_METHODS"))
ALLOW_HEADERS = split_csb(os.getenv("CORS_ALLOW_HEADERS"))

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

@app.post("/api/memory/write")
def write_memory_api(user_name:  str, text: str) -> dict[str, str | bool]:
    # try:
    #     data = read_user_local_json(user_name)
    #     if data is None:
    #         raise HTTPException(status_code=404, detail="記憶ファイルが存在しません。")
    #     memories = data.get('memories', [])
    #     ## memoriesはリストであることを確認
    #     if not isinstance(memories, list):
    #         raise HTTPException(status_code=500, detail="記憶データの形式が不正です。")
    #     memories.append({
    #         ""
    #     })
    try:
        memory = propose_memory(text)
        if memory is None:
            return {
                "saved": False,
                "message": "保存する文ではありません。",
            }
        write_user_local_json(user_name, {"memories": memory})
        return {
            "saved": True,
            "message": "記憶を追加しました。",
            "memory": memory,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/api/memory/read")
def read_memory_api(user_name: str, text: str) -> dict[str, list[str]]:
    try:
        data = read_user_local_json(user_name)
        if data is None:
            raise HTTPException(status_code=404, detail="記憶ファイルが存在しません。")
        memories = data.get("memories", [])
        if not isinstance(memories, list):
            raise HTTPException(status_code=500, detail="記憶データの形式が不正です。")
        results = [memory for memory in memories if text in memory]
        return {
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.delete("/api/memory/delete")
def delete_memory_api(user_name: str, text: str) -> dict[str, str |  list[str] | bool]:
    try:
        data = read_user_local_json(user_name)
        if data is None:
            raise HTTPException(status_code=404, detail="記憶ファイルが存在しません。")
        memories = data.get("memories", [])
        if not isinstance(memories, list):
            raise HTTPException(status_code=500, detail="記憶データの形式が不正です。")
        keywords = extract_search_keywords(text)
        matched_memory = search_memory(memories, keywords)
        if len(matched_memory) == 0:
            return {
                "deleted": False,
                "message": "削除する記憶が見つかりません。",
                "results": [],
            }
        if len(matched_memory) > 1:
            return {
                "deleted": False,
                "message": "複数の記憶が見つかりました。",
                "results": matched_memory,
            }
        target_memory = matched_memory[0]
        remaining = [
            memory for memory in memories if memory != target_memory
        ]
        specific_delete_user_local_json(user_name, remaining)
        return {
            "deleted": True,
            "message": "記憶を削除しました。",
            "results": remaining,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e