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
## 正規化用の関数
def normalize(request: str) -> str:
    text = request.strip().replace("\u3000", "").replace(" ", "")
    for mark in _TARGET_NORMALIZATION:
        text = text.replace(mark, "")
    return text

## 記憶機能用の関数
## 入力：記憶内容
## 出力：使う文書か、記憶なしかを返す
def reply_remember(memory: str | None) -> str | None:
    if memory is None or memory == "":
        return None
    return memory

## 現発言のキーワード取得用の関数
## 入力：発言内容
## 出力：一番左の語句、またはNone
def reply_phrase(request: str) -> str | None:
    normalized_req = normalize(request)
    for key in _REPLY_KEYWORDS_INDEX:
        position = normalized_req.find(key)
        if position != -1:
            return normalized_req[position:position + len(key)]
    return None

## 応答生成用の関数
## 入力：発言内容、ユーザー名、記憶内容
## 出力：応答内容
def reply(request: str, user_name: str, memory: str | None) -> str | None:
    phrase = reply_phrase(request)
    remember = reply_remember(memory)

    if phrase is None or phrase == "":
        return f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
    body = _REPLY_KEYWORDS_INDEX.get(phrase)
    if remember is None:
        return body
    else:
        return f"{remember} {body}"