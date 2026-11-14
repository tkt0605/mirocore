import pytest
from mirocore.terminal_robot.search import (
    extract_query, 
    search_memory,
    extract_search_keywords
)

@pytest.mark.parametrize(
    ("utterance", "expected"),
    [
        ("犬が好きを教えて！", "犬が好き"),
        ("僕の犬が好きについて覚えていますか？", "犬が好き"),
        ("A B Cを教えてください", "a b c"),
        ("教えて", None),
        ("こんにちは", None),
        ("面談について　教えて", "面談"),
        ("明日 面談を教えて", "明日 面談"),
        ("明日　面談　を　教えて", "明日 面談"),
    ]
)
def test_extract_query(utterance: str, expected: str | None) -> None:
    assert extract_query(utterance) == expected

def test_search_memory_normalizes_both_sides() -> None:
    memories = [
        "ＡＢＣが好き。",
        "猫が好き。",
        "犬が好き、猫も好き",
    ]

    keywords = [
        "猫",
        "犬",
    ]
    assert search_memory(memories, ["abc"]) == ["ＡＢＣが好き。"]
    assert search_memory(memories, keywords) == ["犬が好き、猫も好き",]
    assert search_memory(memories, [""]) == []
    assert search_memory(memories, ["!!!"]) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("明日 面談", ["明日", "面談"]),
        ("明日　面談", ["明日", "面談"]),
        ("犬が好き", ["犬が好き"]),
        ("猫が好き", ["猫が好き"]),
        ("犬が好き、猫も好き", ["犬が好き猫も好き"]),
        ("", []),
    ]
)
def test_extract_search_keywords(text: str, expected: list[str]) -> None:
    assert extract_search_keywords(text) == expected
