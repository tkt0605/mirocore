from mirocore.terminal_robot.expressive import add_prefix
from mirocore.terminal_robot.state import RobotState

## is_user=Trueの時に「あなた  > 」を返すかどうか
def test_add_prefix_user() -> None:
    state = RobotState.IDLE
    assert add_prefix(True, state) == "あなた  > "

## 一方、is_user=Falseの時に、IDLE状態の時に「(－‿－) > 」を返すかどうか
def test_add_prefix_miroc_idle() -> None:
    state = RobotState.IDLE
    assert add_prefix(False, state) == "(－‿－) > "

def test_add_prefix_miroc_listening() -> None:
    state = RobotState.LISTENING
    assert add_prefix(False, state) == "MIROC(•‿•) > "

def test_add_prefix_miroc_thinking() -> None:
    state = RobotState.THINKING
    assert add_prefix(False, state) == "MIROC(•_•) > "

def test_add_prefix_miroc_speaking() -> None:
    state = RobotState.SPEAKING
    assert add_prefix(False, state) == "MIROC(^‿^) > "

def test_add_prefix_miroc_error() -> None:
    state = RobotState.ERROR
    assert add_prefix(False, state) == "MIROC(×_×) > "

def test_add_prefix_miroc_empty() -> None:
    state = RobotState.EMPTY
    assert add_prefix(False, state) == "MIROC(・o・) > "