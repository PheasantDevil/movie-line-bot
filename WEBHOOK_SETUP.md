# Webhookサーバーのセットアップガイド

このガイドでは、LINE Webhookサーバーをデプロイして、LINEグループでの映画検索機能を有効にする方法を説明します。

## 概要

このシステムは2つの主要な機能で構成されています：

1. **週次通知（GitHub Actions）**: 毎日日本時間9時に過去1週間と先1週間の映画情報をLINEに通知
2. **Webhook機能（常時起動サーバー）**: LINEからのメッセージに反応して映画情報を検索・返信

## Webhookサーバーのデプロイ

### オプション1: Render.comにデプロイ（推奨・無料枠あり）

1. [Render.com](https://render.com/)にアカウントを作成

2. 新しいWeb Serviceを作成
   - GitHubリポジトリを接続
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.webhook_server:app`

3. 環境変数を設定
   ```
   LINE_CHANNEL_ACCESS_TOKEN=<your_token>
   LINE_USER_ID=<your_user_id>
   LINE_CHANNEL_SECRET=<your_channel_secret>
   ```

4. デプロイ完了後、WebhookのURLをコピー（例: `https://your-app.onrender.com/webhook`）

### オプション2: Railway.appにデプロイ（無料枠あり）

1. [Railway.app](https://railway.app/)にアカウントを作成

2. 新しいプロジェクトを作成し、GitHubリポジトリを接続

3. 環境変数を設定（上記と同じ）

4. デプロイ完了後、WebhookのURLをコピー

### オプション3: Herokuにデプロイ

1. [Heroku](https://heroku.com/)にアカウントを作成

2. Heroku CLIをインストール

3. デプロイコマンド
   ```bash
   heroku create your-app-name
   heroku config:set LINE_CHANNEL_ACCESS_TOKEN=<your_token>
   heroku config:set LINE_USER_ID=<your_user_id>
   heroku config:set LINE_CHANNEL_SECRET=<your_channel_secret>
   git push heroku main
   ```

4. WebhookのURLは `https://your-app-name.herokuapp.com/webhook`

## LINE DevelopersでWebhook URLを設定

1. [LINE Developers Console](https://developers.line.biz/console/)にログイン

2. チャネルを選択し、「Messaging API設定」タブを開く

3. 「Webhook URL」にデプロイしたサーバーのURLを入力
   - 例: `https://your-app.onrender.com/webhook`

4. 「Webhookの利用」をオンにする

5. 「接続確認」ボタンをクリックして接続をテスト

## LINE_CHANNEL_SECRETの取得方法

1. LINE Developers Consoleでチャネルを選択

2. 「Basic settings」タブを開く

3. 「Channel secret」をコピー

4. デプロイしたサーバーの環境変数に追加
   ```
   LINE_CHANNEL_SECRET=<your_channel_secret>
   ```

## 使用方法

### 週次通知（自動）

- 毎日日本時間9時に自動で過去1週間と先1週間の映画情報が通知されます
- GitHub Actionsが自動実行します

### 映画検索（手動）

1. LINE Botをグループまたはトークルームに追加

2. 映画のタイトルを入力
   ```
   君の名は。
   ```

3. Botが該当する映画情報を返信
   ```
   🎬 検索結果 (1件)
   ==============================
   
   【1】君の名は。
   公開日: 8月26日
   上映館数: 300館
   詳細: https://eiga.com/movie/...
   ```

## トラブルシューティング

### Webhookが動作しない

1. LINE Developers ConsoleでWebhook URLが正しく設定されているか確認
2. サーバーのログを確認（Render/Railway/Herokuのダッシュボード）
3. 環境変数が正しく設定されているか確認

### 署名検証エラー

1. `LINE_CHANNEL_SECRET`が正しく設定されているか確認
2. 環境変数に余分なスペースや改行がないか確認

### サーバーが起動しない

1. `requirements.txt`のパッケージが正しくインストールされているか確認
2. Procfileが正しく設定されているか確認
3. サーバーのログでエラーメッセージを確認

## コスト

- **GitHub Actions**: 無料枠内（月2,000分）
- **Render.com**: 無料枠あり（750時間/月のスリープ時間あり）
- **Railway.app**: 無料枠あり（$5相当/月）
- **Heroku**: 有料プランが必要（$5/月〜）

推奨: Render.comの無料枠を使用することで、完全無料で運用可能です。

## 注意事項

- 無料プランの場合、サーバーが一定時間アクセスがないとスリープする場合があります
- スリープ状態からの復帰には数秒〜数十秒かかる場合があります
- 24時間365日稼働が必要な場合は、有料プランの使用を検討してください

## セキュリティ

- 環境変数は必ずサーバーの環境変数として設定し、コードにハードコードしないでください
- LINE_CHANNEL_SECRETを使用してWebhook署名を検証しているため、不正なリクエストは自動的に拒否されます

