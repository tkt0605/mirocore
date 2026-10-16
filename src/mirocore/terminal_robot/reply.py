from mirocore.terminal_robot.state import RobotEvent, RobotState, transition
from mirocore.terminal_robot.expressive import add_prefix

def reply(state: RobotState, is_user:bool, request: str) -> None:
    face = add_prefix(is_user, state)

    print(face + f"こんにちは、{request}さん")