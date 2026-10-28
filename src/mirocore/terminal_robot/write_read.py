from keyword import kwlist
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

    ## 新規データ追加
    # 1周目: key=name, value="takato"
    # 2周目: key=memories, value=["takatoの記憶1", "takatoの記憶2"]
    for key, value in data.items():
        if key == "name":
            loaded_data[key] = value
        elif key == "memories":
            # キーがない時は、空のリストを作成
            if key not in loaded_data:
                loaded_data[key] = []
            ## 記憶を追加
            for memory in value:
                ## 記憶がない時は、追加
                if memory not in loaded_data[key]:
                    loaded_data[key].append(memory)
                ## 記憶がある時は、何もしない
                else:
                    print( "この内容は、すでに記憶されています。")
        else:
            raise ValueError(f"Invalid key: {key}")

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