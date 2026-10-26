import json
import os

def user_local_file_exists(user_name: str) -> bool:
    return os.path.exists(f"memory_index/{user_name}/{user_name}_memories.local.json")