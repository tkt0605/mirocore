from mirocore.terminal_robot.normalized import (
    normalize,
    _REPLY_KEYWORDS_INDEX,
)
from mirocore.terminal_robot.reply import (
    reply_to_greeting,
    reply_remember,
    reply_phrase,
    propose_memory,
    add_memory,
    reply_to_self_introduction,
)
import pytest

user_name = ""
@pytest.mark.parametrize(
    ("_request", "response"),
    [
        ("こんにちは", "こんにちは！"),
        ("こんばんは", "こんばんは！"),
        ("おはよう", "おはようございます！"),
        ("疲れた", "ゆっくり休んでください！"),
        ("お疲れ様", "お疲れ様です！"),
    ]
)
def test_reply_function(_request: str, response: str) -> None:
    user_name = "テスト"
    assert reply_to_greeting(_request, user_name) == response

@pytest.mark.parametrize(
    ("normalized_request", "normalized_expected"),
    [
        ("こ んにちは", "こんにちは"),
        ("こ　んばんは", "こんばんは"),
        ("おはよう！", "おはよう"),
        ("疲れた！", "疲れた"),
        ("お疲れ様、・。", "お疲れ様"),
    ]
)
def test_normalize_function(normalized_request: str, normalized_expected: str) -> None:
    assert normalize(normalized_request) == normalized_expected

@pytest.mark.parametrize(
    ("unmatched", "expected"),
    [
        ("Hi", "テストさん、ごめんね。もう一度聞いてくれる？"),
        ("Hello", "テストさん、ごめんね。もう一度聞いてくれる？"),
        ("Good evening", "テストさん、ごめんね。もう一度聞いてくれる？"),
        ("Good morning", "テストさん、ごめんね。もう一度聞いてくれる？"),
        ("Good night", "テストさん、ごめんね。もう一度聞いてくれる？"),
    ]
)
def test_reply_function_with_fallback(unmatched: str, expected: str) -> None:
    user_name = "テスト"
    assert reply_to_greeting(unmatched, user_name) == f"{expected}"

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
