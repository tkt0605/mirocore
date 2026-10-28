from pathlib import Path
import json
import os

def local_memory_path(user_name: str) -> Path:
    return Path("memory_index") / user_name / f"{user_name}_memories.local.json"

def user_local_file_exists(user_name: str) -> bool:
    return local_memory_path(user_name).exists()


def write_user_local_json(
    user_name: str,
    data: dict[str, list[str]]
) -> None:
    try:
        with open(local_memory_path(user_name), "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
    except FileNotFoundError:
        loaded_data = {
            "name": user_name
        }
    for key, new_memory in data.items():
        if not new_memory:
            continue
        if key not in loaded_data:
            loaded_data[key] = []
        for memory in new_memory:
            if memory not in loaded_data[key]:
                loaded_data[key].append(memory)
    
    with open(local_memory_path(user_name), "w", encoding="utf-8") as f:
        json.dump(loaded_data, f, ensure_ascii=False, indent=4)
        


def read_user_local_json(user_name: str) -> dict[str, list[str]] | None:
    try:
        with open(local_memory_path(user_name), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None