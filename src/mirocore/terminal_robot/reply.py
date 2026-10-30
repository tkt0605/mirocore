import json
from pathlib import Path
from mirocore.terminal_robot.write_read import (
    local_memory_path,
    read_user_local_json,
    write_user_local_json,
    user_local_file_exists,
)

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

## 発言から記憶するk候補を引き出す関数
# 返信を作る前に、今の発言だけを見る純粋な関数を置きます
# 返すのは、覚えておく文か None です。ファイルも辞書も触りません
# 最初の規則は狭くてよく、たとえば「僕は、男です。」のように、ユーザーが自分について述べた文だけを候補
def propose_memory(request: str) -> str | None:
    ## 最初の規則は狭くてよく、たとえば「僕は、男です。」のように、ユーザーが自分について述べた文だけを候補
    target_words = ["僕", "私", "俺", "自分", "自分自身", "私自身"]
    for word in target_words:
        if word in request:
            return request
    return None

## 記憶の追加・更新
# 候補があるときだけ、ループが持っているリストを更新
# 空や、すでに同じ文があるときはリストを変更しない。
# 戻り値は、更新されたリストを返す。
def add_memory(memories: list[str], item: str) -> list[str]:
    if item is None or item == "":
        return memories
    
    if item in memories:
        return memories
    ## itemをリストに追加
    memories.append(item)
    ## リストを返す
    return memories


## 現発言のキーワード取得用の関数
## 入力：発言内容
## 出力：一番左の語句、またはNone
# 正規化された文書の全てみてから、キーワードを返す関数
def reply_phrase(request: str) -> str | None:
    normalized_req = normalize(request)
    best_key: str | None = None
    best_position_key: int | None = None

    for key in _REPLY_KEYWORDS_INDEX:
        position = normalized_req.find(key)
        ## キーワードが見つからなかった場合は、次のキーワードを検索
        if position == -1:
            continue
        ## キーワードが見つかった場合は、
        if best_position_key is None or position < best_position_key:
            ## 辞書におけるキーワードの決定
            best_key = key
            ## キーワードの位置の決定
            best_position_key = position
    ## 辞書におけるキーワードを返す。
    return best_key

## 応答生成用の関数
## 入力：発言内容、ユーザー名、記憶内容
## 出力：応答内容
def reply_to_greeting(request: str, user_name: str) -> str | None:
    phrase = reply_phrase(request)

    if phrase is None or phrase == "":
        return f"{user_name}さん、ごめんね。もう一度聞いてくれる？"
    body = _REPLY_KEYWORDS_INDEX.get(phrase)
    return f"{body}"
## 自己紹介、新規記憶追加用の関数
# input: 新規記憶かどうか
# output: 応答内容
def reply_to_self_introduction(is_new: bool) -> str | None:
    if is_new:
        return "覚えておくね。"
    return "それは前に聞いたよ。"

## 記憶の選定
## 入力：記憶内容、ユーザー名
## 出力：検索対象のデータ

def search_memory(memories: list[str], query: str) -> list[str]:
    response: list[str] = []
    if query is None or query == "":
        return response
    
    for memory in memories:
        if query in memory:
            response.append(memory)
    return response
