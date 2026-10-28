from tkinter import NO
from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.reply import (
 reply,
 reply_remember,
 reply_phrase,
 select_memory,
 propose_memory,
 add_memory
)
from mirocore.terminal_robot.write_read import (
    user_local_file_exists,
    write_user_local_json,
    read_user_local_json,
    local_memory_path,
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

def on_thinking(state: RobotState, request: str, user_name: str, memories: list[str]) -> tuple[RobotEvent,str]:
    face = add_prefix(False, state)
    proposed_memory = propose_memory(request)
    remembered_memory = reply_remember(proposed_memory)
    if remembered_memory is not None:
        memories = add_memory(memories, remembered_memory)
    selected_memory = select_memory(memories, request)
    json_data: dict[str, str |list[str]] = {
        "name": user_name,
        "memories": memories,
    }
    write_user_local_json(user_name, json_data)
    text = reply(request, user_name, selected_memory)
    print(face + f"{user_name}さん、考え中です。少々お待ち下さい。")
    return RobotEvent.REPLY_READY, text


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

## json用のフォルダ作成用のかんす
def create_json_folder(user_name: str) -> None:
    os.makedirs(f"memory_index/{user_name}", exist_ok=True)
    print(f"memory_index/{user_name}フォルダを作成しました: {user_name}")

# <ユーザー名>_memories.jsonというファイルを作成
# 以上のファイルがない時は、この関数を読み出して、ファイルを作らせる。
# ファイルがある時は、そのファイルを読み出して、ユーザー名を返す。
# このファイルは、ユーザー名と、そのユーザーに関する記憶のリストを持っている。
# localでは、nameのみでいい。しかし、globalでは、nameとUUIDを組み合わせて、ユーザーを特定する。
# <ユーザー名>/<ユーザー名>_memories.local.jsonと<ユーザー名>/<ユーザー名>_memories.jsonの二つ作成。
# localの方は、編集可能。しかし、globalの方は、編集不可。
def inputer_user_name() -> str | None:
    try:
        REQUEST_NAME: str = "あなたの名前は？"
        user_name = input(f"{REQUEST_NAME}: ")
        if user_name.strip() == "":
            print("名前が必要です。")
            return inputer_user_name()
        ## ユーザー名の有無を判断。
        if not user_local_file_exists(user_name):
            print(f"あなたの名前は、{user_name}ですね。\nよろしくお願いします。\n")
            create_json_folder(user_name)
            data: dict[str, list[str]] = {
                "name": user_name,
                "memories": [],
            }
            write_user_local_json(user_name, data)
            return user_name
        else:
            data = read_user_local_json(user_name)
            if data is None:
                return None
            if not "name" in data:
                return None
            return data["name"]
    except KeyboardInterrupt:
        print("\n終了します。")
        return None 