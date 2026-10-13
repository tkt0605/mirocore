from mirocore.terminal_robot.expressive import add_prefix

## is_user=Trueの時に「あなた  > 」を返すかどうか
def test_add_prefix_user() -> None:
    assert add_prefix(True) == "あなた  > "

## 一方、is_user=Falseの時に「MIROC  > 」を返すかどうか
def test_add_prefix_miroc() -> None:
    assert add_prefix(False) == "MIROC  > "


