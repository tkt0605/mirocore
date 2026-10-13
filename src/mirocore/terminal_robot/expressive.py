## terminal・Robotのターミナル管理用のモジュール
import stat
from mirocore.terminal_robot.state import RobotState
# ターミナルの表示の前に、ユーザーかロボットかによって「YOU」か「MIROC」を追加する。

def add_prefix(is_user:bool, state) -> str:
    def add_emoji(state: RobotState) -> str:
        if state == state.IDLE:
            return "(－‿－)";
        elif state == state.LISTENING:
            return "(•‿•)"
        elif state == state.THINKING:
            return "(•_•)"
        elif state == state.SPEAKING:
            return "(^‿^)"
        else:
            return "(×_×)"
    
    emoji = add_emoji(state)
    
    if is_user:
        return "あなた  > "
    elif is_user is False and state == RobotState.IDLE:
        return emoji + " > "
    else:
        return "MIROC" + emoji + " > "

## 「考え中...」の後にloading用（例で言うと、npm i ora）の点々を追加する。
