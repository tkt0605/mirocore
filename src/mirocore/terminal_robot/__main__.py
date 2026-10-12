from mirocore.terminal_robot.state import RobotEvent, RobotState, transition


def main() -> None:
    print("== ターミナル・RoBotを起動しました!! ==")
    print("===================================")
    print("!!@@HELLO WORLD@@!!")
    print("===================================")
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
    request = ""

    while True:
        try:
            ## ここは、状態遷移用の関数を読み出すためのスクリプト
            try:
                state = transition(state, event)
            except KeyError as err:
                print(f"エラーが発生しました: {err}")
                state = RobotState.ERROR
                event = RobotEvent.ERROR_SHOWN
                state = transition(state, event)
            ## 以下のif-elif-else構文は、現在のStateに応じて、次のEventを指定するスクリプト
            if state == RobotState.LISTENING:
                request = input("あなたの名前を教えてください:")
                ### 空文字の場合は、メッセージを残して、IDLE状態にする
                if request == "":
                    state = RobotState.ERROR
                    event = RobotEvent.ERROR_SHOWN
                    print("===================================")
                    print("@@ 空文字では誰かはわかりません @@")
                    print("===================================")
                    continue
                elif request in { "/q", "/quit", "/exit" }:
                    break
                event = RobotEvent.CONFIRM_INPUT
            
            elif state == RobotState.THINKING:
                print(f"こんにちは、{request}さん")
                event = RobotEvent.REPLY_READY

            elif state == RobotState.SPEAKING:
                event = RobotEvent.OUTPUT_DONE

            elif state == RobotState.IDLE:
                event = RobotEvent.START_LISTENING

            elif state == RobotState.ERROR:
                print("エラーが発生しました。")

        except KeyboardInterrupt:
            print("\n終了します。")
            break

if __name__ == "__main__":
    main()
