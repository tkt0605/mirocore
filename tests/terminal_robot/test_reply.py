from mirocore.terminal_robot.reply import reply, normalize
import pytest

request_lists = [
    "こんにちは",
    "こんばんは",
    "おはよう",
    "疲れた",
    "お疲れ様",
]

request_normalized_lists = [
    "こ んにちは",
    "こ　んばんは",
    "おはよう!",
    "疲れた！",
    "お疲れ様、・。",
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

user_name = ""

def test_reply_function() -> None:
    user_name = "テスト"
    for request, response in zip(request_lists, response_lists):
        assert reply(request, user_name) == response

def test_normalize_function() -> None:
    for request, normalized in zip(request_normalized_lists, request_lists):
        assert normalize(request) == normalized

def test_reply_function_with_fallback() -> None:
    user_name = "テスト"
    for unmatched in unmatched_lists:
        assert reply(unmatched, user_name) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
