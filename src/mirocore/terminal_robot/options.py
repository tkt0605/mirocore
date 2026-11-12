from doctest import FAIL_FAST
from tkinter import NO
from types import NoneType
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.reply import (
 reply_to_greeting,
 reply_remember,
 reply_phrase,
 propose_memory,
 add_memory,
 reply_to_self_introduction,
 search_memory,
)
from mirocore.terminal_robot.normalized import (
    normalize,
    normalize_word,
    normalized_delete_req,
)
from mirocore.terminal_robot.write_read import (
    specific_delete_user_local_json,
    user_local_file_exists,
    write_user_local_json,
    read_user_local_json,
    local_memory_path,
    create_json_folder,
    delete_user_local_file,
)
import json
import os

def terminal_robot_state(state: RobotState, event: RobotEvent) -> RobotState:
    ## ここは、状態遷移用の関数を読み出すためのスクリプト
    try:
        ### ここで、LISTENINGになっている
        state = transition(state, event)
        ### reply機能を追加・実行。
    except KeyError as err:
        print(f"エラーが発生しました: {err}\n")
        state = RobotState.ERROR
        event = RobotEvent.ERROR_SHOWN
        state = transition(state, event)
    return state

def on_listening(state: RobotState, user_name: str) -> tuple[RobotEvent,str]:
    face = add_prefix(False, state)
    print(face + f"{user_name}さん、待ってるよ")
    request = input(add_prefix(True, state))
    if request.strip() == "":
        return RobotEvent.EMPTY_INPUT, ""
    return RobotEvent.CONFIRM_INPUT, request

def reply_to_search_memory(
    memories: list[str],
    query: str
) -> str | None:
    search_results = search_memory(memories, query)
    result_counter = len(search_results)
    if result_counter == 0:
        return "検索結果がありません。"
    else:
        body = "\n".join(search_results)
        return f"{body}"

def request_to_search(request: str) -> bool:
    normalized_request = normalize(request)
    normalized_text = normalize_word(normalized_request)
    return normalized_text is not None

def catch_up_query_to_request(request: str) -> str | None:
    normalized_query = normalize(request)
    normalized_word = normalize_word(normalized_query)
    if normalized_word is None:
        return None
    return normalized_word

def on_thinking(
    state: RobotState,
    request: str,
    user_name: str,
    memories: list[str]
) -> tuple[RobotEvent, str, list[str]]:
    face = add_prefix(False, state)
    delete_request = normalized_delete_req(request)
    proposed_memory = propose_memory(request)
    remembered_memory = reply_remember(proposed_memory)
    search_request = request_to_search(request)
    before_memory = len(memories)
    if delete_request is not None:
        remaining_memories = on_delete(memories, request, user_name)
        if len(remaining_memories) < before_memory:
            text = f"{delete_request}を削除しました。"
        else:
            text = f"{delete_request}は見つかりませんでした。"
        return RobotEvent.REPLY_READY, text, remaining_memories
    elif search_request is True:
        search_target = catch_up_query_to_request(request)
        text = reply_to_search_memory(memories, search_target)
    elif remembered_memory is not None:
        memories = add_memory(memories, remembered_memory)
        after_memory = len(memories)
        added_memory = after_memory - before_memory
        text = reply_to_self_introduction(added_memory > 0)
    elif remembered_memory is None:
        text = reply_to_greeting(request, user_name)
    json_data: dict[str, str |list[str]] = {
        "name": user_name,
        "memories": memories,
    }
    write_user_local_json(user_name, json_data)
    print(face + f"{user_name}さん、考え中です。少々お待ち下さい。")
    return RobotEvent.REPLY_READY, text, memories


def on_speaking(state: RobotState, reply_text: str) -> RobotEvent:
    face = add_prefix(False, state)
    print(face + reply_text)
    return RobotEvent.OUTPUT_DONE

def on_empty(state: RobotState, user_name: str) -> RobotEvent:
    face = add_prefix(False, state)
    print(face + f"{user_name}さん空白です。もう一度聞いてください。")
    return RobotEvent.START_LISTENING

def on_idle(state:RobotState) -> RobotEvent:
    return RobotEvent.START_LISTENING

def on_delete_memory(state: RobotState, user_name: str) -> RobotEvent:
    face = add_prefix(False, state)
    delete_user_local_file(user_name)
    print(face + f"{user_name}さん、記憶を削除します。")
    return RobotEvent.START_LISTENING
# 記憶の削除
# 入力：記憶内容、ユーザー名
# 出力：検索対象のデータ
def on_delete(memories: list[str], query:str, user_name: str) -> list[str]:
    if not query:
        return memories
    
    normalized_delete = normalized_delete_req(query)
    if not normalized_delete:
        return memories

    response = memories.copy()
    for memory in memories:
        if normalized_delete == memory:
            response.remove(memory)
            specific_delete_user_local_json(user_name, response)
            break
    return response
# <ユーザー名>_memories.jsonというファイルを作成
# 以上のファイルがない時は、この関数を読み出して、ファイルを作らせる。
# ファイルがある時は、そのファイルを読み出して、ユーザー名を返す。
# このファイルは、ユーザー名と、そのユーザーに関する記憶のリストを持っている。
# localでは、nameのみでいい。しかし、globalでは、nameとUUIDを組み合わせて、ユーザーを特定する。
# <ユーザー名>/<ユーザー名>_memories.local.jsonと<ユーザー名>/<ユーザー名>_memories.jsonの二つ作成。
# localの方は、編集可能。しかし、globalの方は、編集不可。

# R02の根本原因
def inputer_user_name() -> tuple[str, list[str]] | None:
    while True:
        try:
            REQUEST_NAME: str = "あなたの名前は？"
            user_name = input(f"{REQUEST_NAME}: ")
            if user_name.strip() == "":
                print("名前が必要です。")
                continue
            ## ユーザー名の有無を判断。
            if not user_local_file_exists(user_name):
                print(f"あなたの名前は、{user_name}ですね。\nよろしくお願いします。\n")
                create_json_folder(user_name)
                data: dict[str, str | list[str]] = {
                    "name": user_name,
                    "memories": [],
                }
                write_user_local_json(user_name, data)
                return user_name, []
            else:
                data = read_user_local_json(user_name)
                if data is None:
                    continue
                return user_name, data["memories"]

        except KeyboardInterrupt:
            print("\n終了します。")
            return None
        
        except TypeError as type_error:
            print(f"予期せぬエラーが発生しました: {type_error}")

        except KeyError as key_error:
            print(f"キーが見つかりません: {key_error}")
            return None
        
        except ValueError as value_error:
            print(f"無効な名前です: {value_error}")
            continue