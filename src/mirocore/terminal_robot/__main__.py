from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.reply import reply
def main() -> None:
    # emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    while True:
        try:
            ## ここは、状態遷移用の関数を読み出すためのスクリプト
            try:
                state = transition(state, event)
                ### reply機能を追加・実行。
            except KeyError as err:
                print(f"エラーが発生しました: {err}\n")
                state = RobotState.ERROR
                event = RobotEvent.ERROR_SHOWN
                state = transition(state, event)
            ## 以下のif-elif-else構文は、現在のStateに応じて、次のEventを指定するスクリプト
            if state == RobotState.LISTENING:
                print(add_prefix(False, state) + "待ってるよ")
                request = input(add_prefix(True, state))
                if request.isspace() or request == "":
                    event = RobotEvent.EMPTY_INPUT
                    state = transition(state, event)
                    face = add_prefix(False, state)
                    print(face + "空白だね。もう一度聞いて。")
                    continue
                elif request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
                event = RobotEvent.CONFIRM_INPUT

            elif state == RobotState.THINKING:
                print(add_prefix(False, state) + "考え中")
                reply_text = reply(request)
                event = RobotEvent.REPLY_READY

            elif state == RobotState.SPEAKING:
                face = add_prefix(False, state)
                print(face + reply_text)
                event = RobotEvent.OUTPUT_DONE

            elif state == RobotState.IDLE:
                event = RobotEvent.START_LISTENING

        except KeyboardInterrupt:
            print("\n終了します。")
            break


if __name__ == "__main__":
    main()
