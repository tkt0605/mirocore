from mirocore.terminal_robot.reply import (
    reply_to_greeting,
    normalize,
    reply_remember,
    reply_phrase,
    _REPLY_KEYWORDS_INDEX,
    propose_memory,
    add_memory,
    reply_to_self_introduction,
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
        assert reply_to_greeting(request, user_name) == f"{response}"

def test_normalize_function() -> None:
    for request, normalized in zip(request_normalized_lists, request_lists):
        assert normalize(request) == normalized

def test_reply_function_with_fallback() -> None:
    user_name = "テスト"
    for unmatched in unmatched_lists:
        assert reply_to_greeting(unmatched, user_name) == f"{user_name}さん、ごめんね。もう一度聞いてくれる？"

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

def test_propose_memory_function() -> str | None:
    inputs = [
        ("僕は、男です。", "僕は、男です。"),
        ("私は、女です。", "私は、女です。"),
        ("自分自身は、男です。", "自分自身は、男です。"),
        ("隆人は、女です。", None),
    ]

    for request, expected in inputs:
        assert propose_memory(request) == expected


@pytest.mark.parametrize(
    ("item", "excepted"),
    [
        (
            "俺は、男です。",
            [
                "僕は、男です。", 
                "私は、女です。", 
                "俺は、男です。"
            ]
        ),
        (
            "私は、女です。",
            [
                "僕は、男です。",
                "私は、女です。"
            ]
        ),
        (
            "",
            [
                "僕は、男です。",
                "私は、女です。"
            ]
        ),
    ]
)
def test_add_memory_function(item: str, excepted: list[str]) -> None:
    memories = [
        "僕は、男です。",
        "私は、女です。"
    ]
    result = add_memory(memories, item)
    
    assert result is memories
    assert result == excepted

def test_reply_to_self_introduction_function() -> str:
    is_new = True
    assert reply_to_self_introduction(is_new) == "覚えておくね。"
    is_new = False
    assert reply_to_self_introduction(is_new) == "それは前に聞いたよ。"
