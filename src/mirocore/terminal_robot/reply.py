"""応答生成用のモジュール"""
_REPLY_KEYWORDS_INDEX: dict[str, str] = {
    "こんにちは": "こんにちは!",
    "おはよう": "おはようございます!",
    "こんばんは": "こんばんは!",
    "お疲れ様": "お疲れ様です!",
    "疲れた": "ゆっくり休んでください!",
}

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
## 正規化用の関数
def normalize(request: str) -> str:
    text = request.strip().replace("\u3000", "").replace(" ", "")
    for mark in _TARGET_NORMALIZATION:
        text = text.replace(mark, "")
    return text
## 応答生成用の関数
def reply(request: str, user_name: str) -> str:
    key = normalize(request)
    return _REPLY_KEYWORDS_INDEX.get(key, f"{user_name}さん、ごめんね。もう一度聞いてくれる？")
    # return _REPLY_KEYWORDS_INDEX.get(request, "ごめんね。もう一度聞いてくれる？") 