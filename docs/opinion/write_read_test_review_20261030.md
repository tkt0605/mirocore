# write_read テストの現状（2026-10-30）

日付: 2026-10-30

## 目的

`src/mirocore/terminal_robot/write_read.py` の4関数について、テストが正常系と重要な異常系を押さえているかを共有する。実装の変更は求めていない。不足しているテストを足すときの基準にする。

対象ファイル: `tests/terminal_robot/test_write_read.py`

## 結論

4関数のうち、当初の正常系・異常系を一通り押さえているものはない。`local_memory_path` の正常系だけが足りている。`user_local_file_exists` と `read_user_local_json` は、作業ツリーの `memory_index/test/test_memories.local.json` に依存している。

ファイルを触るテストは `tmp_path` と `monkeypatch.chdir` に閉じる。リポジトリ直下の `memory_index/` へ書かない。

## 関数ごとの判定

| 関数 | 正常系 | 異常・境界 | 判定 |
|---|---|---|---|
| `local_memory_path` | ユーザー名から `memory_index/<名前>/<名前>_memories.local.json` になることを確認済み | ディレクトリを作らないことは未確認（優先度は低い） | パス組み立ての正常系は足りている |
| `user_local_file_exists` | `"test"` で `True` のみ。実ファイルがある前提 | ファイルが無いとき `False` は未確認 | 不十分。環境が変わると落ちる |
| `read_user_local_json` | `"test"` の中身が `{"name": "test", "memories": []}` と一致することのみ | ファイルが無いとき `None` は未確認。壊れた JSON が例外のままであることも未確認 | 不十分。`test` の JSON に記憶が増えるとこの assert は壊れる |
| `write_user_local_json` | `tmp_path` 上で初回作成し、読み戻しが一致する | `name` の上書き、既存 `memories` への追記、同じ文を足さないこと、不正キーの `ValueError` でファイルが変わらないことは未確認 | 新規作成だけ。関数固有の振る舞いは未カバー |

## いまのテストが実際に見ていること

- `test_local_memory_path`: 戻り値の `Path` が期待パスと一致する。
- `test_user_local_file_exists`: `user_local_file_exists("test") == True`。一時ディレクトリは使っていない。
- `test_read_user_local_json`: カレントディレクトリの `test` ユーザー JSON を読む。
- `test_write_user_local_json`: `tmp_path` へ移動し、親ディレクトリを作ってから初回書き込みし、`read_user_local_json` の結果と比較する。マージ・重複・不正キーは見ていない。

テスト関数の戻り型が `-> Path` や `-> bool` になっている箇所がある。pytest のテストは `-> None` にする。

## 次に足す確認

1. `exists` / `read` / `write` をすべて `tmp_path` に閉じる。
2. ファイルが無いとき、`user_local_file_exists` は `False`、`read_user_local_json` は `None`。
3. `write_user_local_json` の2回目で、既存の記憶の後ろに新しい文が足される。同じ文を渡しても件数は増えない。
4. `name` と `memories` 以外のキーでは `ValueError` になり、既存ファイルの中身は変わらない。

## 参考: reply 側で済んでいる正常系

`tests/terminal_robot/test_reply.py` では、次は確認済み。

- `add_memory` の未登録1件: 同じリストオブジェクトを返し、元の順序の末尾にその1件だけ増える（`result is memories` と、呼ぶ前のコピーへ同じ文を足したリストとの一致）。
- `reply_to_self_introduction`: `True` は `"覚えておくね。"`、`False` は `"それは前に聞いたよ。"`。

`add_memory` の重複・空文字、`select_memory`、`propose_memory` の期待値の固定、`on_thinking` と `main` の記憶読み込みは、この文書の対象外。