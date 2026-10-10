# Terminal Robot 状態設計

## 目的
ターミナルで、ユーザが送った内容に表情で反応する、簡単なターミナル・ロボットを作成する。

## 状態の意味

### IDLE
- デフォルトの状態。Textが空状態

### LISTENING
- textが入力済みの状態

### THINKING
- textが送信済みの状態

### SPEAKING
- 返信用のtextが表示済みの状態

### ERROR
- 表示、処理を失敗した時の状態

## 正常な状態遷移

| 現在 | イベント | 次 |
|---|---|---|
| idle | 入力受付開始 | listening |
| listening | 入力確定 | thinking |
| thinking | 返答完成 | speaking |
| speaking | 出力完了 | idle |
| error | エラー取得・表示 | idle |

## 終了方法
listening中に /q または, /quit 
全ての状態で Ctrl+C で 切れる。

## 不正な状態遷移
状態は変更しない。
エラーを発生し、表示。
安全にループを終了し、強制的に停止させる。

## 初期MVPでは扱わないもの
 /q と /quit はLISTENING中だけ、どの状態からでも停止できるのはCtrl+C