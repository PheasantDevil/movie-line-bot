# 🚀 映画情報 LINE Bot セットアップガイド

このガイドでは、映画情報 LINE Bot の完全なセットアップ手順を説明します。

## 📋 目次

1. [前提条件](#前提条件)
2. [LINE Messaging API の設定](#line-messaging-apiの設定)
3. [GitHub リポジトリの設定](#githubリポジトリの設定)
4. [ローカル開発環境のセットアップ](#ローカル開発環境のセットアップ)
5. [リッチメニューの設定](#リッチメニューの設定)
6. [Webhook サーバーのデプロイ](#webhookサーバーのデプロイ)
7. [動作確認](#動作確認)
8. [トラブルシューティング](#トラブルシューティング)

---

## 前提条件

以下のアカウントとツールが必要です：

- ✅ GitHub アカウント
- ✅ LINE アカウント
- ✅ LINE Developers アカウント（無料）
- ✅ Render.com アカウント（無料、Webhook 用）
- ✅ Python 3.11 以上
- ✅ Git

---

## LINE Messaging API の設定

### ステップ 1: LINE Developers コンソールにアクセス

1. [LINE Developers Console](https://developers.line.biz/console/) にアクセス
2. LINE アカウントでログイン

### ステップ 2: プロバイダーの作成

1. **「Create」** または **「新規プロバイダー作成」** をクリック
2. プロバイダー名を入力（例: `My Movie Bot Provider`）
3. **「作成」** をクリック

### ステップ 3: Messaging API チャネルの作成

1. 作成したプロバイダーを選択
2. **「Messaging API」** を選択
3. 以下の情報を入力：
   - **チャネル名**: `映画情報Bot`
   - **チャネル説明**: `新作映画情報を通知するBot`
   - **大業種**: `ニュース/情報`
   - **小業種**: `エンタメ/芸能/音楽`
4. 利用規約に同意して **「作成」** をクリック

### ステップ 4: チャネルアクセストークンの発行

1. 作成したチャネルを開く
2. **「Messaging API 設定」** タブを選択
3. **「チャネルアクセストークン」** セクションで **「発行」** をクリック
4. 表示されたトークンをコピーして安全な場所に保存

**例**:

```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...
```

### ステップ 5: チャネルシークレットの取得

1. **「チャネル基本設定」** タブを選択
2. **「チャネルシークレット」** をコピーして保存

### ステップ 6: Webhook 設定の準備

1. **「Messaging API 設定」** タブに戻る
2. **「Webhook URL」** は後で設定するので、今はスキップ
3. **「Webhook の利用」** を **有効** にする
4. **「応答メッセージ」** を **無効** にする
5. **「Greeting messages」** を **無効** にする（Bot 側で管理）

### ステップ 7: QR コードで友だち追加

1. **「Messaging API 設定」** タブの下部にある QR コードをスキャン
2. 自分の LINE アカウントで友だち追加

### ステップ 8: USER ID の取得

**方法 1: LINE Official Account Manager で確認**

1. [LINE Official Account Manager](https://manager.line.biz/) にアクセス
2. 作成したアカウントを選択
3. **「設定」** > **「アカウント設定」** から確認

**方法 2: Webhook ログから確認**（後で Webhook サーバーを起動後）

1. Bot に何かメッセージを送信
2. サーバーログに表示される `userId` を確認

---

## GitHub リポジトリの設定

### ステップ 1: リポジトリのフォーク/クローン

```bash
# クローン
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot
```

### ステップ 2: GitHub Secrets の設定

1. GitHub リポジトリページにアクセス
2. **Settings** > **Secrets and variables** > **Actions** を開く
3. **「New repository secret」** をクリック

以下の 3 つの Secret を追加：

#### Secret 1: LINE_CHANNEL_ACCESS_TOKEN

- **Name**: `LINE_CHANNEL_ACCESS_TOKEN`
- **Value**: ステップ 4 で取得したチャネルアクセストークン

#### Secret 2: LINE_USER_ID

- **Name**: `LINE_USER_ID`
- **Value**: ステップ 8 で取得した USER ID（例: `U1234567890abcdef...`）

#### Secret 3: LINE_CHANNEL_SECRET

- **Name**: `LINE_CHANNEL_SECRET`
- **Value**: ステップ 5 で取得したチャネルシークレット

### ステップ 3: GitHub Actions の有効化

1. **Actions** タブを開く
2. ワークフローが表示されていることを確認
3. 必要に応じて **「I understand my workflows, go ahead and enable them」** をクリック

---

## ローカル開発環境のセットアップ

### ステップ 1: 仮想環境の作成

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境をアクティベート
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### ステップ 2: 依存関係のインストール

```bash
pip install -r requirements.txt
```

### ステップ 3: 環境変数の設定

```bash
# macOS/Linux
export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'
export LINE_USER_ID='your_user_id_here'
export LINE_CHANNEL_SECRET='your_secret_here'

# Windows (PowerShell)
$env:LINE_CHANNEL_ACCESS_TOKEN='your_token_here'
$env:LINE_USER_ID='your_user_id_here'
$env:LINE_CHANNEL_SECRET='your_secret_here'
```

### ステップ 4: 動作確認

```bash
# 今週公開映画通知のテスト
python src/weekly_new_movies.py --test

# 上映中映画通知のテスト
python src/weekly_now_showing.py --test
```

---

## リッチメニューの設定

### ステップ 1: Pillow のインストール（画像生成用）

```bash
pip install pillow
```

### ステップ 2: リッチメニュー画像の生成

```bash
python tools/generate_rich_menu_image.py
```

生成された画像は `assets/rich_menu.png` に保存されます。

### ステップ 3: リッチメニューの設定

```bash
python tools/setup_rich_menu.py
```

プロンプトに従って設定を完了します。

### ステップ 4: 確認

1. LINE アプリで Bot のトーク画面を開く
2. 画面下部にリッチメニューが表示されることを確認
3. 各ボタンをタップして動作を確認

---

## Webhook サーバーのデプロイ

Webhook サーバーは、ユーザーが Bot に送信したメッセージを受信して処理します。

### オプション 1: Render.com（推奨）

#### ステップ 1: Render.com アカウント作成

1. [Render.com](https://render.com/) にアクセス
2. **「Get Started」** をクリック
3. GitHub アカウントで登録

#### ステップ 2: 新しい Web サービスの作成

1. ダッシュボードで **「New」** > **「Web Service」** を選択
2. GitHub リポジトリを接続
3. 以下の設定を入力：
   - **Name**: `movie-line-bot-webhook`
   - **Region**: `Singapore` または最寄りのリージョン
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.webhook_server:app`

#### ステップ 3: 環境変数の設定

**Environment Variables** セクションで以下を追加：

- `LINE_CHANNEL_ACCESS_TOKEN`: チャネルアクセストークン
- `LINE_USER_ID`: USER ID
- `LINE_CHANNEL_SECRET`: チャネルシークレット

#### ステップ 4: デプロイ

1. **「Create Web Service」** をクリック
2. デプロイが完了するまで待機（5-10 分程度）
3. デプロイ完了後、URL が表示される（例: `https://movie-line-bot-webhook.onrender.com`）

#### ステップ 5: Webhook URL の設定

1. LINE Developers コンソールに戻る
2. **「Messaging API 設定」** タブを開く
3. **「Webhook URL」** に以下を入力：
   ```
   https://your-app-name.onrender.com/webhook
   ```
4. **「検証」** ボタンをクリックして成功を確認
5. **「Webhook の利用」** を **有効** にする

### オプション 2: Heroku

詳細は [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) を参照してください。

---

## 動作確認

### 1. 週次通知のテスト

#### 手動実行

```bash
# ローカルで実行
python src/weekly_new_movies.py
python src/weekly_now_showing.py
```

#### GitHub Actions で実行

1. GitHub リポジトリの **Actions** タブを開く
2. **週次映画通知** ワークフローを選択
3. **「Run workflow」** > **「Run workflow」** をクリック
4. 実行ログを確認

### 2. リッチメニューのテスト

LINE アプリで以下を確認：

1. ✅ **🎬 映画検索**

   - ボタンをタップ
   - 「映画検索モードです」というメッセージが表示される
   - 映画名を入力して検索結果が表示される

2. ✅ **🎪 映画館検索**

   - ボタンをタップ
   - 「映画館検索モードです」というメッセージが表示される
   - 映画館名を入力して検索ボタンが表示される

3. ✅ **📅 今週公開**

   - ボタンをタップ
   - 今週公開予定の映画一覧が表示される

4. ✅ **🎭 上映中**
   - ボタンをタップ
   - 上映中の映画一覧が表示される

### 3. セッション管理のテスト

1. 映画検索ボタンをタップ
2. 10 分以内に映画名を入力 → 検索結果が表示される
3. 10 分経過後に映画名を入力 → 通常モードに戻る

### 4. Webhook ログの確認

#### Render.com

1. ダッシュボードでサービスを選択
2. **「Logs」** タブを開く
3. リアルタイムログを確認

#### ローカル

```bash
# Flaskサーバーをローカルで起動
python src/webhook_server.py

# 別のターミナルでngrokを使用（外部公開）
ngrok http 5000
```

---

## トラブルシューティング

### 通知が届かない

**原因 1: GitHub Secrets の設定ミス**

- Secrets が正しく設定されているか確認
- トークンや User ID に余分なスペースがないか確認

**原因 2: GitHub Actions が無効**

- Actions タブで有効化されているか確認
- ワークフローファイルが存在するか確認

**原因 3: LINE API の制限**

- 無料プランの月間 1,000 通制限を超えていないか確認
- チャネルが有効か確認

**解決策**:

```bash
# ローカルで手動実行してエラーを確認
python src/weekly_new_movies.py
```

### Webhook が動作しない

**原因 1: Webhook URL が正しくない**

- LINE Developers コンソールで設定を確認
- URL の末尾が `/webhook` になっているか確認

**原因 2: サーバーが起動していない**

- Render.com のダッシュボードでサービスが起動しているか確認
- ログにエラーがないか確認

**原因 3: 署名検証エラー**

- `LINE_CHANNEL_SECRET` が正しく設定されているか確認

**解決策**:

```bash
# ヘルスチェック
curl https://your-app-name.onrender.com/health

# ログ確認
# Render.comのダッシュボード > Logs
```

### リッチメニューが表示されない

**原因 1: リッチメニューが設定されていない**

```bash
# 再設定
python tools/setup_rich_menu.py
```

**原因 2: LINE アプリのキャッシュ**

- LINE アプリを完全に終了して再起動
- Bot をブロック解除してから再度友だち追加

**原因 3: 複数のリッチメニューが存在**

```bash
# 既存のリッチメニューを削除してから再設定
python tools/setup_rich_menu.py
# プロンプトで'y'を入力して既存メニューを削除
```

### セッション管理が動作しない

**原因: データディレクトリが存在しない**

```bash
# dataディレクトリを作成
mkdir -p data
```

**確認**:

```bash
# セッションファイルが作成されているか確認
ls -la data/sessions.json
```

### 依存関係のエラー

```bash
# 仮想環境を削除して再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📚 次のステップ

セットアップが完了したら、以下のドキュメントも参照してください：

- [README.md](README.md) - プロジェクト概要
- [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) - Webhook 詳細設定
- [docs/LINE_API_CAPABILITIES.md](docs/LINE_API_CAPABILITIES.md) - LINE API 機能一覧
- [NEXT_STEPS.md](NEXT_STEPS.md) - 機能拡張ガイド

---

## 🤝 サポート

問題が解決しない場合は、GitHub の Issue を作成してください。

**Happy Movie Watching! 🎬🍿**
