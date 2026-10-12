# Repository Guidelines

## プロジェクト概要

Miroc Coreは、人と長期的な関係を築くPersonal Robotの基盤です。
中心理念は「The body can change. The relationship remains.」です。
現在はPython 3.13で、Coreの設定処理とDB不要のTerminal Robotを開発しています。
小さく理解できる実装を優先し、未実装の将来機能を先回りして追加しないでください。

## プロジェクト構成

- `src/mirocore/`: アプリケーション本体です。
- `src/mirocore/config.py`: 環境変数から設定を構築します。
- `src/mirocore/main.py`: `mirocore` CLIのエントリーポイントです。
- `src/mirocore/terminal_robot/`: DB・LLMなしで動く会話試作です。
- `terminal_robot/state.py`: 状態、イベント、純粋な遷移関数を定義します。
- `terminal_robot/__main__.py`: 入力ループと状態別の処理を担当します。
- `terminal_robot/expressive.py`: 表情管理を配置するモジュールです。
- `terminal_robot/reply.py`: 応答処理を配置するモジュールです。
- `tests/`: pytestのテストを、本体と対応する構成で置きます。
- `docs/`: 設計、計画、質問、デバッグ手順を保存します。
- `.docker/` と `docker-compose.yml`: コンテナ実行環境です。
- `.github/workflows/test.yml`: pushとPRでpytestを実行します。
- `pyproject.toml` と `uv.lock`: 依存関係と再現可能なロック情報です。

## アーキテクチャ原則

Terminal Robotの基本遷移は次のとおりです。

`IDLE → LISTENING → THINKING → SPEAKING → IDLE`

状態とイベントの組み合わせは`transition()`に集約してください。
入力、状態遷移、応答生成、表情、描画を一つの関数へ混在させないでください。
通常の会話処理は、DB、LLM、ネットワークなしでも動作可能に保ちます。
OS固有処理や将来のハードウェア処理はAdapterとして分離します。
非TTY環境ではプレーンテキストへフォールバックできる設計を優先します。

LLMは応答や行動を提案できますが、実行権限は持ちません。
権限、DB書き込み、タイムアウト、再試行、モーター、安全停止は決定論的コードが管理します。
安全境界は`Miroc Core / LLM → Policy Layer → Robot Controller`です。

## セットアップと開発コマンド

依存関係をロックファイルどおりに同期します。

```bash
uv sync --frozen
```

ローカルの全テストを実行します。

```bash
uv run pytest -v
```

Terminal Robotを対話モードで起動します。

```bash
uv run python -m mirocore.terminal_robot
```

Core CLIは`DATABASE_URL`を設定して起動します。

```bash
DATABASE_URL='<development-url>' uv run mirocore
```

Docker環境をビルドして起動します。

```bash
docker compose up --build
```

コンテナ内でテストを実行します。

```bash
docker compose run --rm --build mirocore uv run pytest
```

依存関係を変更した場合は`pyproject.toml`と`uv.lock`を同時に更新してください。
pytest関連のツールは原則として開発依存へ追加します。

## コーディング規約

インデントはスペース4文字とし、PythonのPEP 8を基準にします。
関数と変数は`snake_case`、クラスとEnumは`PascalCase`を使います。
定数とEnumメンバーには`UPPER_SNAKE_CASE`を使います。
公開関数には引数と戻り値の型注釈を付けてください。
importは標準ライブラリ、外部パッケージ、ローカルモジュールの順に整理します。
未使用importや、`except Exception`のような広すぎる例外捕捉を避けます。
例外は想定した発生源の近くで、具体的な型を捕捉してください。
コメントは処理の逐語訳ではなく、判断理由や制約を説明します。
関数は一つの責務に絞り、状態変更と入出力の境界を明確にします。
現時点ではフォーマッターやリンターを必須設定として導入していません。
新しいツールを追加する場合は、必要性とCIへの影響を説明してください。

## テスト指針

テストフレームワークはpytestです。
ファイルは`test_*.py`、関数は`test_*`で命名します。
変更した振る舞いには、正常系と重要な異常系のテストを追加してください。
状態遷移では、現在状態、イベント、期待する次状態を明示します。
対話入力は`monkeypatch`、標準出力は`capsys`で検証します。
`Ctrl+C`は`KeyboardInterrupt`を発生させ、正常終了メッセージを確認します。
テスト同士で状態を共有せず、単独でも実行できるようにします。

対象テストだけを実行する例です。

```bash
uv run pytest tests/terminal_robot/test_main.py -v
```

完了前に全テストを実行し、収集数、成功数、終了コードを確認してください。
`collected 0 items`は成功として扱いません。
設定確認、Dockerビルド、コンテナ起動、対話動作は別々の検証です。

## コミットとPull Request

既存履歴は、日本語で変更内容と効果を説明するコミットメッセージが中心です。
一つのコミットには一つの目的を持たせ、変更対象を具体的に書いてください。
例: `Terminal RobotのCtrl+C終了テストを追加`
生成キャッシュ、`.venv`、`.env`、秘密情報はコミットしないでください。

PRには目的、主な変更、確認コマンド、結果、未検証事項を記載します。
関連Issueがある場合はリンクしてください。
画面表示を変更した場合は、必要に応じて実行ログや画像を添付します。
依存関係、公開API、環境変数を変えた場合は影響範囲を明記します。
レビューしやすい小さな差分を優先し、無関係な整形を混ぜないでください。

## セキュリティと設定

`DATABASE_URL`、APIキー、トークン、パスワードを表示・記録・コミットしないでください。
接続情報を説明するときは、実値ではなく環境変数名を使用します。
現行Core CLIの接続URL出力は機密情報漏えいのリスクとして扱ってください。
LLMへShell、ホストファイル、秘密情報、DB書き込み、ハードウェア制御を直接許可しません。
Docker設定が通ることと、実際のサービスが安全に動くことを区別してください。
実機制御では、タイムアウト、緊急停止、フェイルセーフを個別に検証します。

## コントリビューターとエージェントの作業手順

作業前に対象ファイル、関連テスト、`git status`、現在の実行経路を確認してください。
既存の未コミット変更は他者の作業として扱い、上書きしないでください。
調査依頼では、再現、原因、影響、修正案までを示し、無断で変更しません。
実装依頼では、根本原因に対応する最小変更を行い、関連テストを実行します。
依存追加、大規模リファクタリング、公開API変更は事前に影響を説明します。
明示的な依頼なしにcommit、push、ブランチ作成、外部書き込みを行いません。
報告では「コード確認」「実行確認」「推測」「未検証」を区別してください。
ユーザーが学習中の場合は、完成コードだけでなく役割と状態変化を短く説明します。
