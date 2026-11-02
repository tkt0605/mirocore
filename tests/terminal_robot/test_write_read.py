from mirocore.terminal_robot.write_read import (
    local_memory_path,
    write_user_local_json,
    read_user_local_json
)
from pathlib import Path
import pytest
from pytest import MonkeyPatch

# 読み込み操作時のテスト
def test_local_memory_path() -> None:
    user_name = "test"
    file_path = Path("memory_index") / user_name / f"{user_name}_memories.local.json"
    assert local_memory_path(user_name) == file_path

def test_read_user_local_json(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True) 
    data = {
        "name": user_name,
        "memories": []
    }
    write_user_local_json(user_name, data)
    assert read_user_local_json(user_name) == data

def test_read_user_local_json_invalid_file(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "new_user"
    local_memory_path(user_name).parent.mkdir(parents=True)
    
    assert read_user_local_json(user_name) is None


# 書き込み操作時のテスト
## 追加するテストを以下に記入
### - os.replace()が失敗しても、元ファイルの内容が変わらない。
### - 失敗後、一時ファイルが残らない。

def test_write_user_local_json(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)
    data = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
            "私もテストです。",
            "おはよう"
        ]
    }
    write_user_local_json(user_name, data)
    assert read_user_local_json(user_name) == data


def test_write_user_local_json_add_save(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)
    data = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
        ]
    }
    write_user_local_json(user_name, data)

    # additional_data = data["memories"].append("私もテストです。")
    additional_data = {
        "name": user_name,
        "memories": [
            "私もテストです。",
        ]
    }
    write_user_local_json(user_name, additional_data)
    result = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
            "私もテストです。",
        ]
    }
    assert read_user_local_json(user_name) == result

## 書き込み途中で例外が発生しても、元ファイルの内容が変わらない
def test_write_user_local_json_exception(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)
    default_data = {
        "name": user_name,
        "memories": [
            "僕は、テストユーザです。"
        ]
    }
    write_user_local_json(user_name, default_data)

    def failing_dump(data, file, **kwargs):
        ## file文字列を書く
        ## 例外を発生させる
        file.write("エラーですね。")
        raise OSError("書き込み失敗を確認")

    monkeypatch.setattr(
        "json.dump",
        failing_dump
    )

    with pytest.raises(RuntimeError):
        exception_data = {
            "name": user_name,
            "memories": [
                "僕は、テストユーザです。",
                "私もテストユーザです。",
            ]
        }
        write_user_local_json(user_name, exception_data)
    assert read_user_local_json(user_name) == default_data

def test_write_user_local_json_same_save(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)
    default_data = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
        ]
    }
    write_user_local_json(user_name, default_data)
    additional_data = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
        ]
    }
    write_user_local_json(user_name, additional_data)
    assert read_user_local_json(user_name) == default_data

def test_write_user_local_json_invalid_key(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)

    default_data = {
        "name": user_name,
        "memories": [
            "僕は、テストです。",
        ]
    }

    write_user_local_json(user_name, default_data)

    with pytest.raises(ValueError):
        invalid_data = {
            "name": user_name,
            "memoriews": [
                "僕は、テストです。",
            ],
        }
        write_user_local_json(user_name, invalid_data)
    assert read_user_local_json(user_name) == default_data
