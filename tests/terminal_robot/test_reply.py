from mirocore.terminal_robot.reply import reply, normalize
import pytest

request_lists = [
    "こんにちは",
    "こんばんは",
    "おはよう",
    "疲れた",
    "お疲れ様",
]

unmatched_lists = [
    "今日はこんにちは",
    "今日はこんばんは",
    "今日はおはよう",
    "今日は疲れた",
    "今日はお疲れ様",
]

response_lists = [
    "こんにちは!",
    "こんばんは!",
    "おはようございます!",
    "ゆっくり休んでください!",
    "お疲れ様です!",
]

def test_reply_function() -> None:
    for request, response in zip(request_lists, response_lists):
        assert reply(request) == response

def test_reply_function_with_fallback() -> None:
    for unmatched in unmatched_lists:
        assert reply(unmatched) == "ごめんね。もう一度聞いてくれる？"

def test_normalize_function() -> None:
    assert normalize("こんにちは！") == "こんにちは"
    