## ターミナル・ボットのみのテストファイル
from _pytest.assertion.rewrite import AssertionRewriter
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.__main__ import main
from mirocore.terminal_robot.expressive import add_prefix
from unittest.mock import Mock
import pytest

user_name = ""
# テスト用の一言テスト

## 初期条件から、名前を入力して永続化したかどうか
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
def test_empty_name_and_quit(monkeypatch, capsys) -> None:
    user_name = "テスト"
    answers = iter([user_name, "", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    main()
    out = capsys.readouterr()
    assert f"MIROC(・o・) > {user_name}さん空白です。もう一度聞いてください。" in out.out
    assert "終了します。" in out.out


# ## requestのinput関数に`Ctrl + C`を入力すると終了するかどうか
def test_ctrl_c_and_quit(monkeypatch, capsys) -> None:
    ## キーボードインタラプトを発生させるためのモック関数
    def interrupted(_prompt: str) -> str:
        raise KeyboardInterrupt
    ### モック関数を設定
    monkeypatch.setattr(
        "builtins.input",
        interrupted
    )
    ### メイン関数を実行
    main()
    ### 出力を確認
    out = capsys.readouterr()

    assert "終了します。" in out.out