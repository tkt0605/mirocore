"""
正規化用の関数をまとめたファイル

今回、正規化関数を作成してはいたが、かなり稚拙なものである。
そこで、cursorに作成してもらったものを、自分で見よう見真似で書く。

今回の目的は、ただAIに推奨してもらったコードをただ写すのではなく、
自分の力にまでに落とし込むことを目標にして設計する。

"""
import re
import unicodedata

_REPLY_KEYWORDS_INDEX: dict[str, str] = {
    "こんにちは": "こんにちは！",
    "おはよう": "おはようございます！",
    "おやすみ": "おやすみなさい！",
    "ありがとう": "どういたしまして！",
    "すみません": "大丈夫です！",
    "ごめんなさい": "大丈夫です！",
    "こんばんは": "こんばんは！",
    "さようなら": "さようなら！",
    "お疲れ様": "お疲れ様です！",
    "疲れた": "ゆっくり休んでください！",
}

# NKFC後も残る句読点と、変換まえの全角形の両方を除く
_PUNCTUATION: tuple[str, ...] = (
    "！",
    "？",
    "。",
    "、",
    "・",
    "：",
    "；",
    "?",
    "!",
    ",",
)

_SPEAKER_PREFIXES: tuple[str, ...] = (
    "僕の",
    "私の",
    "あなたの",
)
_QUERY_SUFFIX = re.compile(
    r"(?:について|を)?\s*"
    r"(?:について|を)?(?:覚えて(?:る|いる|ます|います)か?|教えて(?:ください)?)$"
)
_DELETE_SUFFIX = re.compile(
    r"(?:は|を)?\s*"
    r"(?:(?:を|は)?(?:削除|消去|消)して(?:ください)?"
    r"|は(?:達成済み|達成ずみ|達成した|達成済|達成完了|完了した|終了した))$"
)

## 正規化前の共通の下処理
def normalize_preserving_spaces(text: str) -> str:
    """表記を揃え、指定した句読点を除く。内部の空白は残す。"""
    normalized = unicodedata.normalize("NFKC", text.strip()).casefold()

    for mark in _PUNCTUATION:
        normalized = normalized.replace(mark, "")
    return normalized.strip()

def normalize(text: str) -> str:
    """
        表記の違いを吸収した比較用の文字列を返す。
        NFKCとcasefoldの後、半角・全角スペースと句読点を除く。
        検索・削除の指示表現は取り除かない。
    """
    # 表記の違いによる検索漏れを減らすために、文字列を揃える処理
    normalized = unicodedata.normalize("NFKC", text.strip()).casefold()
    # 空白と余白を取り除く
    normalized = normalized.replace(" ", "").replace("\u3000", "")
    for mark in _PUNCTUATION:
        normalized = normalized.replace(mark, "")
    return normalized

def _extract_target(request: str, suffix: re.Pattern[str]) -> str | None:
    """
        正規化し、先頭の「僕の」とコマンドの語尾を取り除き、残りが空ならNoneを返す。
    """
    ## ここで、空白区切りにするのが理想。
    text = normalize_preserving_spaces(request)
    for prefix in sorted(_SPEAKER_PREFIXES, key=len, reverse=True):
        if text.startswith(prefix):
            text = text.removeprefix(prefix)
            break
    if suffix.search(text) is None:
        return None
    target = suffix.sub("", text, count=1).strip()

    return target if target else None

def extract_query(request: str) -> str | None:
    """
    質問コマンドから、検索対象を取り出す。対象がなければ、Noneを返す。
    """
    return _extract_target(request, _QUERY_SUFFIX)

## 削除用と検索のようには、 _extract_targetの仕様を分ける。
def extract_delete_target(request: str) -> str | None:
    """
        削除コマンドから、削除対象を取り出す。
        対象がなければ、Noneを返す。
    """
    return _extract_target(request, _DELETE_SUFFIX)

def delete_memory(memories: list[str], query: str) -> list[str]:
    """
        削除対象を含む記憶全てを除いたリストを返す。
        queryが空、削除コマンドでない、対象が空の場合は、memoriesをそのまま返す。
        比較前に記憶がわもnormalizeされていることを期待する。
    """
    if not query:
        return memories
    ## ここで、quries内の文をmemories内の文と比較して、削除対象を含む文を削除する。
    remaining = [
        memory for memory in memories
        # 正規化したmemoryとqueryが含まれていなければ、リストに追加する。
        if normalize(query) not in normalize(memory)
    ]

    before_length = len(memories)
    after_length = len(remaining)

    if after_length == before_length:
        return memories
    return remaining

    # target = extract_delete_target(query)
    # if target is None:
    #     return memories
    # remaining = [
    #     memory for memory in memories
    #     if target not in normalize(memory)
    # ]
    # before_counter = len(memories)
    # after_counter = len(remaining)

    # if after_counter == before_counter:
    #     return memories
    
    # return remaining

def extract_search_keywords(text: str) -> list[str]:
    """
        検索用の正規化を行い、対象を取り出す。
        検索用の正規化を行い、対象を取り出す。
        queryが空、対象がない場合は、空リストを返す。
    """
    search_lists: list[str] = []
    keywords = text.split()
    
    for keyword in keywords:
        normalized = normalize(keyword)
    
        if normalized == "":
            continue
    
        search_lists.append(normalized)
    return search_lists