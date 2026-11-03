from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.options import (
    inputer_user_name,
    terminal_robot_state,
    on_listening,
    on_thinking,
    on_speaking,
    on_empty,
    on_idle,
)
from mirocore.terminal_robot.write_read import (
    read_user_local_json,
    write_user_local_json,
)
import json
import os

def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    ## 初期条件の設定
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    user_data = inputer_user_name()
    print(" hello world ")
    if user_data is None or user_data.get("name") is None:
        return
    user_name = user_data.get("name")
    memories = user_data.get("memories")
    if memories is None:
        memories = []
    else:
        memories = [
            item for item in memories if isinstance(item, str)
        ]

    # memories = control_memories(user_name)
    # if memories is None:
    #     return
    while True:
        try:
            state = terminal_robot_state(state, event)
            if state == RobotState.LISTENING:
                event, request = on_listening(state, user_name)
                if request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
            elif state == RobotState.THINKING:
                event, reply_text, memories = on_thinking(state, request, user_name, memories)

            elif state == RobotState.SPEAKING:
                event = on_speaking(state, reply_text)
            elif state == RobotState.IDLE:
                event = on_idle(state)
            elif state == RobotState.EMPTY:
                event= on_empty(state, user_name)
        except KeyboardInterrupt:
            print("\n終了します。")
            break
        except RuntimeError as runtime_error:
            print(f"実行時エラーが発生しました: {runtime_error}")
            state =RobotState.IDLE
            event =RobotEvent.START_LISTENING
            continue

# def control_memories(user_name: str) -> list[str] | None:
#     try:
#         loaded_data = read_user_local_json(user_name)
#         if loaded_data is not None and isinstance(loaded_data.get("memories"), list):
#             return [
#                 item for item in loaded_data["memories"] if isinstance(item, str)
#             ]
#         else:
#             return []

#     except FileNotFoundError:
#         return []

#     except json.JSONDecodeError as json_error:
#         print(f"既存のJSONファイルが破損しているため、読み込めませんでした: {json_error}")

if __name__ == "__main__":
    main()
