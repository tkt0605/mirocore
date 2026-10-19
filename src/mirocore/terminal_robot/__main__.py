from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.reply import reply

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

def on_listening(state: RobotState) -> tuple[RobotEvent,str]:
    face = add_prefix(False, state)
    print(face + "待ってるよ")
    request = input(add_prefix(True, state))
    if request.strip() == "":
        return RobotEvent.EMPTY_INPUT, ""
    return RobotEvent.CONFIRM_INPUT, request

def on_thinking(state: RobotState, request: str) -> tuple[RobotEvent,str]:
    face = add_prefix(False, state)
    print(face + "考え中")
    return RobotEvent.REPLY_READY, reply(request)


def on_speaking(state: RobotState, reply_text: str) -> RobotEvent:
    face = add_prefix(False, state)
    print(face + reply_text)
    return RobotEvent.OUTPUT_DONE

def on_empty(state: RobotState) -> RobotEvent:
    face = add_prefix(False, state)
    print(face + "空白だね。もう一度聞いて。")
    return RobotEvent.START_LISTENING

def on_idle(state:RobotState) -> RobotEvent:
    return RobotEvent.START_LISTENING

def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    ## 初期条件の設定
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    while True:
        try:
            state = terminal_robot_state(state, event)
            if state == RobotState.LISTENING:
                event, request = on_listening(state)
                if request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
            elif state == RobotState.THINKING:
                event, reply_text = on_thinking(state, request)
            elif state == RobotState.SPEAKING:
                event = on_speaking(state, reply_text)
            elif state == RobotState.IDLE:
                event = on_idle(state)
            elif state == RobotState.EMPTY:
                event= on_empty(state)
            # ## 以下のif-elif-else構文は、現在のStateに応じて、次のEventを指定するスクリプト
            # if state == RobotState.LISTENING:
            #     print(add_prefix(False, state) + "待ってるよ")
            #     request = input(add_prefix(True, state))
            #     if request.isspace() or request == "":
            #         event = on_empty(state)
            #         state = transition(state, event)
            #         face = add_prefix(False, state)
            #         print(face + "空白だね。もう一度聞いて。")
            #         event = RobotEvent.START_LISTENING
            #         continue
            #     if request in { "/q", "/quit", "/exit" }:
            #         print("\n終了します。")
            #         break
            #     event = on_listening(state)

            # elif state == RobotState.THINKING:
            #     reply_text = reply(request)
            #     event = on_thinking(state, request)

            # elif state == RobotState.SPEAKING:
            #     event = on_speaking(state, reply_text)

            # elif state == RobotState.IDLE:
            #     event = on_idle(state)
        except KeyboardInterrupt:
            print("\n終了します。")
            break


if __name__ == "__main__":
    main()
