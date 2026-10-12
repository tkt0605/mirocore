## ここでは、idleの正常な状態と、Errorの状態を定義しています。

from enum import Enum

class RobotState(Enum):
    IDLE = "idle"
    ERROR = "error"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"

## ここでは、状態変化のきっかけを表すイベントを定義。
class RobotEvent(Enum):
    START_LISTENING = "# 入力受付開始"
    CONFIRM_INPUT = "# 入力確定"
    REPLY_READY = "# 返答完成"
    OUTPUT_DONE = "# 出力完了"
    ERROR_SHOWN = "# エラー表示"

## ここでは、状態遷移ルールを定義している。
_TRANSITIONS: dict[tuple[RobotState, RobotEvent], RobotState] = {
    (RobotState.IDLE, RobotEvent.START_LISTENING): RobotState.LISTENING,
    (RobotState.LISTENING, RobotEvent.CONFIRM_INPUT): RobotState.THINKING,
    (RobotState.THINKING, RobotEvent.REPLY_READY): RobotState.SPEAKING,
    (RobotState.SPEAKING, RobotEvent.OUTPUT_DONE): RobotState.IDLE,
    (RobotState.ERROR, RobotEvent.ERROR_SHOWN): RobotState.IDLE
}

def transition(state: RobotState, event: RobotEvent) -> RobotState:
    return _TRANSITIONS[(state, event)]