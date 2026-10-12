## terminal・Robotのターミナル管理用のモジュール

# ターミナルの表示の前に、ユーザーかロボットかによって「YOU」か「MIROC」を追加する。

def add_prefix(is_user:bool) -> str:
    if is_user:
        return "あなた  > "
    else:
        return "MIROC  > "

## 「考え中...」の後にloading用（例で言うと、npm i ora）の点々を追加する。

### 今はまだ早いけど、表情もつける
