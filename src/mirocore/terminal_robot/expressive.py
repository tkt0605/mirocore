## terminal・Robotのターミナル管理用のモジュール

## ターミナルの表示の前に、出力内容によって「YOU:」or「ROBOT:」を追加する。
def add_prefix(message: str) -> str:
    if message.startswith("あなたの名前を教えてください:"):
        return "YOU >" + message
    elif message.startswith("考え中..."):
        return "ROBOT >" + message
    else:
        return "YOU >" + message

## 「考え中...」の後にloading用（例で言うと、npm i ora）の点々を追加する。

### 今はまだ早いけど、表情もつける
