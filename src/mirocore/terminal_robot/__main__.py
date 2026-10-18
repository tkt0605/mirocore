from tkinter import RADIOBUTTON
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

def terminal_robot_event(state: RobotState) -> RobotEvent:
    if state == RobotState.IDLE:
        event = RobotEvent.START_LISTENING
    elif state == RobotState.LISTENING:
        event = RobotEvent.CONFIRM_INPUT
    elif state == RobotState.THINKING:
        event = RobotEvent.REPLY_READY
    elif state == RobotState.SPEAKING:
        event = RobotEvent.OUTPUT_DONE
    
    elif state == RobotState.ERROR:
        event = RobotEvent.ERROR_SHOWN
    elif state == RobotState.EMPTY:
        event = RobotEvent.START_LISTENING
    return event
def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    ## 初期条件の設定
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    while True:
        try:
            state = terminal_robot_state(state, event)
            ## 以下のif-elif-else構文は、現在のStateに応じて、次のEventを指定するスクリプト
            if state == RobotState.LISTENING:
                print(add_prefix(False, state) + "待ってるよ")
                request = input(add_prefix(True, state))
                if request.isspace() or request == "":
                    event = terminal_robot_event(state)
                    state = transition(state, event)
                    face = add_prefix(False, state)
                    print(face + "空白だね。もう一度聞いて。")
                    event = RobotEvent.START_LISTENING
                    continue
                elif request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
                event = terminal_robot_event(state)

            elif state == RobotState.THINKING:
                print(add_prefix(False, state) + "考え中")
                reply_text = reply(request)
                event = terminal_robot_event(state)

            elif state == RobotState.SPEAKING:
                face = add_prefix(False, state)
                print(face + reply_text)
                event = terminal_robot_event(state)

            elif state == RobotState.IDLE:
                event = terminal_robot_event(state)

        except KeyboardInterrupt:
            print("\n終了します。")
            break


if __name__ == "__main__":
    main()
