import random
## 名前の設定
name = "隆人"
def setup_build_to_user_name() -> str:
    return f"こんにちは、{name}さん"
## 受信用スクリプト作成のモジュール
greeting = ["こんにちは", "おはよう", "こんばんは"]
sad = ["疲れた", "眠い", "鬱病"]
happy = ["楽しい", "嬉しい", "元気"]

## 返信用スクリプト作成のモジュール
greeting_reply = ["こんにちは！", "おはよう！", "こんばんは！"]
sad_reply = ["大丈夫？", "今日もお疲れ様", "鬱病なの？なんかあった？"]
happy_reply = ["よかったね！", "嬉しいね！", "元気だね！"]

def reply(request: str) -> str:
    for word in request.split():
        print(word)
        if word in greeting:
            return random.choice(greeting_reply)
        elif word in sad:
            return sad_reply
        elif word in happy:
            return happy_reply
    return "ごめんね。もう一度聞いてくれる？"