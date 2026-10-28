from pathlib import Path
import json
import os

def local_memory_path(user_name: str) -> Path:
    return Path("memory_index") / user_name / f"{user_name}_memories.local.json"

def user_local_file_exists(user_name: str) -> bool:
    return local_memory_path(user_name).exists()


def write_user_local_json(
    user_name: str,
    data: dict[str, str | list[str]]
) -> None:
    try:
        with open(
            local_memory_path(user_name),
            "r",
            encoding="utf-8"
        ) as f:
            loaded_data = json.load(f)
    except FileNotFoundError:
        loaded_data = {
            "name": user_name
        }
    ## 新規データ追加。
    ## 入れ込んだ情報を各キーとして分解し保存。
    for key, new_memory in data.items():
        if isinstance(new_memory, list):
            if new_memory:
                loaded_data[key] = new_memory
            continue
        if not new_memory:
            continue
        
        if not isinstance(loaded_data.get(key), list):
            loaded_data[key] = []
        
        for memory in new_memory:
            if memory not in loaded_data[key]:
                loaded_data[key].append(memory)
    with open(
        local_memory_path(user_name),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(loaded_data, f, ensure_ascii=False, indent=4)
        


def read_user_local_json(user_name: str) -> dict[str, str | list[str]] | None:
    try:
        with open(
            local_memory_path(user_name),
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None