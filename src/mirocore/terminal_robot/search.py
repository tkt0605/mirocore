"""検索要求から記憶を探し、応答文を作る。"""
import re

from mirocore.terminal_robot.normalized import _extract_target, normalize

## 検索用の正規化用の正規表現
_QUERY_SUFFIX = re.compile(
    r"(?:について|を)?\s*"
    r"(?:について|を)?(?:覚えて(?:る|いる|ます|います)か?|教えて(?:ください)?)$"
)

def extract_query(request: str) -> str | None:
    """
    質問コマンドから、検索対象を取り出す。対象がなければ、Noneを返す。
    """
    return _extract_target(request, _QUERY_SUFFIX)

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

def search_memory(memories: list[str], keywords: list[str]) -> list[str]:
    # keywords = [
    #     keyword for keyword in keywords if keyword != ""
    # ]
    keywords = list(filter(lambda keyword: keyword != "", keywords))
    if not keywords:
        return []
    results: list[str] = []

    for memory in memories:
        normalized_memory = normalize(memory)
        if all(keyword in normalized_memory for keyword in keywords):
            results.append(memory)
    return results

def reply_to_search_memory(
    memories: list[str],
    keywords: list[str]
) -> str | None:
    search_results = search_memory(memories, keywords)

    if not search_results:
        return "検索結果がありません。"
    return "\n".join(search_results)