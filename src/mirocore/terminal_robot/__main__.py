from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.options import (
    inputer_user_name,
    terminal_robot_state,
    on_listening,
    on_thinking,
    on_speaking,
    on_delete_memory,
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
    result = inputer_user_name()
    if result is None:
        return
    print(" hello world ")
    user_name, memories = result
    while True:
        try:
            state = terminal_robot_state(state, event)
            if state == RobotState.LISTENING:
                event, request = on_listening(state, user_name)
                if request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
                elif request in { "/d", "/delete", "/delete_memory" }:
                    event = RobotEvent.DELETE_MEMORY
                    event = on_delete_memory(state, event, user_name)
                    continue
            elif state == RobotState.THINKING:
                event, reply_text, memories = on_thinking(state, request, user_name, memories)

            elif state == RobotState.SPEAKING:
                event = on_speaking(state, reply_text)
            elif state == RobotState.IDLE:
                event = on_idle(state)
            elif state == RobotState.EMPTY:
                event= RobotEvent.DELETE_MEMORY
                on_delete_memory(state, event, user_name)
                continue
        except KeyboardInterrupt:
            print("\n終了します。")
            break
        except RuntimeError as runtime_error:
            print(f"実行時エラーが発生しました: {runtime_error}")
            state =RobotState.IDLE
            event =RobotEvent.START_LISTENING
            continue

if __name__ == "__main__":
    main()
