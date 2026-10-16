from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix

def main() -> None:
    emoji = add_prefix(False,RobotState.IDLE)
    print("== ターミナル・RoBotを起動しました!! ==")
    print("===================================")
    print(emoji + "!!@@HELLO WORLD@@!!")
    print("===================================")
    state = RobotState.IDLE
    event = RobotEvent.START_LISTENING
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
                print(add_prefix(False, state) + "あなたのお名前は？")
                request = input(add_prefix(True, state))
                if request.isspace() or request == "":
                    ## ここではまだ、stateはListeningのままである
                    event = RobotEvent.EMPTY_INPUT
                    ## ここでは、stateをEMPTYにする
                    state = transition(state, event)
                    print(add_prefix(False, state) + "空白では誰か分からないよ．．．")
                    continue
                elif request in { "/q", "/quit", "/exit" }:
                    print("\n終了します。")
                    break
                event = RobotEvent.CONFIRM_INPUT
            
            elif state == RobotState.THINKING:
                print(add_prefix(False, state) + "考え中")
                event = RobotEvent.REPLY_READY

            elif state == RobotState.SPEAKING:
                print(add_prefix(False, state) + f"こんにちは、{request}さん")
                event = RobotEvent.OUTPUT_DONE

            elif state == RobotState.IDLE:
                event = RobotEvent.START_LISTENING

        except KeyboardInterrupt:
            print("\n終了します。")
            break


if __name__ == "__main__":
    main()
