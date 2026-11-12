"""応答生成用のモジュール"""
_REPLY_KEYWORDS_INDEX: dict[str, str] = {
    "こんにちは": "こんにちは!",
    "おはよう": "おはようございます!",
    "こんばんは": "こんばんは!",
    "お疲れ様": "お疲れ様です!",
    "疲れた": "ゆっくり休んでください!",
}

"""個人記憶用のモジュール"""
# _KEYWORD_
_TARGET_NORMALIZATION: list[str] = [
    "！",
    "!",
    "？",
    "?",
    ".",
    ",",
    "、",
    "。",
    "・",
]

_TARGET_NORMALIZATION_WORDS: list[str] = [
    "僕の",
    "を覚えてる",
    "を覚えてるか",
    "を覚えてますか",
    "を教えて",
    "を教えてください",
    "について覚えてる",
    "について覚えてるか",
    "について覚えてますか",
    "について教えて",
    "について教えてください",
    "覚えてる",
    "覚えてるか",
    "覚えてますか",
    "教えて",
    "教えてください"
]
_TARGET_DELETE_WORDS: list[str] = [
    "を削除して",
    "を消去して",
    "は達成済み",
    "は達成完了",
    "は完了した",
]

def normalize_word(request: str) -> str | None:
    text = request.strip().replace("\u3000", "").replace(" ", "")
    for word in _TARGET_NORMALIZATION_WORDS:
        if text.endswith(word):
            query = text.removesuffix(word)
            return query if query != "" else None
    return None
## 正規化用の関数
def normalize(request: str) -> str:
    text = request.strip().replace("\u3000", "").replace(" ", "")
    for mark in _TARGET_NORMALIZATION:
        text = text.replace(mark, "")
    return text

# 削除用の正規化関数
def normalized_delete_req(request: str) -> str | None:
    for word in _TARGET_DELETE_WORDS:
        if request.endswith(word):
            target = request.removesuffix(word).strip()
            return target if target else None
    return None
