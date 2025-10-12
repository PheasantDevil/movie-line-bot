# 💻 開発ガイド

ローカル環境での開発・テスト方法を説明します。

## 開発環境のセットアップ

### 前提条件

- Python 3.11 以上
- Git
- テキストエディタ（VS Code 推奨）

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot
```

### 2. 仮想環境の作成

```bash
# Python仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

```bash
# .envファイルを作成（開発用）
cat > .env << EOF
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_USER_ID=your_user_id_here
EOF
```

**注意**: `.env`ファイルは`.gitignore`に含まれているため、Git にコミットされません。

## 開発ワークフロー

### ブランチ戦略

```bash
# 新機能の開発
git checkout -b feature/new-feature

# バグ修正
git checkout -b fix/bug-description

# ドキュメント更新
git checkout -b docs/update-readme
```

### コミットメッセージ規約

```bash
# 機能追加
git commit -m "✨ Add: 新機能の説明"

# バグ修正
git commit -m "🐛 Fix: バグの説明"

# ドキュメント
git commit -m "📝 Docs: ドキュメントの更新"

# リファクタリング
git commit -m "♻️ Refactor: リファクタリング内容"

# テスト
git commit -m "✅ Test: テストの追加"
```

## 各モジュールのテスト

### 1. スクレイパーのテスト

```bash
python src/scraper.py
```

**期待される出力**:

```
映画情報のスクレイピングを開始します...
映画情報を取得中: https://eiga.com/movie/
✓ 28件の映画情報を取得しました

取得した映画数: 28

--- 映画 1 ---
タイトル: 映画タイトル
公開日: 10月10日
URL: https://eiga.com/movie/12345/
...
```

### 2. ストレージのテスト

```bash
python src/storage.py
```

**期待される出力**:

```
データ永続化機能のテスト...

1. 保存テスト
✓ 2件の映画情報を保存しました: data/movies.json

2. 読み込みテスト
✓ 前回のデータを読み込みました: 2件（最終更新: ...）
...
```

### 3. 差分検知のテスト

```bash
python src/diff_detector.py
```

### 4. LINE 通知のテスト

```bash
# 環境変数を設定してから実行
export LINE_CHANNEL_ACCESS_TOKEN="your_token"
export LINE_USER_ID="your_user_id"

python src/line_notifier.py
```

### 5. 統合テスト

```bash
# メインスクリプトを実行
python src/main.py
```

## デバッグ

### VS Code デバッグ設定

`.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/src/main.py",
      "console": "integratedTerminal",
      "env": {
        "LINE_CHANNEL_ACCESS_TOKEN": "your_token",
        "LINE_USER_ID": "your_user_id"
      }
    }
  ]
}
```

### ログ出力の追加

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
```

## コードスタイル

### フォーマッター（推奨）

```bash
# Blackのインストール
pip install black

# フォーマット実行
black src/

# チェックのみ
black --check src/
```

### Linter（推奨）

```bash
# Flake8のインストール
pip install flake8

# Lint実行
flake8 src/
```

### Import 順序

PEP 8 に従い、以下の順序でインポート：

```python
# 1. 標準ライブラリ
import os
import sys
from datetime import datetime

# 2. サードパーティライブラリ
import requests
from bs4 import BeautifulSoup

# 3. ローカルモジュール
from scraper import MovieScraper
from storage import MovieStorage
```

## トラブルシューティング

### よくある問題

#### 1. `ModuleNotFoundError`

```bash
# 解決方法：依存関係を再インストール
pip install -r requirements.txt
```

#### 2. `LINE通知が届かない`

```bash
# トークンとUser IDを確認
echo $LINE_CHANNEL_ACCESS_TOKEN
echo $LINE_USER_ID

# テストスクリプトで確認
python src/line_notifier.py
```

#### 3. `スクレイピングが失敗する`

```bash
# ネットワーク接続を確認
curl -I https://eiga.com/movie/

# User-Agentを変更してテスト
# src/scraper.py の User-Agent を修正
```

## テストデータの生成

### ダミーデータでテスト

```python
# test_data.py
test_movies = [
    {
        'title': 'テスト映画1',
        'url': 'https://eiga.com/movie/12345/',
        'release_date': '10月10日',
        'thumbnail': 'https://example.com/image1.jpg',
        'scraped_at': '2025-10-12T10:00:00'
    },
    # ... 追加のテストデータ
]

from storage import MovieStorage
storage = MovieStorage()
storage.save_movies(test_movies)
```

## パフォーマンス測定

### 実行時間の計測

```python
import time

start = time.time()
# 処理
end = time.time()

print(f"実行時間: {end - start:.2f}秒")
```

### プロファイリング

```bash
# cProfileで詳細分析
python -m cProfile -o profile.stats src/main.py

# 結果の確認
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('time').print_stats(10)"
```

## Git Tips

### 便利なエイリアス

```bash
# .gitconfig に追加
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"
```

### コミット前のチェックリスト

- [ ] コードがフォーマットされている
- [ ] Lint エラーがない
- [ ] テストが通る
- [ ] 不要なデバッグコードを削除
- [ ] コミットメッセージが明確

## CI/CD ローカルテスト

### GitHub Actions をローカルで実行

```bash
# actのインストール（macOS）
brew install act

# ワークフローをローカルで実行
act -j check-and-notify
```

## 本番環境との違い

| 項目       | ローカル            | GitHub Actions |
| ---------- | ------------------- | -------------- |
| OS         | macOS/Windows/Linux | Ubuntu         |
| Python     | システムの Python   | Python 3.11    |
| 環境変数   | .env または export  | GitHub Secrets |
| データ保存 | ローカルファイル    | Git コミット   |

## 次のステップ

開発環境が整ったら：

1. [実装詳細](implementation_details.md)で内部構造を理解
2. [技術仕様書](technical_specifications.md)で API 仕様を確認
3. 新機能の実装を開始
4. プルリクエストを作成

## 質問やサポート

- GitHub Issues で質問
- Pull Request で改善提案
- ドキュメントの改善も歓迎！
