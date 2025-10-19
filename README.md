# 🎬 映画情報通知 LINE Bot

日本国内の新作映画情報を自動で通知する LINE Bot システムです。

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![LINE](https://img.shields.io/badge/LINE-Messaging%20API-00C300)](https://developers.line.biz/)

## 📝 概要

このプロジェクトは、映画.com から最新の映画情報を取得し、LINE 経由で週次通知とキーワード検索機能を提供します。

**主な機能:**

- ✅ **週次通知**: 過去 1 週間と先 1 週間の映画情報を毎日自動通知
- ✅ **上映館数表示**: 限定公開映画を ⚠️ マークで表示
- ✅ **映画検索**: LINE で映画名を入力すると情報を返信
- ✅ **LINE Messaging API**: Push 通知と Webhook 対応
- ✅ **GitHub Actions**: 毎日自動実行
- ✅ **完全無料運用可能**（無料枠内）

### 通知内容

#### 週次通知（毎日 9 時）

- 📅 **過去 1 週間以内に公開された映画**の一覧
- 📅 **先 1 週間以内に公開予定の映画**の一覧
- 🎬 上映館数と限定公開情報
- 🔗 作品詳細 URL

#### キーワード検索（リアルタイム）

- LINE で映画名を入力すると該当する映画情報を返信
- 公開日、上映館数、詳細 URL などを表示

## 🚀 クイックスタート

**→ [詳細な次のステップガイド](NEXT_STEPS.md)** ← ここから始めてください！

## 🚀 セットアップ

### 必要なもの

- GitHub アカウント
- LINE アカウント
- LINE Developers アカウント（無料）

### 1. リポジトリのフォーク/クローン

```bash
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot
```

### 2. LINE Messaging API の設定

#### 2.1 LINE Developers でチャネルを作成

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. ログイン後、**「新規プロバイダー」**を作成
3. **「Messaging API」**チャネルを作成
   - チャネル名: 例）映画情報 Bot
   - チャネル説明: 例）新作映画情報を通知する Bot
   - カテゴリ: 適切なものを選択

#### 2.2 アクセストークンの取得

1. 作成したチャネルの「Messaging API 設定」タブを開く
2. **「チャネルアクセストークン」**セクションで「発行」ボタンをクリック
3. 表示されたトークンをコピーして保存（後で使用）

#### 2.3 LINE User ID の取得

**方法 1: LINE 公式アカウントを友だち追加して確認**

1. チャネルの QR コードから自分の LINE アカウントで友だち追加
2. 以下の Python スクリプトで確認（一時的に Webhook URL を設定する必要があります）

**方法 2: 簡易的な方法**

LINE Bot に何かメッセージを送って、Webhook ログから確認する方法もありますが、
最も簡単なのは、[LINE Official Account Manager](https://manager.line.biz/)で確認することです。

### 3. GitHub リポジトリに Secret を設定

1. GitHub リポジトリのページで **Settings** > **Secrets and variables** > **Actions** を開く
2. **「New repository secret」**をクリックして以下を追加：

   **Secret 1:**

   - Name: `LINE_CHANNEL_ACCESS_TOKEN`
   - Value: 先ほど取得したチャネルアクセストークン

   **Secret 2:**

   - Name: `LINE_USER_ID`
   - Value: 取得した LINE User ID（例: U1234567890abcdef...）

### 4. GitHub Actions を有効化

1. リポジトリの **Actions** タブを開く
2. ワークフローを有効化（必要に応じて）
3. 手動で実行してテスト：
   - 「映画情報チェック & LINE 通知」ワークフローを選択
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

GitHub Actions により、以下のスケジュールで自動実行されます：

- **定期実行**: 毎日日本時間の午前 9 時（UTC 0 時）
- **手動実行**: GitHub の Actions ページからいつでも実行可能

### 実行の流れ

1. 映画.com から今週公開の映画情報を取得
2. 前回保存したデータと比較
3. 新作映画があれば LINE に通知
4. 最新データを GitHub に自動コミット

### 通知の例

#### 週次通知

```
🎬 週刊映画情報
==============================

【過去1週間以内に公開された映画】
1. 映画タイトル1
   公開日: 10月10日
   https://eiga.com/movie/12345/

2. 映画タイトル2
   公開日: 10月12日
   https://eiga.com/movie/12346/

==============================

【先1週間以内に公開予定の映画】
1. 映画タイトル3 (300館)
   公開日: 10月20日
   https://eiga.com/movie/12347/

2. 映画タイトル4 ⚠️ 限定公開(30館)
   公開日: 10月22日
   https://eiga.com/movie/12348/
```

#### キーワード検索の例

LINE で「君の名は。」と入力すると：

```
🎬 検索結果 (1件)
==============================

【1】君の名は。
公開日: 8月26日
上映館数: 300館
詳細: https://eiga.com/movie/...
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

- GitHub Actions: 無料枠内（週次通知）
- LINE Messaging API: 無料枠内（1,000 通/月）
- Webhook サーバー: 無料枠あり（Render.com 推奨）
- **総コスト: ¥0/月**（無料プランの場合）

## 🔧 Webhook 機能の設定

キーワード検索機能を有効にするには、Webhook サーバーのデプロイが必要です。

**→ [Webhook セットアップガイド](WEBHOOK_SETUP.md)** ← 詳細はこちら

### クイックセットアップ

1. [Render.com](https://render.com/)でアカウント作成
2. GitHub リポジトリを接続
3. 環境変数を設定（`LINE_CHANNEL_ACCESS_TOKEN`, `LINE_USER_ID`, `LINE_CHANNEL_SECRET`）
4. LINE Developers Console で Webhook URL を設定

詳細は[WEBHOOK_SETUP.md](WEBHOOK_SETUP.md)を参照してください。

## 📚 ドキュメント

- **[LINE API機能一覧](docs/LINE_API_CAPABILITIES.md)** - LINE Messaging APIで利用可能な全機能の詳細
- **[Webhookセットアップガイド](WEBHOOK_SETUP.md)** - Webhookサーバーのデプロイ方法
- **[次のステップガイド](NEXT_STEPS.md)** - 初回セットアップ手順

## 📄 ライセンス

MIT License

## 🛠️ トラブルシューティング

### LINE 通知が届かない

1. GitHub Secrets が正しく設定されているか確認
2. LINE Bot を友だち追加しているか確認
3. GitHub Actions のログを確認（Actions タブ）

### ワークフローが失敗する

1. Actions タブでエラーログを確認
2. Python の依存関係が正しくインストールされているか確認
3. 映画.com の HTML 構造が変更されている可能性（その場合はスクレイパーの修正が必要）

### データが更新されない

1. GitHub Actions に書き込み権限があるか確認
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
  - cron: '0 0 * * *' # UTC 0時 = JST 9時
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
