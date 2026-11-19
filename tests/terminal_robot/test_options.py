from email.policy import default
from threading import local
# from pytest import MonkeyPatch
from mirocore.terminal_robot.search import extract_search_keywords, search_memory
from mirocore.terminal_robot.write_read import (
    local_memory_path,
    read_user_local_json,
    write_user_local_json,
)
from mirocore.terminal_robot.options import (
    on_delete,
    terminal_robot_state,
    on_listening,
    on_thinking,
    create_json_folder,
    on_selected_data
)
from mirocore.terminal_robot.state import (
    RobotEvent,
    RobotState,
    transition
)
from pytest import MonkeyPatch
from pathlib import Path
import pytest
import os


## terminal_robot_stateのテスト条件追加
@pytest.mark.parametrize(
    ("state", "event", "excepted_state"),
    [
        (
            RobotState.IDLE,
            RobotEvent.START_LISTENING,
            RobotState.LISTENING
        ),
        (
            RobotState.LISTENING,
            RobotEvent.CONFIRM_INPUT,
            RobotState.THINKING
        ),
        (
            RobotState.THINKING,
            RobotEvent.REPLY_READY,
            RobotState.SPEAKING
        ),
        (
            RobotState.SPEAKING,
            RobotEvent.OUTPUT_DONE,
            RobotState.IDLE
        ),
        (
            RobotState.ERROR,
            RobotEvent.ERROR_SHOWN,
            RobotState.IDLE
        ),
        (
            RobotState.LISTENING,
            RobotEvent.EMPTY_INPUT,
            RobotState.EMPTY
        ),
        (
            RobotState.EMPTY,
            RobotEvent.START_LISTENING,
            RobotState.LISTENING
        ),
        (
            RobotState.EMPTY,
            RobotEvent.ERROR_SHOWN,
            RobotState.IDLE
        )
    ]
)
def test_terminal_robot_state(
    state: RobotState,
    event: RobotEvent,
    excepted_state: RobotState,
) -> None:
    
    assert terminal_robot_state(state, event) == excepted_state

@pytest.mark.parametrize(
    ("input_text", "excepted_event", "excepted"),
    [
        (
            "こんにちは",
            RobotEvent.CONFIRM_INPUT,
            "こんにちは"
        ),
        (
            "",
            RobotEvent.EMPTY_INPUT,
            ""
        ),
        (
            "   ",
            RobotEvent.EMPTY_INPUT,
            ""
        ),
        (
            "　",
            RobotEvent.EMPTY_INPUT,
            ""
        ),
    ]
)
def test_on_listening(
    monkeypatch: MonkeyPatch,
    input_text: str,
    excepted_event: RobotEvent,
    excepted: str,
) -> None:
    monkeypatch.setattr(
        "builtins.input",
        lambda _: input_text
    )
    state = RobotState.LISTENING
    user_name = "test"

    event, request = on_listening(state, user_name)

    assert event == excepted_event
    assert request == excepted

@pytest.mark.parametrize(
    ("req", "excepted_event", "excepted_text", "excepted_memories"),
    [
        (
            "こんにちは", 
            RobotEvent.REPLY_READY, 
            "こんにちは！", 
            [
                "僕は、日大生です。"
            ]
        ),
        (
            "僕は、21歳です。", 
            RobotEvent.REPLY_READY, 
            "覚えておくね。", 
            [
                "僕は、日大生です。",
                "僕は、21歳です。",
            ]
        ),
        (
            "僕は、日大生です。",
            RobotEvent.REPLY_READY,
            "それは前に聞いたよ。",
            [
                "僕は、日大生です。",
            ]
        ),
    ]
)
def test_on_thinking(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    req: str,
    excepted_event: RobotEvent,
    excepted_text: str,
    excepted_memories: list[str]
) -> None:
    # monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    memories = [
        "僕は、日大生です。"
    ]
    local_memory_path(user_name).parent.mkdir(parents=True)
    state = RobotState.THINKING

    event, text, memories = on_thinking(state, req, user_name, memories)

    assert event == excepted_event
    assert text == excepted_text
    assert memories == excepted_memories

    excepted_memory_path = {
        "name": user_name,
        "memories": excepted_memories
    }
    assert read_user_local_json(user_name) == excepted_memory_path

