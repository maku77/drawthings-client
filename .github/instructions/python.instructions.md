---
applyTo: "**/*.py"
---

# Python Coding Guidelines

Apply the [general coding guidelines](./general.instructions.md) to all code.

## 基本原則

- Python のプロジェクト管理、パッケージ管理には必ず`uv` を使用してください。
- パッケージのインストールには `uv add` を使用すること（`pip install` は使用しない）。
- Python スクリプトの実行には `uv run` を使用すること。
- Python 3.8+を対象とする
- PEP 8 スタイルガイドに準拠
- 型ヒントを必須とする
- コレクション型として大文字の `Dict` や `List` は使わず、代わりに小文字の `dict` や `list` を使用すること。

## コーディング規約

- import 文は標準ライブラリ、サードパーティ、ローカルモジュールの順に記述
- 全ての関数とメソッドに型ヒントを付ける
- docstring を必ず記述する（Args、Returns、Raises を含む）
- 具体的な例外を使用し、チェーンする（`raise ... from e`）
- `pathlib.Path`を使用してファイル操作を行う
- ログ出力には`logging`モジュールを使用

## 命名規則

- パッケージ名（モジュール名 は文字のみ（例: `mypackage`）
- クラス名は大文字で始める（例: `MyClass`）
- 関数、あるいは public メソッド、変数は文字（例: `my_public_method`）
- protected メソッドはアンダースコア 1 つで始める（例: `_my_protected_method`）
- private メソッドはアンダースコア 2 つで始める（例: `__my_private_method`）
- 定数名はすべて大文字（例: `MY_CONSTANT`）

## 推奨パターン

- データクラスには`@dataclass`を使用
- 設定管理には`pydantic.BaseSettings`を使用
- Context Manager を積極的に使用
- 非同期処理には`asyncio`を使用
- CLI 実装には`click`を使用

## 避けるべきパターン

- `from module import *`の使用
- 過度に長い関数（50 行以上）
- 深いネスト（3 レベル以上）
- マジックナンバーの使用
- 例外の無視（`except: pass`）
- 変数名の省略（`x`, `data`, `temp`など）

## ツール設定

- `mypy`で型チェック
- `pytest`でテスト実行
