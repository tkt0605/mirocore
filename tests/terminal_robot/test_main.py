## ターミナル・ボットのみのテストファイル
from _pytest.assertion.rewrite import AssertionRewriter
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.__main__ import main
from mirocore.terminal_robot.expressive import add_prefix
from unittest.mock import Mock
from mirocore.terminal_robot.options import inputer_user_name
from pathlib import Path
import pytest

from mirocore.terminal_robot.write_read import read_user_local_json, write_user_local_json

user_name = ""
# テスト用の一言テスト

## 状態遷移の関係をまとめた表をパラメータ化
@pytest.mark.parametrize(
    ("state", "event", "expected_state"),
    [
        (RobotState.IDLE, RobotEvent.START_LISTENING, RobotState.LISTENING),
        (RobotState.LISTENING, RobotEvent.CONFIRM_INPUT, RobotState.THINKING),
        (RobotState.THINKING, RobotEvent.REPLY_READY, RobotState.SPEAKING),
        (RobotState.SPEAKING, RobotEvent.OUTPUT_DONE, RobotState.IDLE),
        (RobotState.ERROR, RobotEvent.ERROR_SHOWN, RobotState.IDLE),
        (RobotState.LISTENING, RobotEvent.EMPTY_INPUT, RobotState.EMPTY),
        (RobotState.EMPTY, RobotEvent.START_LISTENING, RobotState.LISTENING),
    ],
)
## transition関数の
def test_transition_function(state: RobotState, event: RobotEvent, expected_state: RobotState) -> None:
    assert transition(state, event) == expected_state

def tmp_path_example(tmp_path) -> None:
    file_path = tmp_path / "example.txt"
    file_path.write_text("Hello World To Test Code !", encoding="utf-8")
    assert file_path.read_text(encoding="utf-8") == "Hello World To Test Code !"

## 空文字 "" も終了し、「こんにちは、名前さん」は出ず、IDLE状態に戻るかどうか
def test_empty_name_and_quit(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    
    mock_input = Mock(
        side_effect=[
            "テスト",
            "",
            "/q"
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        mock_input
    )
    main()

    out = capsys.readouterr()

    assert "MIROC(•‿•) > テストさん、待ってるよ" in out.out
    assert "MIROC(・o・) > テストさん空白です。もう一度聞いてください。" in out.out
    assert "終了します。" in out.out
    assert mock_input.call_count == 3


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

# ## requestのinput関数に`Ctrl + C`を入力すると終了するかどうか
def test_listening_ctrl_c_and_quit(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)

    mock_input = Mock(
        side_effect=[
            "テスト",
            KeyboardInterrupt()
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        mock_input
    )

    main()

    out = capsys.readouterr()
    assert "MIROC(•‿•) > テストさん、待ってるよ" in out.out
    assert "終了します。" in out.out

    assert mock_input.call_count == 2

## 確認文 名前 が出ること
def test_username_is_exists(monkeypatch, capsys, tmp_path) -> None:
    answers = iter(["テスト", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    monkeypatch.chdir(tmp_path)
    user_name, memories = inputer_user_name()
    assert user_name is not None
    assert user_name == "テスト"
    assert memories == []

## 空の名前で 名前が必要です。 と出て、再入力できること
def test_username_is_empty(monkeypatch, capsys, tmp_path) -> None:
    answers = iter(["", "テスト"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    monkeypatch.chdir(tmp_path)
    
    user_name, memories = inputer_user_name()
    assert user_name is not None

    out = capsys.readouterr()
    assert "名前が必要です。" in out.out
    assert user_name == "テスト"
    assert memories == []

##  保存済みの記憶を持つユーザーで、記憶本文を正しく読み戻せるか
def test_user_has_memories(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "テスト"
    write_user_local_json(
        user_name,
        {
            "name": user_name,
            "memories": [
                "僕は、ロボットが大好きです。"
            ]
        }
    )

    answers = iter(["テスト", "/q"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )
    user_name, read_memories = inputer_user_name()

    assert user_name is not None

    assert read_memories == ["僕は、ロボットが大好きです。"]
    assert user_name == "テスト"


## 2回目以降の発言でも同じ名前が使われ、名前を聞き直さないこと
def test_username_is_same(monkeypatch, capsys, tmp_path) -> None:
    answers = iter(["test", "こんにちは", "おはよう", "/q"])
    # ある場所の属性を別のものに置き換える。
    monkeypatch.setattr(
        # python組み込み型のinput関数のモック
        "builtins.input",
        # モック関数
        lambda _: next(answers)
    )
    monkeypatch.chdir(tmp_path)
    ## main()関数内にもinputer_user_nameがあるからわざわざもう一回inputer_user_nameを呼ぶ必要はない
    main()
    out = capsys.readouterr()
    assert out.out.count("MIROC(•‿•) > testさん、待ってるよ") == 3
    assert out.out.count("MIROC(•_•) > testさん、考え中です。少々お待ち下さい。") == 2
    assert "終了します。" in out.out

## 名前入力中の Ctrl+C で 待ってるよ が出ず、input() が1回で終わること
def test_username_is_ctrl_c(monkeypatch, capsys) -> None:
    called = 0

    def interrupted(_prompt: str) -> str:
        nonlocal called
        called += 1
        raise KeyboardInterrupt
    
    monkeypatch.setattr(
        "builtins.input",
        interrupted
    )
    main()
    out = capsys.readouterr()
    
    assert called == 1
    assert "待ってるよ" not in out.out
    assert "あなたの名前は、" not in out.out
    assert "終了します。" in out.out


## 記憶を追加した後、検索を仕掛けてその出力と、記憶追加した出力が合致するかどうか。
def test_memory_survives_restart_and_is_searched(
    monkeypatch,
    capsys,
    tmp_path
) -> None:
    monkeypatch.chdir(tmp_path)
    user_name = "テスト"
    ## 　1回目：　名前を入力し、記憶を追加
    first_input = Mock(
        side_effect=[
            user_name,
            "僕の趣味は、読書です。",
            "/q"
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        first_input
    )
    main()
    capsys.readouterr()

    ## 中間：　ファイルに保存されているのかどうかの確認　
    data = read_user_local_json(user_name)

    assert data is not None

    assert data["name"] == user_name
    assert data["memories"] == ["僕の趣味は、読書です。"]

    ## 2回目: 検索を仕掛けて、記憶追加した出力と合致するかどうかの確認
    second_input = Mock(
        side_effect=[
            user_name,  
            "趣味について教えて",
            "/q"
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        second_input
    )
    main()

    out = capsys.readouterr()

    assert "MIROC(•‿•) > テストさん、待ってるよ" in out.out
    assert "MIROC(•_•) > テストさん、考え中です。少々お待ち下さい。" in out.out
    assert "僕の趣味は、読書です。" in out.out
    assert "終了します。" in out.out

    ### 3回目: 検索後のJSONも確認
    data_after_search = read_user_local_json(user_name)

    assert data_after_search is not None

    assert data_after_search["name"] == user_name
    assert data_after_search["memories"] == ["僕の趣味は、読書です。"]
