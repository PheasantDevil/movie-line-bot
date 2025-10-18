# Webhook サーバーのセットアップガイド

このガイドでは、LINE Webhook サーバーをデプロイして、LINE グループでの映画検索機能を有効にする方法を説明します。

## 概要

このシステムは 2 つの主要な機能で構成されています：

1. **週次通知（GitHub Actions）**: 毎日日本時間 9 時に過去 1 週間と先 1 週間の映画情報を LINE に通知
2. **Webhook 機能（常時起動サーバー）**: LINE からのメッセージに反応して映画情報を検索・返信

## Webhook サーバーのデプロイ

### オプション 1: Render.com にデプロイ（推奨・無料枠あり）

1. [Render.com](https://render.com/)にアカウントを作成

2. 新しい Web Service を作成

   - GitHub リポジトリを接続
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.webhook_server:app`

3. 環境変数を設定

   ```
   LINE_CHANNEL_ACCESS_TOKEN=<your_token>
   LINE_USER_ID=<your_user_id>
   LINE_CHANNEL_SECRET=<your_channel_secret>
   ```

4. デプロイ完了後、Webhook の URL をコピー（例: `https://your-app.onrender.com/webhook`）

### オプション 2: Railway.app にデプロイ（無料枠あり）

1. [Railway.app](https://railway.app/)にアカウントを作成

2. 新しいプロジェクトを作成し、GitHub リポジトリを接続

3. 環境変数を設定（上記と同じ）

4. デプロイ完了後、Webhook の URL をコピー

### オプション 3: Heroku にデプロイ

1. [Heroku](https://heroku.com/)にアカウントを作成

2. Heroku CLI をインストール

3. デプロイコマンド

   ```bash
   heroku create your-app-name
   heroku config:set LINE_CHANNEL_ACCESS_TOKEN=<your_token>
   heroku config:set LINE_USER_ID=<your_user_id>
   heroku config:set LINE_CHANNEL_SECRET=<your_channel_secret>
   git push heroku main
   ```

4. Webhook の URL は `https://your-app-name.herokuapp.com/webhook`

## LINE Developers で Webhook URL を設定

1. [LINE Developers Console](https://developers.line.biz/console/)にログイン

2. チャネルを選択し、「Messaging API 設定」タブを開く

3. 「Webhook URL」にデプロイしたサーバーの URL を入力

   - 例: `https://your-app.onrender.com/webhook`

4. 「Webhook の利用」をオンにする

5. 「接続確認」ボタンをクリックして接続をテスト

## LINE_CHANNEL_SECRET の取得方法

1. LINE Developers Console でチャネルを選択

2. 「Basic settings」タブを開く

3. 「Channel secret」をコピー

4. デプロイしたサーバーの環境変数に追加
   ```
   LINE_CHANNEL_SECRET=<your_channel_secret>
   ```

## 使用方法

### 週次通知（自動）

- 毎日日本時間 9 時に自動で過去 1 週間と先 1 週間の映画情報が通知されます
- GitHub Actions が自動実行します

### 映画検索（手動）

1. LINE Bot をグループまたはトークルームに追加

2. 映画のタイトルを入力

   ```
   君の名は。
   ```

3. Bot が該当する映画情報を返信

   ```
   🎬 検索結果 (1件)
   ==============================

   【1】君の名は。
   公開日: 8月26日
   上映館数: 300館
   詳細: https://eiga.com/movie/...
   ```

## トラブルシューティング

### Webhook が動作しない

1. LINE Developers Console で Webhook URL が正しく設定されているか確認
2. サーバーのログを確認（Render/Railway/Heroku のダッシュボード）
3. 環境変数が正しく設定されているか確認

### 署名検証エラー

1. `LINE_CHANNEL_SECRET`が正しく設定されているか確認
2. 環境変数に余分なスペースや改行がないか確認

### サーバーが起動しない

1. `requirements.txt`のパッケージが正しくインストールされているか確認
2. Procfile が正しく設定されているか確認
3. サーバーのログでエラーメッセージを確認

## コスト

- **GitHub Actions**: 無料枠内（月 2,000 分）
- **Render.com**: 無料枠あり（750 時間/月のスリープ時間あり）
- **Railway.app**: 無料枠あり（$5 相当/月）
- **Heroku**: 有料プランが必要（$5/月〜）

推奨: Render.com の無料枠を使用することで、完全無料で運用可能です。

## 注意事項

- 無料プランの場合、サーバーが一定時間アクセスがないとスリープする場合があります
- スリープ状態からの復帰には数秒〜数十秒かかる場合があります
- 24 時間 365 日稼働が必要な場合は、有料プランの使用を検討してください

## セキュリティ

- 環境変数は必ずサーバーの環境変数として設定し、コードにハードコードしないでください
- LINE_CHANNEL_SECRET を使用して Webhook 署名を検証しているため、不正なリクエストは自動的に拒否されます
