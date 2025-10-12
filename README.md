# 🎬 映画情報通知 LINE Bot

日本国内の新作映画情報を自動で通知するLINE Botシステムです。

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![LINE](https://img.shields.io/badge/LINE-Messaging%20API-00C300)](https://developers.line.biz/)

## 📝 概要

このプロジェクトは、映画.comから最新の映画情報を取得し、新作映画が追加された際にLINE経由で自動通知を行います。

**主な機能:**
- ✅ 映画.comから今週公開の映画情報を自動取得
- ✅ 前回との差分を検知して新作映画のみを通知
- ✅ LINE Messaging APIで自動通知
- ✅ GitHub Actionsで毎日自動実行
- ✅ 完全無料で運用可能（無料枠内）

### 通知内容

- 🎬 **タイトル**
- 📅 **公開日**
- 🔗 **作品詳細URL**（映画.comへのリンク）

## 🚀 セットアップ

### 必要なもの

- GitHubアカウント
- LINEアカウント
- LINE Developers アカウント（無料）

### 1. リポジトリのフォーク/クローン

```bash
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot
```

### 2. LINE Messaging API の設定

#### 2.1 LINE Developersでチャネルを作成

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. ログイン後、**「新規プロバイダー」**を作成
3. **「Messaging API」**チャネルを作成
   - チャネル名: 例）映画情報Bot
   - チャネル説明: 例）新作映画情報を通知するBot
   - カテゴリ: 適切なものを選択

#### 2.2 アクセストークンの取得

1. 作成したチャネルの「Messaging API設定」タブを開く
2. **「チャネルアクセストークン」**セクションで「発行」ボタンをクリック
3. 表示されたトークンをコピーして保存（後で使用）

#### 2.3 LINE User IDの取得

**方法1: LINE公式アカウントを友だち追加して確認**

1. チャネルのQRコードから自分のLINEアカウントで友だち追加
2. 以下のPythonスクリプトで確認（一時的にWebhook URLを設定する必要があります）

**方法2: 簡易的な方法**

LINE Botに何かメッセージを送って、Webhookログから確認する方法もありますが、
最も簡単なのは、[LINE Official Account Manager](https://manager.line.biz/)で確認することです。

### 3. GitHubリポジトリにSecretを設定

1. GitHubリポジトリのページで **Settings** > **Secrets and variables** > **Actions** を開く
2. **「New repository secret」**をクリックして以下を追加：

   **Secret 1:**
   - Name: `LINE_CHANNEL_ACCESS_TOKEN`
   - Value: 先ほど取得したチャネルアクセストークン

   **Secret 2:**
   - Name: `LINE_USER_ID`
   - Value: 取得したLINE User ID（例: U1234567890abcdef...）

### 4. GitHub Actionsを有効化

1. リポジトリの **Actions** タブを開く
2. ワークフローを有効化（必要に応じて）
3. 手動で実行してテスト：
   - 「映画情報チェック & LINE通知」ワークフローを選択
   - **「Run workflow」**ボタンをクリック
   - ブランチを選択して実行

### 5. ローカルでの実行（任意・開発用）

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
export LINE_CHANNEL_ACCESS_TOKEN="your_token_here"
export LINE_USER_ID="your_user_id_here"

# 実行
python src/main.py
```

## 🔄 自動実行スケジュール

GitHub Actionsにより、以下のスケジュールで自動実行されます：

- **定期実行**: 毎日日本時間の午前9時（UTC 0時）
- **手動実行**: GitHubのActionsページからいつでも実行可能

### 実行の流れ

1. 映画.comから今週公開の映画情報を取得
2. 前回保存したデータと比較
3. 新作映画があればLINEに通知
4. 最新データをGitHubに自動コミット

### 通知の例

```
🎬 新作映画情報 (3件)
==============================

【1】映画タイトル1
📅 公開日: 10月10日
🔗 https://eiga.com/movie/12345/

【2】映画タイトル2
📅 公開日: 10月11日
🔗 https://eiga.com/movie/12346/

【3】映画タイトル3
📅 公開日: 10月12日
🔗 https://eiga.com/movie/12347/
```

## 📁 プロジェクト構造

```
movie-line-bot/
├── .github/workflows/    # GitHub Actions設定
├── src/                  # ソースコード
├── data/                 # 映画データ保存
├── requirements.txt      # Python依存パッケージ
└── README.md            # このファイル
```

## 💰 コスト

- GitHub Actions: 無料枠内
- LINE Messaging API: 無料枠内（1,000通/月）
- **総コスト: ¥0/月**

## 📄 ライセンス

MIT License

## 🛠️ トラブルシューティング

### LINE通知が届かない

1. GitHub Secretsが正しく設定されているか確認
2. LINE Botを友だち追加しているか確認
3. GitHub Actionsのログを確認（Actionsタブ）

### ワークフローが失敗する

1. Actionsタブでエラーログを確認
2. Pythonの依存関係が正しくインストールされているか確認
3. 映画.comのHTML構造が変更されている可能性（その場合はスクレイパーの修正が必要）

### データが更新されない

1. GitHub Actionsに書き込み権限があるか確認
   - Settings > Actions > General > Workflow permissions
   - "Read and write permissions" を選択

## 📊 プロジェクト構造

```
movie-line-bot/
├── .github/
│   └── workflows/
│       ├── check-movies.yml    # GitHub Actionsワークフロー
│       └── README.md            # ワークフロー説明
├── src/
│   ├── __init__.py
│   ├── main.py                  # メインスクリプト
│   ├── scraper.py               # 映画情報スクレイピング
│   ├── storage.py               # データ永続化
│   ├── diff_detector.py         # 差分検知
│   └── line_notifier.py         # LINE通知
├── data/
│   └── movies.json              # 映画データ（自動生成）
├── requirements.txt             # Python依存パッケージ
├── .gitignore
└── README.md
```

## 🔧 カスタマイズ

### 実行時刻の変更

`.github/workflows/check-movies.yml` の cron 設定を変更：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0時 = JST 9時
```

### 通知メッセージのカスタマイズ

`src/line_notifier.py` の `_format_movie_message()` メソッドを編集

### スクレイピング対象の変更

`src/scraper.py` の `BASE_URL` やパース処理を編集

## 🤝 貢献

プルリクエストや Issue の作成を歓迎します！

### 開発の流れ

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

