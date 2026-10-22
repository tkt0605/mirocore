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
def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    ## 初期条件の設定
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    user_name = inputer_user_name()

    if user_name is None:
        return
    while True:
        try:
            state = terminal_robot_state(state, event)
            if state == RobotState.LISTENING:
                event, request = on_listening(state, user_name)
                if request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
            elif state == RobotState.THINKING:
                event, reply_text = on_thinking(state, request, user_name)
            elif state == RobotState.SPEAKING:
                event = on_speaking(state, reply_text)
            elif state == RobotState.IDLE:
                event = on_idle(state)
            elif state == RobotState.EMPTY:
                event= on_empty(state, user_name)
        except KeyboardInterrupt:
            print("\n終了します。")
            break


if __name__ == "__main__":
    main()
