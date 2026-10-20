import sys
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

def inputer_user_name() -> str:
    try:
        REQUEST_NAME: str = "あなたの名前は？"
        user_name = input(f"{REQUEST_NAME}: ")
        if user_name.strip() == "":
            print("名前が必要です。")
            return inputer_user_name()
        print(f"あなたの名前は、{user_name}ですね。\nよろしくお願いします。\n")
        return user_name

    except KeyboardInterrupt:
        print("\n終了します。")