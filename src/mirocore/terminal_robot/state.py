from enum import Enum

class RobotState(Enum):
    IDLE = "idle"
    ERROR = "error"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    EMPTY = "empty"
    DELETE = "delete"

## ここでは、状態変化のきっかけを表すイベントを定義。
class RobotEvent(Enum):
    START_LISTENING = "# 入力受付開始"
    CONFIRM_INPUT = "# 入力確定"
    REPLY_READY = "# 返答完成"
    OUTPUT_DONE = "# 出力完了"
    ERROR_SHOWN = "# エラー表示"
    EMPTY_INPUT = "# 空文字入力"
    DELETE_MEMORY = "# 記憶削除"
## ここでは、状態遷移ルールを定義している。
_TRANSITIONS: dict[tuple[RobotState, RobotEvent], RobotState] = {
    (RobotState.IDLE, RobotEvent.START_LISTENING): RobotState.LISTENING,
    (RobotState.LISTENING, RobotEvent.CONFIRM_INPUT): RobotState.THINKING,
    (RobotState.THINKING, RobotEvent.REPLY_READY): RobotState.SPEAKING,
    (RobotState.SPEAKING, RobotEvent.OUTPUT_DONE): RobotState.IDLE,
    (RobotState.ERROR, RobotEvent.ERROR_SHOWN): RobotState.IDLE,
    (RobotState.LISTENING, RobotEvent.EMPTY_INPUT): RobotState.EMPTY,
    (RobotState.EMPTY, RobotEvent.START_LISTENING): RobotState.LISTENING,
    (RobotState.LISTENING, RobotEvent.DELETE_MEMORY): RobotState.DELETE,
    (RobotState.DELETE, RobotEvent.START_LISTENING): RobotState.LISTENING,
}

def transition(state: RobotState, event: RobotEvent) -> RobotState:
    return _TRANSITIONS[(state, event)]