from mirocore.terminal_robot.write_read import (
    local_memory_path,
    user_local_file_exists,
    write_user_local_json,
    read_user_local_json
)
from pathlib import Path
import pytest
from pytest import MonkeyPatch

def test_local_memory_path() -> None:
    user_name = "test"
    file_path = Path("memory_index") / user_name / f"{user_name}_memories.local.json"
    assert local_memory_path(user_name) == file_path

def test_user_local_file_exists() -> None:
    assert user_local_file_exists("test") == True

def test_read_user_local_json() -> dict[str, str | list[str]] | None:
    user_name = "test"
    data = {
        "name": user_name,
        "memories": []
    }
    assert read_user_local_json(user_name) == data

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