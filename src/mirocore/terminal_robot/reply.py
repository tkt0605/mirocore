_REPLY_KEYWORDS_INDEX: dict[str, str] = {
    "こんにちは": "こんにちは！",
    "おはよう": "おはようございます！",
    "こんばんは": "こんばんは！",
    "お疲れ様": "お疲れ様です！",
    "疲れた": "ゆっくり休んでください！",
}

def reply(request: str) -> str:
    return _REPLY_KEYWORDS_INDEX.get(request, "ごめんね。もう一度聞いてくれる？")