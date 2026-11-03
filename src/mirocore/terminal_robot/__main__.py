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
    user_name = inputer_user_name()
    print(" hello world ")
    if user_name is None:
        return
    memories = control_memories(user_name)
    if memories is None:
        return
    # loaded_data = read_user_local_json(user_name)
    # memories: list[str] = []
    # if loaded_data is not None and isinstance(loaded_data.get("memories"), list):
    #     memories = [
    #         item for item in loaded_data["memories"] if isinstance(item, str)
    #     ]
    # else:
    #     memories = []

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
        except json.JSONDecodeError as json_error:
            print(f"既存のJSONファイルが破損しているため、読み込めませんでした: {json_error}")
        except Exception as error:
            print(f"予期せぬエラーが発生しました: {error}")

def control_memories(user_name: str) -> list[str] | None:
    try:
        # loaded_data = user_name.get("memories")
        loaded_data = read_user_local_json(user_name)
        if loaded_data is not None and isinstance(loaded_data.get("memories"), list):
            return [
                item for item in loaded_data["memories"] if isinstance(item, str)
            ]
        else:
            return []

    except FileNotFoundError:
        return []

    except json.JSONDecodeError as json_error:
        print(f"既存のJSONファイルが破損しているため、読み込めませんでした: {json_error}")
        return None

if __name__ == "__main__":
    main()
