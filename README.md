# 🎬 映画情報通知 LINE Bot

日本国内の新作映画情報を自動で通知し、インタラクティブな検索機能を提供する LINE Bot システムです。

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![LINE](https://img.shields.io/badge/LINE-Messaging%20API-00C300)](https://developers.line.biz/)

## 📝 概要

このプロジェクトは、映画.com から最新の映画情報を取得し、LINE 経由で週次通知とインタラクティブな検索機能を提供します。

**主な機能:**

- ✅ **週次自動通知**: 毎週水曜 9 時に今週公開・上映中映画を通知
- ✅ **リッチメニュー**: 画面下部の固定メニュー（4つのボタン）
- ✅ **映画検索**: セッション管理による対話式検索
- ✅ **映画館検索**: Google検索連携で映画館情報を検索
- ✅ **上映館数表示**: 限定公開映画を ⚠️ マークで表示
- ✅ **インタラクティブUI**: Postbackイベント対応、不要入力への誘導
- ✅ **完全無料運用可能**（無料枠内）

## 🎯 機能詳細

### 1. 週次自動通知（毎週水曜 9時）

- **今週公開映画**: 今週公開予定の映画一覧
  - 映画がない場合は通知をスキップ
- **上映中映画**: 現在上映中の映画一覧
  - 上映館数と限定公開情報を表示

### 2. リッチメニュー（画面下部の固定メニュー）

| ボタン | 機能 | 動作 |
|--------|------|------|
| 🎬 映画検索 | 映画名で検索 | セッションモードに入り、映画名入力を受け付ける |
| 🎪 映画館検索 | 映画館を検索 | セッションモードに入り、Google検索結果を表示 |
| 📅 今週公開 | 今週公開予定 | 即座に今週公開映画の一覧を表示 |
| 🎭 上映中 | 上映中映画 | 即座に上映中映画の一覧を表示 |

### 3. インタラクティブ機能

- **セッション管理**: ユーザーごとの状態を10分間保持
- **対話式検索**: ボタンタップ後、次の入力を待機
- **不要入力への対応**: 画像・スタンプなどにメニュー誘導
- **ウェルカムメッセージ**: 友だち追加時に機能説明を表示

### 4. 検索機能

#### 映画検索
- キーワードで映画を検索
- eiga.com からリアルタイム検索
- ローカルストレージからも検索
- 公開日、上映館数、詳細URLを表示

#### 映画館検索
- 映画館名で Google 検索
- 検索ボタン付きメッセージで結果表示
- ブラウザで検索結果を開く

## 🏗️ アーキテクチャ

### システム構成

```
映画.com → スクレイピング → データ保存
                ↓
          週次通知（GitHub Actions）
                ↓
          LINE Messaging API → ユーザー
                ↑
          Webhook（Render.com等）
                ↑
          ユーザー操作（リッチメニュー）
```

### ファイル構成と機能

```
movie-line-bot/
├── src/
│   ├── main.py                     # メイン処理（週次通知のデータ収集）
│   ├── scraper.py                  # 映画情報スクレイピング
│   ├── storage.py                  # データ永続化
│   ├── line_notifier.py            # LINE通知機能
│   ├── webhook_server.py           # Webhookサーバー（Flask）
│   ├── session_manager.py          # セッション管理
│   ├── rich_menu_manager.py        # リッチメニュー管理
│   ├── movie_theater_search.py     # 映画館検索
│   ├── weekly_new_movies.py        # 今週公開映画通知
│   └── weekly_now_showing.py       # 上映中映画通知
├── .github/workflows/
│   └── weekly-notifications.yml    # 週次通知ワークフロー
├── tools/
│   ├── generate_rich_menu_image.py # リッチメニュー画像生成
│   └── setup_rich_menu.py          # リッチメニュー設定
├── assets/
│   └── rich_menu.png               # リッチメニュー画像
├── data/
│   ├── movies.json                 # 映画データ
│   └── sessions.json               # セッションデータ
├── docs/
│   └── LINE_API_CAPABILITIES.md    # LINE API機能一覧
├── requirements.txt                # Python依存関係
├── Procfile                        # Webサーバー起動設定
└── README.md                       # このファイル
```

## 🚀 セットアップ

### 必要なもの

- GitHub アカウント
- LINE アカウント
- LINE Developers アカウント（無料）
- （Webhook用）Render.com アカウントまたは他のホスティングサービス

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
   - チャネル名: 例）映画情報Bot
   - チャネル説明: 例）新作映画情報を通知するBot
   - カテゴリ: 適切なものを選択

#### 2.2 アクセストークンとシークレットの取得

1. 作成したチャネルの「Messaging API 設定」タブを開く
2. **「チャネルアクセストークン」**セクションで「発行」ボタンをクリック
3. 表示されたトークンをコピーして保存
4. **「チャネルシークレット」**もコピーして保存

#### 2.3 LINE User ID の取得

1. チャネルのQRコードから自分のLINEアカウントで友だち追加
2. Webhookサーバーのログから確認、または
3. [LINE Official Account Manager](https://manager.line.biz/)で確認

### 3. GitHub リポジトリに Secret を設定

1. GitHub リポジトリのページで **Settings** > **Secrets and variables** > **Actions** を開く
2. **「New repository secret」**をクリックして以下を追加：

   - `LINE_CHANNEL_ACCESS_TOKEN`: チャネルアクセストークン
   - `LINE_USER_ID`: LINE User ID
   - `LINE_CHANNEL_SECRET`: チャネルシークレット（Webhook用）

### 4. 依存関係のインストール

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 5. リッチメニューの設定

```bash
# 環境変数を設定
export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'

# リッチメニュー画像を生成（Pillowが必要）
pip install pillow
python tools/generate_rich_menu_image.py

# リッチメニューを設定
python tools/setup_rich_menu.py
```

### 6. Webhookサーバーのデプロイ

詳細は [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) を参照してください。

簡易手順：
1. Render.com でアカウント作成
2. GitHubリポジトリを接続
3. 環境変数を設定
4. デプロイ
5. Webhook URLをLINE Developersコンソールに設定

### 7. GitHub Actions を有効化

1. GitHub リポジトリの **Actions** タブを開く
2. ワークフローが表示されていることを確認
3. 初回は手動で実行してテスト

## 📅 使い方

### ユーザー操作

1. **友だち追加**: LINE Bot を友だち追加するとウェルカムメッセージが表示されます
2. **リッチメニュー**: 画面下部のメニューから機能を選択
3. **映画検索**: 🎬ボタン → 映画名を入力
4. **映画館検索**: 🎪ボタン → 映画館名を入力
5. **今週公開**: 📅ボタンで即座に表示
6. **上映中**: 🎭ボタンで即座に表示

### 管理者操作

#### ローカルでのテスト実行

```bash
# 環境変数を設定
export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'
export LINE_USER_ID='your_user_id'

# 今週公開映画通知のテスト
python src/weekly_new_movies.py --test

# 上映中映画通知のテスト
python src/weekly_now_showing.py --test

# Webhookサーバーのローカル起動
python src/webhook_server.py
```

#### GitHub Actionsの手動実行

1. GitHubリポジトリの **Actions** タブを開く
2. **週次映画通知** ワークフローを選択
3. **Run workflow** ボタンをクリック

## 🛠️ 機能追加手順テンプレート

### 新しい通知機能の追加

1. `src/` に新しいスクリプトを作成
2. `line_notifier.py` に専用メソッドを追加
3. `.github/workflows/` に新しいワークフローを追加
4. テスト実行して確認

### Quick Reply機能の追加

```python
# line_notifier.py に追加
def reply_with_quick_reply(self, reply_token: str, text: str, items: List[Dict]) -> bool:
    data = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': text,
            'quickReply': {'items': items}
        }]
    }
    # 送信処理...
```

### リッチメニューの変更

1. `tools/generate_rich_menu_image.py` で画像を再生成
2. `src/rich_menu_manager.py` でボタン配置を変更
3. `src/webhook_server.py` でPostback処理を更新
4. `tools/setup_rich_menu.py` で再設定

## 📊 技術スタック

- **Python 3.11+**: メインプログラミング言語
- **Beautiful Soup**: Webスクレイピング
- **Flask**: Webhookサーバー
- **Gunicorn**: Webサーバー（本番環境）
- **LINE Messaging API**: LINE連携
- **GitHub Actions**: 自動実行
- **Render.com**: Webホスティング（推奨）

## 📚 ドキュメント

- [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) - Webhook設定ガイド
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 詳細セットアップガイド
- [NEXT_STEPS.md](NEXT_STEPS.md) - 次のステップガイド
- [docs/LINE_API_CAPABILITIES.md](docs/LINE_API_CAPABILITIES.md) - LINE API機能一覧

## 🔧 トラブルシューティング

### 通知が届かない

- GitHub Secretsが正しく設定されているか確認
- GitHub Actionsのログを確認
- LINE Developersコンソールでチャネルが有効か確認

### Webhookが動作しない

- Webhook URLが正しく設定されているか確認
- サーバーが起動しているか確認
- 署名検証が有効になっているか確認
- ログを確認: `heroku logs --tail` または Render.comのログ

### リッチメニューが表示されない

- リッチメニューが正しく設定されているか確認: `python tools/setup_rich_menu.py`
- LINE アプリを再起動
- Bot をブロック解除してから再度友だち追加

## 💡 今後の拡張案

- [ ] ユーザーごとのお気に入り映画登録
- [ ] 特定ジャンルの映画通知
- [ ] 映画レビュー機能
- [ ] 近隣の映画館検索（位置情報連携）
- [ ] AIによる映画レコメンド

## 📝 ライセンス

MIT License

## 🤝 貢献

Pull Requestsを歓迎します！

## 📧 お問い合わせ

Issue を作成してください。

---

**🎬 Happy Movie Watching! 🍿**
