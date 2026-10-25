from mirocore.terminal_robot.reply import (
    reply,
    normalize,
    reply_remember,
    reply_phrase,
    _REPLY_KEYWORDS_INDEX
)
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
    "Hi",
    "Hello",
    "Good evening",
    "Good morning",
    "Good night",
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
        assert reply(request, user_name, None) == f"{response}"
        ## ここで、記憶を追加して、再びテストを実行
        memory = "僕は、男です。"
        assert reply(request, user_name, memory) == f"{memory} {response}"
        ## ここで、memoryを空文字にして、再びテストを実行
        memory = ""
        assert reply(request, user_name, memory) == f"{response}"

def test_normalize_function() -> None:
    for request, normalized in zip(request_normalized_lists, request_lists):
        assert normalize(request) == normalized

def test_reply_function_with_fallback() -> None:
    user_name = "テスト"
    for unmatched in unmatched_lists:
        assert reply(unmatched, user_name, None) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
        ## ここで、記憶を追加して、再びテストを実行
        memory = "僕は、男です。"
        assert reply(unmatched, user_name, memory) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
        ## ここで、memoryを空文字にして、再びテストを実行
        memory = ""
        assert reply(unmatched, user_name, memory) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
        ## ここで、memoryを英語にして、再びテストを実行
        memory = "I am a boy."
        assert reply(unmatched, user_name, memory) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"

def test_reply_remember_function() -> None:
    assert reply_remember(None) is None
    assert reply_remember("") is None

    context = "Hi"
    assert reply_remember(context) == "Hi"

def test_reply_phrase_function() -> None:
    assert reply_phrase("Hi") is None
    input_lists = [
        "こんにちは",
        "今日は疲れた",
        "おはよう！",
        "こんにちは、今日は疲れた。",
        "疲れた、こんにちは",
    ]
    output_lists = [
        "こんにちは",
        "疲れた",
        "おはよう",
        "こんにちは",
        "疲れた",
    ]

    for input, output in zip(input_lists, output_lists):
        assert reply_phrase(input) == output