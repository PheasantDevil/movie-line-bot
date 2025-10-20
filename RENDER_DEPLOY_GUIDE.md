# 🚀 Render.com デプロイガイド（即実行可能版）

このガイドに従ってWebhookサーバーをデプロイしてください。

## ✅ 準備完了している項目

- ✅ GitHub Secrets登録完了（3つ全て）
  - `LINE_CHANNEL_ACCESS_TOKEN`
  - `LINE_USER_ID`
  - `LINE_CHANNEL_SECRET`
- ✅ デプロイ設定ファイル作成完了
  - `Procfile`
  - `render.yaml`
- ✅ リッチメニュー設定完了

---

## 🌐 Render.comデプロイ手順（10分）

### ステップ 1: Render.comアカウント作成

1. ブラウザで [https://render.com/](https://render.com/) を開く
2. 右上の **「Get Started」** をクリック
3. **「Sign up with GitHub」** を選択
4. GitHubで認証（movie-line-botリポジトリへのアクセスを許可）

### ステップ 2: 新しいWebサービスの作成

1. Render.comダッシュボードが表示される
2. 左メニューまたは右上の **「New +」** をクリック
3. **「Web Service」** を選択

### ステップ 3: リポジトリの接続

1. **「Build and deploy from a Git repository」** を選択
2. **「Next」** をクリック
3. リポジトリリストから **`PheasantDevil/movie-line-bot`** を探す
4. 右側の **「Connect」** ボタンをクリック

**リポジトリが見つからない場合**:
- **「Configure account」** をクリック
- GitHubでRender.comにリポジトリアクセス権限を付与

### ステップ 4: サービス設定（コピー＆ペースト）

以下をそのまま入力してください：

#### Name
```
movie-line-bot-webhook
```

#### Region
```
Singapore (Southeast Asia)
```

#### Branch
```
main
```

#### Root Directory
```
（空欄のまま）
```

#### Runtime
```
Python 3
```
（自動検出されるのでそのまま）

#### Build Command
```
pip install -r requirements.txt
```

#### Start Command
```
gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app
```

### ステップ 5: プラン選択

**Instance Type**:
- **「Free」** を選択（月$0）

### ステップ 6: 環境変数の設定

**Advanced** ボタンをクリックして展開

**Environment Variables** セクションで **「Add Environment Variable」** を3回クリック：

#### 環境変数 1
```
Key: LINE_CHANNEL_ACCESS_TOKEN
Value: MR06P0Ijv3fqJndlrdhldw2mUq6dBVlbB67V/2gDWEDNrscwB+isZsKUtflzzlKmubUxHbfXa6dExOmwsG+UvZxYGHhoIMYlGdzpFIbOONykXGB4rn7c197li2tjC3kmpKRhOj9bxne39uFq3ZTuqwdB04t89/1O/w1cDnyilFU=
```

#### 環境変数 2
```
Key: LINE_USER_ID
Value: U7d4c46cc2c1894692f0dc35efaa1495b
```

#### 環境変数 3
```
Key: LINE_CHANNEL_SECRET
Value: 870064a9ef364643a724fe399625e30e
```

### ステップ 7: デプロイ実行

1. 全ての設定を確認
2. 画面下部の **「Create Web Service」** をクリック
3. デプロイが開始されます

---

## 📊 デプロイ状況の確認（5-10分）

**Logs** タブで進行状況を確認できます。以下のようなログが表示されます：

```
Oct 20 11:30:01 AM  ==> Cloning from https://github.com/PheasantDevil/movie-line-bot...
Oct 20 11:30:05 AM  ==> Running build command 'pip install -r requirements.txt'...
Oct 20 11:30:15 AM  ==> Successfully installed beautifulsoup4-4.14.2 flask-3.1.2 ...
Oct 20 11:30:16 AM  ==> Build successful 🎉
Oct 20 11:30:17 AM  ==> Starting service with 'gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app'
Oct 20 11:30:18 AM  ==> [INFO] Starting gunicorn 23.0.0
Oct 20 11:30:18 AM  ==> [INFO] Listening at: http://0.0.0.0:10000
Oct 20 11:30:18 AM  ==> Your service is live 🎉
```

**「Your service is live 🎉」** が表示されたらデプロイ成功です！

---

## 🔗 ステップ 8: Webhook URLの設定

### A. Render.comのURLを確認

画面上部にサービスのURLが表示されています：
```
https://movie-line-bot-webhook-xxxx.onrender.com
```

**このURLをコピーしてください。**

### B. LINE DevelopersでWebhook URLを設定

1. [LINE Developers Console](https://developers.line.biz/console/)を開く
2. チャネルを選択
3. **「Messaging API設定」** タブをクリック
4. **「Webhook設定」** セクションを探す
5. **「Webhook URL」** の **「編集」** をクリック
6. 以下のように入力（末尾に`/webhook`を追加）：
   ```
   https://movie-line-bot-webhook-xxxx.onrender.com/webhook
   ```
7. **「更新」** をクリック
8. **「検証」** ボタンをクリック
9. ✅ **「成功」** と表示されることを確認

### C. Webhook機能の有効化

同じページで：
1. **「Webhookの利用」** を **ON** にする
2. **「応答メッセージ」** を **OFF** にする（重要）
3. **「Greeting messages」** を **OFF** にする（重要）

---

## 🎉 完了！動作確認

### 1. リッチメニューの確認

LINEアプリでBotのトーク画面を開く：
- ✅ 画面下部に4つのボタンメニューが表示

### 2. Quick Replyの確認

1. Botに「テスト」と送信
2. Botから返信が来る
3. ✨ **返信メッセージの上部に4つのボタンが表示される**

### 3. 各機能のテスト

- 🎬 **映画検索**: ボタンタップ → 映画名入力 → 検索結果表示
- 🎪 **映画館検索**: ボタンタップ → 映画館名入力 → Google検索
- 📅 **今週公開**: ボタンタップ → 即座に一覧表示
- 🎭 **上映中**: ボタンタップ → 即座に一覧表示

---

## 🔧 トラブルシューティング

### デプロイが失敗する

**Logsタブでエラーを確認**:
- ModuleNotFoundError → requirements.txtを確認
- Port binding error → Start Commandを確認
- Environment variable error → 環境変数を確認

### Webhook検証が失敗する

1. URLを確認: 末尾が `/webhook` になっているか
2. サーバーを確認:
   ```
   curl https://your-app-name.onrender.com/health
   ```
3. 環境変数を確認: LINE_CHANNEL_SECRETが正しいか

### Quick Replyが表示されない

- Webhookの利用がONになっているか確認
- 応答メッセージがOFFになっているか確認
- LINEアプリを再起動

---

## 📝 次のステップ

デプロイが完了したら：
1. 全ての機能をテスト
2. 毎週水曜9時の自動通知を待つ（またはGitHub Actionsで手動実行）
3. 必要に応じて機能を拡張

**Happy Deploying! 🚀**

