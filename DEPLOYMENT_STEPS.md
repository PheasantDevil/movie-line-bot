# 🚀 Webhookサーバー デプロイ手順書

このガイドに従って、Render.comにWebhookサーバーをデプロイします。

## 📋 事前準備

### 必要な情報

以下の3つの環境変数が必要です：

1. **LINE_CHANNEL_ACCESS_TOKEN**（既に取得済み）
   ```
   MR06P0Ijv3fqJndlrdhldw2mUq6dBVlbB67V/2gDWEDNrscwB+isZsKUtflzzlKmubUxHbfXa6dExOmwsG+UvZxYGHhoIMYlGdzpFIbOONykXGB4rn7c197li2tjC3kmpKRhOj9bxne39uFq3ZTuqwdB04t89/1O/w1cDnyilFU=
   ```

2. **LINE_USER_ID**（既に取得済み）
   ```
   U7d4c46cc2c1894692f0dc35efaa1495b
   ```

3. **LINE_CHANNEL_SECRET**（要取得）
   - [LINE Developers Console](https://developers.line.biz/console/) > チャネル選択
   - **「チャネル基本設定」**タブ
   - **「チャネルシークレット」**をコピー

---

## 🌐 Render.comへのデプロイ

### ステップ 1: Render.comアカウント作成

1. ブラウザで [https://render.com/](https://render.com/) にアクセス
2. 右上の **「Get Started」** または **「Sign Up」** をクリック
3. **「Sign up with GitHub」** を選択
4. GitHubアカウントで認証・ログイン

### ステップ 2: 新しいWebサービスの作成

1. Render.comダッシュボードが表示されます
2. 右上の **「New +」** ボタンをクリック
3. ドロップダウンから **「Web Service」** を選択

### ステップ 3: GitHubリポジトリの接続

1. **「Build and deploy from a Git repository」** を選択
2. **「Next」** をクリック
3. GitHubリポジトリのリストが表示されます
4. **`movie-line-bot`** を探してクリック
5. **「Connect」** ボタンをクリック

リポジトリが見つからない場合：
- **「Configure account」** をクリック
- GitHubで権限を付与

### ステップ 4: サービス設定の入力

以下の情報を正確に入力してください：

#### Name（サービス名）
```
movie-line-bot-webhook
```

#### Region（リージョン）
```
Singapore (Southeast Asia)
```
または最寄りのリージョンを選択

#### Branch（ブランチ）
```
main
```

#### Root Directory（ルートディレクトリ）
```
（空欄のまま）
```

#### Runtime（ランタイム）
```
Python 3
```
自動検出されるので、そのままでOK

#### Build Command（ビルドコマンド）
```
pip install -r requirements.txt
```

#### Start Command（起動コマンド）
```
gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app
```

### ステップ 5: プランの選択

#### Instance Type（インスタンスタイプ）

**「Free」** を選択してください（無料プラン）

**Free プランの特徴**:
- ✅ 月750時間まで無料
- ⚠️ 非アクティブ時に自動スリープ（15分後）
- ⚠️ 初回アクセス時のコールドスタート（数秒の遅延）

### ステップ 6: 環境変数の設定（重要）

**Advanced** セクションを展開します。

**Environment Variables** セクションで **「Add Environment Variable」** を3回クリックして以下を追加：

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

#### 環境変数 3（⚠️ 要取得）
```
Key: LINE_CHANNEL_SECRET
Value: （LINE Developersコンソールから取得したチャネルシークレット）
```

**LINE_CHANNEL_SECRETの取得方法**:
1. [LINE Developers Console](https://developers.line.biz/console/)
2. チャネルを選択
3. **「チャネル基本設定」** タブ
4. **「チャネルシークレット」** の右側にある **「表示」** をクリック
5. 表示された文字列をコピー

### ステップ 7: デプロイの実行

1. すべての設定を再確認
2. 画面下部の **「Create Web Service」** ボタンをクリック
3. デプロイが開始されます

### ステップ 8: デプロイ状況の確認

**Logs** タブで進行状況を確認できます：

```
==> Cloning from https://github.com/PheasantDevil/movie-line-bot...
==> Checked out commit abc123
==> Running build command 'pip install -r requirements.txt'...
==> Collecting requests>=2.31.0
==> Collecting beautifulsoup4>=4.12.0
==> ... (依存関係のインストール)
==> Successfully installed ...
==> Build successful 🎉
==> Starting service with 'gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app'
==> [2025-10-19 12:00:00 +0000] [1] [INFO] Starting gunicorn 23.0.0
==> [2025-10-19 12:00:00 +0000] [1] [INFO] Listening at: http://0.0.0.0:10000
==> Your service is live 🎉
```

**「Your service is live」** が表示されたらデプロイ成功です！

### ステップ 9: Webhook URLの確認

画面上部にサービスのURLが表示されます：

```
https://movie-line-bot-webhook.onrender.com
```

このURLをコピーしてください。

---

## 🔗 LINE Developersでの設定

### ステップ 10: Webhook URLの設定

1. [LINE Developers Console](https://developers.line.biz/console/) にアクセス
2. チャネルを選択
3. **「Messaging API設定」** タブをクリック
4. **「Webhook設定」** セクションを探す
5. **「Webhook URL」** の **「編集」** をクリック
6. 以下のURLを入力：
   ```
   https://movie-line-bot-webhook.onrender.com/webhook
   ```
   ⚠️ 末尾の `/webhook` を忘れずに！

7. **「更新」** をクリック
8. **「検証」** ボタンをクリック
9. **「成功」** と表示されることを確認 ✅

### ステップ 11: Webhook機能の有効化

同じ「Messaging API設定」タブで：

1. **「Webhookの利用」** を **ON** にする
2. **「応答メッセージ」** を **OFF** にする（重要）
3. **「Greeting messages」** を **OFF** にする（重要）

---

## ✅ 動作確認チェックリスト

### 1. Render.comでの確認

```bash
# ヘルスチェック
curl https://your-app-name.onrender.com/health
# 応答: OK
```

### 2. LINEアプリでの確認

#### リッチメニュー
- [ ] LINEアプリでBotのトーク画面を開く
- [ ] 画面下部に4つのボタンメニューが表示される
- [ ] 各ボタンをタップして反応することを確認

#### Quick Reply
- [ ] Botに何かメッセージを送信（例: "テスト"）
- [ ] Botから返信が来る
- [ ] 返信メッセージの上部に4つのボタンが表示される
- [ ] ボタンをタップして動作することを確認

#### 各機能のテスト
- [ ] 🎬 映画検索：映画名入力 → 検索結果表示
- [ ] 🎪 映画館検索：映画館名入力 → 検索ボタン表示
- [ ] 📅 今週公開：即座に一覧表示
- [ ] 🎭 上映中：即座に一覧表示

---

## 🔧 トラブルシューティング

### エラー: "Build failed"

**Logsを確認**:
```
==> ERROR: Could not find a version that satisfies the requirement...
```

**解決策**: `requirements.txt`を確認

### エラー: "Application failed to start"

**よくある原因**:
1. Start Commandが間違っている
2. 環境変数が設定されていない

**解決策**: Render.comダッシュボードで設定を確認

### Webhook検証が失敗

**症状**: LINE Developersで「検証」ボタンをクリックしても失敗

**解決策**:
1. URLを確認: `https://your-app-name.onrender.com/webhook`
2. サーバーが起動しているか確認
3. `LINE_CHANNEL_SECRET`が正しく設定されているか確認

---

## 📝 デプロイ後にやること

### 1. ログの確認

Render.comダッシュボード > サービス > **Logs** タブで：
- サーバーが正常に起動しているか確認
- エラーがないか確認

### 2. LINEでテスト

1. LINEアプリでBotのトーク画面を開く
2. 何かメッセージを送信
3. Render.comのLogsで受信を確認
4. Quick Replyが表示されることを確認

---

## 💡 次のステップ

デプロイが完了したら、以下を確認してください：

1. **リッチメニュー**: 画面下部に表示 ✅
2. **Quick Reply**: メッセージ上部に表示（Webhook経由）
3. **週次通知**: 毎週水曜9時に自動配信（GitHub Actions）

---

それでは、以下の手順で進めてください：

1. **LINE_CHANNEL_SECRETを取得**
2. **Render.comでアカウント作成**（GitHubアカウントで）
3. **上記の手順に従ってデプロイ**

進行中に問題が発生したら、エラーメッセージを教えてください！

変更をコミットしておきます。

<function_calls>
<invoke name="run_terminal_cmd">
<parameter name="command">cd /Users/Work/movie-line-bot && git checkout -b deploy/render-config
