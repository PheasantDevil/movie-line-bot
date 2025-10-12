# 🎬 映画情報通知 LINE Bot

日本国内の新作映画情報を自動で通知するLINE Botシステムです。

## 📝 概要

このプロジェクトは、映画.comから最新の映画情報を取得し、新作映画が追加された際にLINE経由で自動通知を行います。

### 通知内容

- 🎬 タイトル
- 📅 公開日
- 🎭 ジャンル（アニメ/実写、洋画/邦画、カテゴリ）
- 🎪 特定映画館限定の場合：映画館一覧
- 🔗 作品詳細URL
- ℹ️ その他特記事項

## 🚀 セットアップ

### 1. LINE Messaging API の設定

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. 新規プロバイダーを作成
3. Messaging APIチャネルを作成
4. 以下の情報を取得：
   - Channel Access Token（長期）
   - Channel Secret
5. あなたのLINE User IDを取得（後述）

### 2. GitHub Secrets の設定

リポジトリのSettings > Secrets and variables > Actionsで以下を設定：

- `LINE_CHANNEL_ACCESS_TOKEN`: LINEのアクセストークン
- `LINE_USER_ID`: 通知先のLINE User ID

### 3. ローカルでの実行（任意）

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
export LINE_CHANNEL_ACCESS_TOKEN="your_token_here"
export LINE_USER_ID="your_user_id_here"

# 実行
python src/main.py
```

## 🔄 自動実行

GitHub Actionsにより、毎日日本時間の午前9時に自動で映画情報をチェックし、新作があれば通知します。

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

## 🤝 貢献

プルリクエストを歓迎します！

