from pathlib import Path
import json
import os

def local_memory_path(user_name: str) -> Path:
    return Path("memory_index") / user_name / f"{user_name}_memories.local.json"

def user_local_file_exists(user_name: str) -> bool:
    return local_memory_path(user_name).exists()


def write_user_local_json(user_name: str, data: dict[str, str]) -> None:
    try:
        with open(local_memory_path(user_name), "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"name": user_name}
    with open(local_memory_path(user_name), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_user_local_json(user_name: str) -> dict[str, str] | None:
    try:
        with open(local_memory_path(user_name), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None