def test_create_json_folder(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    create_json_folder(user_name)

    assert local_memory_path(user_name).parent.exists()


@pytest.mark.parametrize(
    ("default_memories", "search_keywords", "delete_queries", "expected_memories"),
    [
        (
            [
                "僕の学校では、明日に期末テストです。",
                "私の期末テストは、来週です。",
                "犬です。わんわん",
                "おはよう",
            ],
            ["明日", "期末"],
            [
                "僕の学校では、明日に期末テストです。",
            ],
            [
                "私の期末テストは、来週です。",
                "犬です。わんわん",
                "おはよう",
            ],
        ),
        (
            [
                "犬です。わんわん",
                "おはよう",
            ],
            ["明日", "期末"],
            [
                
            ],
            [
                "犬です。わんわん",
                "おはよう",
            ],
        )
    ]
)
def test_on_delete(
    default_memories: list[str],
    search_keywords: list[str],
    delete_queries: list[str],
    expected_memories: list[str],
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True, exist_ok=True)
    default_data = {
        "name": user_name,
        "memories": default_memories
    }
    write_user_local_json(user_name, default_data)

    search_results = search_memory(default_memories, search_keywords)
    assert search_results == delete_queries
    remaining_memories = on_delete(default_memories, delete_queries, user_name)

    expected_data = {
        "name": user_name,
        "memories": expected_memories
    }

    assert read_user_local_json(user_name) == expected_data
    assert remaining_memories == expected_memories


def test_on_thinking_delete_no_matches(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,

) -> None:
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)

    request = "明日 期末を削除して"
    default = {
        "name": user_name,
        "memories": ["犬です。わんわん", "おはよう"]
    }

    write_user_local_json(user_name, default)

    event, text, memories = on_thinking(
        RobotState.THINKING,
        request,
        user_name,
        default["memories"]
    )

    assert event == RobotEvent.REPLY_READY
    assert text == "明日 期末は見つかりませんでした。"
    assert memories == default["memories"]
    assert read_user_local_json(user_name) == default

def test_on_thinking_delete_one_match(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)

    default = {
        "name": user_name,
        "memories": ["犬です。わんわん", "おはよう", "僕は、明日期末テストがあります。"]
    }
    request = "明日 期末を削除して"
    write_user_local_json(user_name, default)
    event, text, memories = on_thinking(
        RobotState.THINKING,
        request,
        user_name,
        default["memories"]
    )


    assert event == RobotEvent.REPLY_READY
    assert text == "明日 期末を削除しました。"
    assert memories == ["犬です。わんわん", "おはよう"]
    expected_data = {
        "name": user_name,
        "memories": ["犬です。わんわん", "おはよう"]
    }
    assert read_user_local_json(user_name) == expected_data

def test_on_thinking_delete_multiple_matches(
    monkeypatch: MonkeyPatch,
    tmp_path: Path
) -> None:
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True)

    default = {
        "name": user_name,
        "memories": ["犬です。わんわん", "おはよう", "僕は、明日に期末テストがあります。", "僕にとっては、明日の期末テストのやまは数学ですね。"]
    }
    request = "明日 期末を削除して"
    write_user_local_json(user_name, default)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    event, text, memories = on_thinking(
        RobotState.THINKING,
        request,
        user_name,
        default["memories"]
    )

    assert event == RobotEvent.REPLY_READY
    assert text == "明日 期末を削除しました。"
    assert memories == ["犬です。わんわん", "おはよう","僕は、明日に期末テストがあります。"]
    expected_data = {
        "name": user_name,
        "memories": ["犬です。わんわん", "おはよう", "僕は、明日に期末テストがあります。"]
    }
    assert read_user_local_json(user_name) == expected_data

### 元の記憶、削除対象、出力の期待値
@pytest.mark.parametrize(
    ("default_data", "keywords", "delete_queries", "expected_data"),
    [
        (
            {
                "name": "test",
                "memories": [
                    "僕は、期末テストです",
                    "僕は、期末テストです。明日は数学です。",
                    "僕は、猫が好きです。"
                ]
            },
            ["期末", "テスト"],
            [
                "僕は、期末テストです",
                "僕は、期末テストです。明日は数学です。",
            ],
            {
                "name": "test",
                "memories": [
                    "僕は、期末テストです。明日は数学です。",
                    "僕は、猫が好きです。"
                ]
            }
        )
    ]
)
# 似た記憶2件の中から、１件のみを選択して、消すテスト
def test_selected_memories(
    monkeypatch: MonkeyPatch, 
    tmp_path: Path,
    default_data: dict[str, str | list[str]],
    keywords: list[str],
    delete_queries: list[str],
    expected_data: dict[str, str | list[str]],
) -> None :
    monkeypatch.setenv("MEMORY_INDEX_DIR", str(tmp_path))
    user_name = "test"
    local_memory_path(user_name).parent.mkdir(parents=True, exist_ok=True)

    write_user_local_json(user_name, default_data)

    search_results = search_memory(default_data["memories"], keywords)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    assert search_results == delete_queries

    selected_query = on_selected_data(search_results)
    remaining_memories = on_delete(
        default_data["memories"],
        selected_query,
        user_name
    )
    assert remaining_memories == expected_data["memories"]

    assert read_user_local_json(user_name) == expected_data