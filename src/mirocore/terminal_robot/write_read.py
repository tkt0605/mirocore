from pathlib import Path
import json
import os
import tempfile

# R02の根本原因
def local_memory_path(user_name: str) -> Path:
    return Path("memory_index") / user_name / f"{user_name}_memories.local.json"

def user_local_file_exists(user_name: str) -> bool:
    return local_memory_path(user_name).exists()


def write_user_local_json(
    user_name: str,
    data: dict[str, str | list[str]]
) -> None:
    path = local_memory_path(user_name)
    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

    except FileNotFoundError:
        loaded_data = {
            "name": user_name
        }
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"既存のJSONファイルが破損しているため、安全のために保存を中止しました: {path}"
        ) from e

    for key, value in data.items():
        if key == "name":
            if isinstance(value, str):
                loaded_data[key] = value
            else:
                raise ValueError("The 'name' key must be a string.")
        
        elif key == "memories":
            if "memories" not in loaded_data:
                loaded_data[key] = []

            if isinstance(value, str):
                memories_to_add = [value]
            else:
                memories_to_add = value
            for memory in memories_to_add:
                if memory not in loaded_data[key]:
                    loaded_data[key].append(memory)
        
        else:
            raise ValueError(f"Invalid key: {key}")
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
            temp_file = tf.name
            json.dump(loaded_data, tf, ensure_ascii=False, indent=4)
        
        if temp_file:
            os.replace(temp_file, path)

    except OSError as e:
        raise RuntimeError(
            f"ユーザーのローカルデータの保存に失敗しました: {e}"
        ) from e
    
    finally:
        if temp_file is not None and os.path.exists(temp_file):
            os.remove(temp_file)
        


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

    except json.JSONDecodeError as json_error:
        print(f"既存のJSONファイルが破損しているため、読み込めませんでした: {json_error}")
        return None