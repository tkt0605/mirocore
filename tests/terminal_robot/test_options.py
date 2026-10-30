from mirocore.terminal_robot.write_read import (
    local_memory_path,
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

def test_terminal_robot_state() -> None:
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    exceptted_state = RobotState.LISTENING

    assert terminal_robot_state(state, event) == exceptted_state

    state = RobotState.ERROR
    event = RobotEvent.ERROR_SHOWN
    exceptted_error_state = RobotState.IDLE
    assert terminal_robot_state(state, event) == exceptted_error_state

def test_on_listening(monkeypatch: MonkeyPatch) -> None:
    input_text = iter(["こんにちは", "", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(input_text)
    )
    user_name = "test"
    state = RobotState.LISTENING
    event, request = on_listening(state, user_name)

    assert event == RobotEvent.CONFIRM_INPUT
    assert request == "こんにちは"

    event, request = on_listening(state, user_name)

    assert event == RobotEvent.EMPTY_INPUT
    assert request == ""

def test_on_thinking_to_greeting(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    request = "こんにちは"
    user_name = "test"
    memories: list[str] = []
    state = RobotState.THINKING

    local_memory_path(user_name).parent.mkdir(parents=True)

    event, text, memories = on_thinking(state, request, user_name, memories)
    
    assert event == RobotEvent.REPLY_READY
    assert text == "こんにちは!"
    assert memories == []

def test_on_thinking_to_self_introduction(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    request = "僕は、日大生です。"
    local_memory_path(user_name).parent.mkdir(parents=True)
    state = RobotState.THINKING
    memories: list[str] = []
    event, text, memories = on_thinking(state, request, user_name, memories)
    assert event == RobotEvent.REPLY_READY
    assert text == "覚えておくね。"
    assert memories == [request] 

def test_create_json_folder(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "test"
    create_json_folder(user_name)

    assert local_memory_path(user_name).parent.exists()