## ターミナル・ボットのみのテストファイル
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.__main__ import main
from unittest.mock import Mock
import pytest

# テスト用の一言テスト

## 初期条件から、名前を入力して永続化したかどうか
def test_bot_name_and_quit(monkeypatch) -> None:
    answers = iter(["太郎"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    
    main()

## transition関数のテスト
def test_transition_function() -> None:
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING

    state = transition(state, event)
    assert state == RobotState.LISTENING
    excepted_event = RobotEvent.CONFIRM_INPUT
    state = transition(state, excepted_event)
    assert state == RobotState.THINKING

## 空文字 "" も終了し、「こんにちは、名前さん」は出ず、IDLE状態に戻るかどうか

## requestのinput関数に`/q, /quit, /exit`を入力すると終了するかどうか


## requestのinput関数に`Cntl + C`を入力すると終了するかどうか
