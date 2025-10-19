# 👨‍💻 開発者ガイド

映画情報LINE Botの開発者向けドキュメントです。

## 📋 目次

- [プロジェクト構造](#プロジェクト構造)
- [コーディング規約](#コーディング規約)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [テストの実行](#テストの実行)
- [デバッグ方法](#デバッグ方法)
- [新機能の追加](#新機能の追加)
- [ベストプラクティス](#ベストプラクティス)

---

## プロジェクト構造

```
movie-line-bot/
├── src/                        # ソースコード
│   ├── main.py                # メイン処理
│   ├── scraper.py             # スクレイピング
│   ├── line_notifier.py       # LINE通知
│   ├── webhook_server.py      # Webhookサーバー
│   ├── session_manager.py     # セッション管理
│   ├── rich_menu_manager.py   # リッチメニュー管理
│   ├── movie_theater_search.py # 映画館検索
│   ├── storage.py             # データ永続化
│   ├── weekly_new_movies.py   # 今週公開映画通知
│   └── weekly_now_showing.py  # 上映中映画通知
├── tools/                      # 開発ツール
│   ├── generate_rich_menu_image.py
│   └── setup_rich_menu.py
├── .github/workflows/          # GitHub Actions
│   └── weekly-notifications.yml
├── assets/                     # 静的ファイル
│   └── rich_menu.png
├── data/                       # データファイル
│   ├── movies.json
│   └── sessions.json
├── docs/                       # ドキュメント
│   ├── API_REFERENCE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── LINE_API_CAPABILITIES.md
│   └── ...
├── requirements.txt            # Python依存関係
├── Procfile                    # Webサーバー起動設定
└── README.md                   # プロジェクト説明
```

### モジュールの役割

| モジュール | 役割 | 依存関係 |
|-----------|------|---------|
| `scraper.py` | 映画情報スクレイピング | requests, BeautifulSoup |
| `line_notifier.py` | LINE通知 | requests |
| `webhook_server.py` | Webhookサーバー | Flask, 全モジュール |
| `session_manager.py` | セッション管理 | なし |
| `rich_menu_manager.py` | リッチメニュー管理 | requests |
| `movie_theater_search.py` | 映画館検索 | urllib |
| `storage.py` | データ永続化 | json |

---

## コーディング規約

### Pythonスタイルガイド

このプロジェクトは[PEP 8](https://pep8-ja.readthedocs.io/ja/latest/)に準拠しています。

#### 命名規則

```python
# クラス名: PascalCase
class MovieScraper:
    pass

# 関数名・変数名: snake_case
def fetch_upcoming_movies():
    movie_title = "..."

# 定数: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.line.me"

# プライベートメソッド: _prefix
def _parse_html(self, html):
    pass
```

#### インポート順序

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
from line_notifier import LineNotifier
```

#### docstring

```python
def fetch_upcoming_movies(self) -> List[Dict]:
    """
    今週公開予定の映画情報を取得
    
    Returns:
        List[Dict]: 映画情報のリスト
    """
    pass
```

#### 型ヒント

```python
from typing import List, Dict, Optional

def search_movie(keyword: str) -> List[Dict]:
    pass

def get_user_state(user_id: str) -> Optional[str]:
    pass
```

### エラーハンドリング

```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"エラー: {e}")
    import traceback
    traceback.print_exc()
    return []
```

---

## 開発環境のセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot
```

### 2. 仮想環境の作成

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 開発用の追加パッケージ

```bash
# リッチメニュー画像生成用
pip install pillow

# コードフォーマッター
pip install black flake8

# 型チェッカー
pip install mypy
```

### 5. 環境変数の設定

```bash
# .envファイルを作成
cat > .env << EOF
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_USER_ID=your_user_id_here
LINE_CHANNEL_SECRET=your_secret_here
EOF

# 環境変数を読み込み
export $(cat .env | xargs)
```

---

## テストの実行

### 単体テスト

各モジュールには`__main__`セクションにテスト関数があります。

```bash
# スクレイパーのテスト
python src/scraper.py

# セッション管理のテスト
python src/session_manager.py

# 映画館検索のテスト
python src/movie_theater_search.py
```

### 週次通知のテスト

```bash
# 今週公開映画通知のテスト
python src/weekly_new_movies.py --test

# 上映中映画通知のテスト
python src/weekly_now_showing.py --test
```

### Webhookサーバーのテスト

```bash
# ローカルでサーバーを起動
python src/webhook_server.py

# 別のターミナルでテスト
curl http://localhost:5000/health
```

### リッチメニューのテスト

```bash
# 環境変数を設定
export LINE_CHANNEL_ACCESS_TOKEN='your_token'

# リッチメニューのテスト
python src/rich_menu_manager.py
```

---

## デバッグ方法

### 1. ログ出力

```python
print("=" * 60)
print("デバッグ情報")
print("=" * 60)
print(f"変数の値: {variable}")
```

### 2. トレースバック

```python
import traceback

try:
    # 処理
    pass
except Exception as e:
    print(f"エラー: {e}")
    traceback.print_exc()
```

### 3. pdb（Pythonデバッガー）

```python
import pdb

# ブレークポイントを設定
pdb.set_trace()

# または Python 3.7+
breakpoint()
```

### 4. Webhookのデバッグ

#### ローカル環境でngrokを使用

```bash
# ngrokをインストール
brew install ngrok  # macOS
# または https://ngrok.com/download

# Flaskサーバーを起動
python src/webhook_server.py

# 別のターミナルでngrokを起動
ngrok http 5000

# 表示されたURLをLINE DevelopersコンソールのWebhook URLに設定
# 例: https://xxxx-xxxx-xxxx.ngrok.io/webhook
```

#### Render.comのログ確認

```bash
# Render.comのダッシュボード > サービス > Logs
```

---

## 新機能の追加

### 1. 新しい通知機能の追加

#### ステップ 1: スクリプトの作成

```python
# src/new_notification.py
import os
from line_notifier import LineNotifier
from scraper import MovieScraper

def main():
    """新しい通知のメイン処理"""
    scraper = MovieScraper()
    movies = scraper.fetch_some_movies()
    
    notifier = LineNotifier()
    notifier.send_new_notification(movies)

if __name__ == "__main__":
    main()
```

#### ステップ 2: LineNotifierにメソッド追加

```python
# src/line_notifier.py
def send_new_notification(self, movies: List[Dict]) -> bool:
    """新しい通知を送信"""
    message = self._format_new_notification_message(movies)
    return self.send_text_message(message)

def _format_new_notification_message(self, movies: List[Dict]) -> str:
    """新しい通知メッセージを整形"""
    lines = []
    lines.append("🎬 新しい通知")
    # メッセージ作成
    return "\n".join(lines)
```

#### ステップ 3: GitHub Actionsワークフロー追加

```yaml
# .github/workflows/new-notification.yml
name: 新しい通知

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python src/new_notification.py
        env:
          LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
          LINE_USER_ID: ${{ secrets.LINE_USER_ID }}
```

### 2. Webhookハンドラーの追加

```python
# src/webhook_server.py
def handle_new_postback(event: dict, notifier: LineNotifier):
    """新しいPostbackイベントを処理"""
    reply_token = event['replyToken']
    postback_data = event['postback']['data']
    
    if postback_data == 'action=new_feature':
        # 新機能の処理
        notifier.reply_text_message(reply_token, "新機能です")
```

### 3. リッチメニューボタンの追加

```python
# src/rich_menu_manager.py
def create_extended_menu(self) -> str:
    """拡張リッチメニューを作成"""
    menu_data = {
        'size': {'width': 2500, 'height': 1686},
        'selected': True,
        'name': '拡張メニュー',
        'chatBarText': 'メニュー',
        'areas': [
            # 既存のボタン
            # ...
            # 新しいボタン
            {
                'bounds': {'x': 0, 'y': 1124, 'width': 833, 'height': 562},
                'action': {
                    'type': 'postback',
                    'data': 'action=new_feature',
                    'displayText': '新機能'
                }
            }
        ]
    }
    # 作成処理
```

---

## ベストプラクティス

### 1. 環境変数の管理

```python
import os
from dotenv import load_dotenv

# .envファイルから読み込み（開発環境）
load_dotenv()

token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
if not token:
    raise ValueError("環境変数が設定されていません")
```

### 2. エラーハンドリング

```python
def safe_request(url: str) -> Optional[requests.Response]:
    """安全なHTTPリクエスト"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response
    except requests.Timeout:
        print("タイムアウトしました")
    except requests.RequestException as e:
        print(f"リクエストエラー: {e}")
    return None
```

### 3. データ検証

```python
def validate_movie_data(movie: Dict) -> bool:
    """映画データの妥当性をチェック"""
    required_fields = ['title', 'url', 'release_date']
    return all(field in movie for field in required_fields)
```

### 4. ログ出力

```python
import logging

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# ログ出力
logger.info("処理を開始します")
logger.error(f"エラーが発生しました: {e}")
```

### 5. リトライロジック

```python
import time

def retry_request(url: str, max_retries: int = 3) -> Optional[requests.Response]:
    """リトライ付きリクエスト"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数バックオフ
                print(f"リトライします... ({attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"最大リトライ回数に達しました: {e}")
    return None
```

### 6. セッション管理のパターン

```python
# Webhookハンドラー内で
def handle_text_message(event: dict, notifier: LineNotifier):
    user_id = event['source']['userId']
    text = event['message']['text']
    
    # セッション状態を確認
    state = session_manager.get_user_state(user_id)
    
    if state == 'movie_search':
        # 映画検索処理
        handle_movie_search(text, event['replyToken'], notifier)
        # セッションをクリア
        session_manager.clear_user_state(user_id)
    else:
        # 通常処理
        handle_normal_message(text, event['replyToken'], notifier)
```

### 7. メッセージフォーマット

```python
def format_movie_list(movies: List[Dict], max_count: int = 10) -> str:
    """映画リストを整形"""
    lines = []
    lines.append(f"🎬 映画一覧 ({len(movies)}件)")
    lines.append("=" * 30)
    lines.append("")
    
    for i, movie in enumerate(movies[:max_count], 1):
        lines.append(f"【{i}】{movie['title']}")
        lines.append(f"   公開日: {movie['release_date']}")
        lines.append(f"   {movie['url']}")
        lines.append("")
    
    if len(movies) > max_count:
        lines.append(f"...他 {len(movies) - max_count}件")
    
    return "\n".join(lines)
```

---

## コードレビューチェックリスト

- [ ] PEP 8に準拠している
- [ ] 型ヒントが付いている
- [ ] docstringが書かれている
- [ ] エラーハンドリングが適切
- [ ] テストが実装されている
- [ ] ログ出力が適切
- [ ] 環境変数が適切に管理されている
- [ ] セキュリティ上の問題がない
- [ ] パフォーマンスが最適化されている

---

## トラブルシューティング

### よくある問題

#### 1. ModuleNotFoundError

```bash
# 仮想環境がアクティベートされているか確認
which python

# 依存関係を再インストール
pip install -r requirements.txt
```

#### 2. LINE API エラー

```python
# トークンが正しいか確認
print(f"TOKEN: {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')[:20]}...")

# 署名検証エラー
# LINE_CHANNEL_SECRET が正しく設定されているか確認
```

#### 3. スクレイピングエラー

```python
# eiga.comのHTML構造が変わった可能性
# セレクターを確認・更新
```

---

## 参考リンク

- [LINE Messaging API ドキュメント](https://developers.line.biz/ja/docs/messaging-api/)
- [Flask ドキュメント](https://flask.palletsprojects.com/)
- [Beautiful Soup ドキュメント](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PEP 8 -- Style Guide for Python Code](https://pep8-ja.readthedocs.io/ja/latest/)

---

## 更新履歴

- 2025-10-19: 初版作成

