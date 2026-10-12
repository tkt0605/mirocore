## ターミナル・ボットのみのテストファイル
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.__main__ import main
from unittest.mock import Mock
import pytest

# テスト用の一言テスト

## 初期条件から、名前を入力して永続化したかどうか
def test_bot_name_and_quit(monkeypatch, capsys) -> None:
    answers = iter(["太郎", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )

    main()

    out = capsys.readouterr()
    assert "こんにちは、太郎さん" in out.out
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
    answers = iter(["", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    main()
    out = capsys.readouterr()
    assert "===================================" in out.out
    assert "@@ 空文字では誰かはわかりません @@" in out.out
    assert "===================================" in out.out


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