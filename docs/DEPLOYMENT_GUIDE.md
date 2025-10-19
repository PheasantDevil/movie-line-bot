# 🚀 デプロイガイド

映画情報LINE BotのWebhookサーバーをデプロイする方法を説明します。

## 📋 目次

- [デプロイ先の選択](#デプロイ先の選択)
- [Render.comへのデプロイ（推奨）](#rendercomへのデプロイ推奨)
- [Herokuへのデプロイ](#herokuへのデプロイ)
- [その他のプラットフォーム](#その他のプラットフォーム)
- [トラブルシューティング](#トラブルシューティング)

---

## デプロイ先の選択

| プラットフォーム | 無料枠 | 特徴 | 推奨度 |
|-----------------|--------|------|--------|
| **Render.com** | ✅ あり | シンプル、自動デプロイ | ⭐️⭐️⭐️⭐️⭐️ |
| **Heroku** | ❌ なし（要クレカ） | 豊富な機能 | ⭐️⭐️⭐️ |
| **Railway** | ✅ あり（制限あり） | シンプル | ⭐️⭐️⭐️⭐️ |
| **Fly.io** | ✅ あり | Docker対応 | ⭐️⭐️⭐️ |

---

## Render.comへのデプロイ（推奨）

Render.comは無料枠があり、GitHubと連携した自動デプロイが可能です。

### 前提条件

- GitHubアカウント
- Render.comアカウント（無料）
- 本プロジェクトのGitHubリポジトリ

### ステップ 1: Render.comアカウントの作成

1. [Render.com](https://render.com/)にアクセス
2. **「Get Started」**をクリック
3. GitHubアカウントで登録

### ステップ 2: 新しいWebサービスの作成

1. ダッシュボードで**「New」** > **「Web Service」**を選択
2. GitHubリポジトリを接続
3. リポジトリを選択

### ステップ 3: サービスの設定

#### 基本設定

| 項目 | 値 |
|------|-----|
| **Name** | `movie-line-bot-webhook` |
| **Region** | `Singapore` または最寄りのリージョン |
| **Branch** | `main` |
| **Root Directory** | （空欄）|
| **Runtime** | `Python 3` |

#### ビルド設定

| 項目 | 値 |
|------|-----|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app` |

#### インスタンスタイプ

- **Instance Type**: `Free` を選択

### ステップ 4: 環境変数の設定

**Environment Variables** セクションで以下を追加：

```
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_USER_ID=your_user_id_here
LINE_CHANNEL_SECRET=your_channel_secret_here
```

### ステップ 5: デプロイ

1. **「Create Web Service」**をクリック
2. デプロイが開始されます（5-10分程度）
3. ログを確認してエラーがないことを確認

### ステップ 6: Webhook URLの取得

デプロイ完了後、URLが表示されます：

```
https://movie-line-bot-webhook.onrender.com
```

### ステップ 7: LINE Developersコンソールでの設定

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. チャネルを選択
3. **「Messaging API設定」**タブを開く
4. **「Webhook URL」**に以下を入力：
   ```
   https://your-app-name.onrender.com/webhook
   ```
5. **「検証」**ボタンをクリックして成功を確認
6. **「Webhookの利用」**を**有効**にする

### ステップ 8: 動作確認

1. LINEアプリでBotのトーク画面を開く
2. 何かメッセージを送信
3. Render.comのログで受信を確認

```bash
# Render.comダッシュボード > Logs
受信メッセージ: テスト (ユーザーID: U...)
```

### 無料枠の制限

Render.comの無料枠：
- ✅ 750時間/月のサービス稼働時間
- ✅ 非アクティブ時の自動スリープ（15分後）
- ⚠️ 初回アクセス時のコールドスタート（数秒）

**対策**: 定期的なヘルスチェックで起動状態を維持

```yaml
# .github/workflows/keep-alive.yml
name: Keep Render.com Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # 10分ごと

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - run: curl https://your-app-name.onrender.com/health
```

---

## Herokuへのデプロイ

Herokuは2022年11月から無料プランが廃止されましたが、有料プランでのデプロイ方法を説明します。

### 前提条件

- Herokuアカウント
- Heroku CLI
- クレジットカード（有料プラン）

### ステップ 1: Heroku CLIのインストール

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# https://devcenter.heroku.com/articles/heroku-cli からインストーラーをダウンロード
```

### ステップ 2: Herokuにログイン

```bash
heroku login
```

### ステップ 3: Herokuアプリの作成

```bash
cd movie-line-bot
heroku create movie-line-bot-webhook
```

### ステップ 4: 環境変数の設定

```bash
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token_here
heroku config:set LINE_USER_ID=your_user_id_here
heroku config:set LINE_CHANNEL_SECRET=your_secret_here
```

### ステップ 5: デプロイ

```bash
# Gitリポジトリからデプロイ
git push heroku main

# または特定のブランチをデプロイ
git push heroku your-branch:main
```

### ステップ 6: ログの確認

```bash
heroku logs --tail
```

### ステップ 7: Webhook URLの設定

```
https://your-app-name.herokuapp.com/webhook
```

### 料金

- **Eco Dyno**: $5/月
- **Basic Dyno**: $7/月

---

## その他のプラットフォーム

### Railway

1. [Railway.app](https://railway.app/)にアクセス
2. GitHubリポジトリを接続
3. 環境変数を設定
4. 自動デプロイ

**無料枠**: $5/月のクレジット

### Fly.io

```bash
# Fly.io CLIのインストール
curl -L https://fly.io/install.sh | sh

# ログイン
flyctl auth login

# アプリの作成
flyctl launch

# デプロイ
flyctl deploy
```

**無料枠**: 月間使用量に応じた無料枠あり

### Google Cloud Run

Docker対応が必要。詳細は別途ドキュメント参照。

---

## トラブルシューティング

### デプロイが失敗する

#### エラー: `ModuleNotFoundError`

```bash
# requirements.txtを確認
cat requirements.txt

# 依存関係を更新
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

#### エラー: `PORT環境変数が設定されていない`

Procfileを確認：

```
web: gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app
```

#### エラー: `Start command failed`

ログを確認：

```bash
# Render.com: ダッシュボード > Logs
# Heroku: heroku logs --tail
```

### Webhookが動作しない

#### 症状: 「検証」ボタンで失敗

1. **URLが正しいか確認**
   ```
   https://your-app-name.onrender.com/webhook
   ```

2. **サーバーが起動しているか確認**
   ```bash
   curl https://your-app-name.onrender.com/health
   # 応答: OK
   ```

3. **ログを確認**
   ```bash
   # Render.com: ダッシュボード > Logs
   ```

#### 症状: 署名検証エラー

```bash
# LINE_CHANNEL_SECRETが正しく設定されているか確認
# Render.com: Environment Variables
# Heroku: heroku config
```

#### 症状: 502 Bad Gateway

サーバーがクラッシュしている可能性：

1. ログを確認
2. 依存関係を確認
3. メモリ使用量を確認

### パフォーマンスの問題

#### 症状: レスポンスが遅い

**原因1: コールドスタート**
- 無料プランではアイドル時にスリープ
- 初回アクセス時に起動に時間がかかる

**対策**:
- Keep-Aliveワークフローを追加
- 有料プランにアップグレード

**原因2: スクレイピングが遅い**
- eiga.comへのリクエストに時間がかかる

**対策**:
- キャッシュを実装
- 非同期処理を検討

### メモリ不足

#### エラー: `R14 - Memory quota exceeded`

**対策**:
1. メモリ使用量を最適化
2. 不要なモジュールを削除
3. プランをアップグレード

```python
# メモリ使用量を確認
import psutil
process = psutil.Process()
print(f"メモリ使用量: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

---

## セキュリティのベストプラクティス

### 1. 環境変数の管理

- ❌ `.env`ファイルをGitにコミットしない
- ✅ `.gitignore`に`.env`を追加
- ✅ プラットフォームの環境変数機能を使用

### 2. Webhook署名の検証

```python
# src/webhook_server.py
if notifier.channel_secret and not notifier.verify_signature(body, signature):
    print("署名検証失敗")
    abort(400)
```

### 3. HTTPS通信

- ✅ Render.com、Herokuは自動的にHTTPS対応
- ✅ LINE Webhook URLもHTTPSが必須

### 4. レート制限

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.headers.get('X-Line-Signature', ''),
    default_limits=["100 per minute"]
)
```

---

## モニタリング

### ログの確認

#### Render.com
```
ダッシュボード > サービス > Logs
```

#### Heroku
```bash
heroku logs --tail
heroku logs --tail --app your-app-name
```

### アップタイムモニタリング

無料のアップタイムモニタリングサービス：

- [UptimeRobot](https://uptimerobot.com/)
- [Pingdom](https://www.pingdom.com/)
- [StatusCake](https://www.statuscake.com/)

設定:
- URL: `https://your-app-name.onrender.com/health`
- 間隔: 5-10分

---

## 更新履歴

- 2025-10-19: 初版作成

