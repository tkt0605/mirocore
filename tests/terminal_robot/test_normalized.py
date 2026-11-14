import pytest
from mirocore.terminal_robot.normalized import (
    delete_memory,
    extract_delete_target,
)

@pytest.mark.parametrize(
    ("utterance", "expected"),
    [
        ("犬が好きを削除して", "犬が好き"),
        ("犬が好きを削除してください", "犬が好き"),
        ("筋トレは達成ずみ", "筋トレ"),
        ("削除して", None),
        ("こんにちは", None),
    ]
)
def test_extract_delete_target(utterance: str, expected: str | None) -> None:
    assert extract_delete_target(utterance) == expected

def test_delete_memory_removes_every_match() -> None:
    memories = [
        "犬が好きです。",
        "犬が好き、散歩も好き。",
        "猫が好きです。",
    ]
    result = delete_memory(memories, "犬が好きを削除して")

    assert result == ["猫が好きです。"]

    assert memories == [
        "犬が好きです。",
        "犬が好き、散歩も好き。",
        "猫が好きです。",
    ]

@pytest.mark.parametrize(
    "query",
    [
        "",
        "削除して",
        "こんにちは",
        "教えて"
    ]
)
def test_delete_memory_keeps_original_list(query: str) -> None:
    memories = [
        "犬が好きです。",
    ]
    assert delete_memory(memories, query) == memories

