from mirocore.terminal_robot.write_read import (
    local_memory_path,
    read_user_local_json,
)
from mirocore.terminal_robot.options import (
    terminal_robot_state,
    on_listening,
    on_thinking,
    create_json_folder
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
def test_terminal_robot_state() -> None:
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    exceptted_state = RobotState.LISTENING

    assert terminal_robot_state(state, event) == exceptted_state

    state = RobotState.ERROR
    event = RobotEvent.ERROR_SHOWN
    exceptted_error_state = RobotState.IDLE
    assert terminal_robot_state(state, event) == exceptted_error_state

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
            "こんにちは!", 
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
    monkeypatch.chdir(tmp_path)
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