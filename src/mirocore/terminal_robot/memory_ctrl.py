## メモリ操作のファイル
import os
import json
from pathlib import Path
from mirocore.terminal_robot.write_read import (
    local_memory_path,
    user_local_file_exists,
    create_json_folder,
    write_user_local_json,
    read_user_local_json,
    delete_user_local_file,
)

## 今はまだ、具体的に実装することはないが、メモリ操作に対する機能一覧。
## メモリ操作の関数。
class MemoryControl:
    def __init__(self, user_name: str) -> None:
        pass
    
    ## ユーザー名の特定
    def get_user_name(self) -> str:
        return self.get_user_name

    ## ユーザー名のローカルファイルの特定
    def get_user_local_file(self) -> Path:
        user_name = self.get_user_name()
        return local_memory_path(user_name)
        
    ## ユーザー名のローカルファイルの存在確認
    def user_local_file_exists(self) -> bool:
        user_name = self.get_user_name()
        return user_local_file_exists(user_name)

    ## ユーザー名のローカルファイルの作成
    def create_user_local_file(self) -> None:
        user_name = self.get_user_name()
        return create_json_folder(user_name)

    ## ユーザー名のローカルファイルの読み込み
    def read_user_local_file(self) -> dict[str, str | list[str]] | None:
        user_name = self.get_user_name()
        return read_user_local_json(user_name)

    ## ユーザー名のローカルファイルの書き込み
    def write_user_local_file(self, data: dict[str, str | list[str]]) -> None:
        user_name = self.get_user_name()
        return write_user_local_json(user_name, data)

    ## ユーザー名のローカルファイルの削除
    def delete_user_local_file(self) -> None:
        user_name = self.get_user_name()
        return delete_user_local_file(user_name)
        
        
    