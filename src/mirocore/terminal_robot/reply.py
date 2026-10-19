


"""応答生成用のモジュール"""
_REPLY_KEYWORDS_INDEX: dict[str, str] = {
    "こんにちは": "こんにちは!",
    "おはよう": "おはようございます!",
    "こんばんは": "こんばんは!",
    "お疲れ様": "お疲れ様です!",
    "疲れた": "ゆっくり休んでください!",
}

## 正規化用の関数
def normalize(request: str) -> str:
    text = request.strip().replace("\u3000", "")
    for mark in "！!？。?,、":
        text = text.replace(mark, "")
    return text
## 応答生成用の関数
def reply(request: str) -> str:
    key = normalize(request)
    return _REPLY_KEYWORDS_INDEX.get(key, "ごめんね。もう一度聞いてくれる？")
    # return _REPLY_KEYWORDS_INDEX.get(request, "ごめんね。もう一度聞いてくれる？")