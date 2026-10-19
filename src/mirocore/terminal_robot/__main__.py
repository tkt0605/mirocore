from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.reply import reply

REQUEST_NAME: str = "あなたの名前は？"

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

def on_thinking(state: RobotState, request: str, user_name: str) -> tuple[RobotEvent,str]:
    face = add_prefix(False, state)
    print(face + f"{user_name}さん、考え中です。少々お待ち下さい。")
    return RobotEvent.REPLY_READY, reply(request, user_name)


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

def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    user_name = input(f"{REQUEST_NAME}: ")
    print(f"あなたの名前は、{user_name}ですね。")
    ## 初期条件の設定
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
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
