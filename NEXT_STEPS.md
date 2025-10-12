# 🚀 次のステップガイド

プロジェクトの実装が完了しました！次は以下の手順で実際に運用を開始しましょう。

## ✅ 現在の状態

- ✅ すべてのコードが実装済み
- ✅ ドキュメントが完備
- ✅ ローカルリポジトリにコミット済み
- ⏳ GitHub へのプッシュ待ち
- ⏳ LINE Messaging API 設定待ち
- ⏳ GitHub Actions 設定待ち

---

## 📝 ステップ 1: GitHub にリポジトリを作成

### 1.1 GitHub で新規リポジトリを作成

1. https://github.com/new にアクセス
2. **Repository name**: `movie-line-bot`（推奨）
3. **Description**: 日本の新作映画情報を LINE で通知する Bot
4. **Public** または **Private** を選択
   - Public: 他の人も見られる
   - Private: 自分だけ
5. **Initialize this repository with** は**すべてチェックなし**
6. 「Create repository」をクリック

### 1.2 ローカルからプッシュ

GitHub でリポジトリを作成したら、以下のコマンドを実行：

```bash
cd /Users/Work/movie-line-bot

# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/movie-line-bot.git

# main ブランチをプッシュ
git push -u origin main
```

**注意**: `YOUR_USERNAME` を自分の GitHub ユーザー名に置き換えてください。

---

## 📱 ステップ 2: LINE Messaging API の設定

### 2.1 LINE Developers Console でチャネル作成

詳細は [SETUP_GUIDE.md](SETUP_GUIDE.md) を参照してください。

**手順概要:**

1. https://developers.line.biz/console/ にアクセス
2. ログイン
3. **新規プロバイダー**を作成
   - プロバイダー名: 例）MyMovieBot
4. **Messaging API チャネル**を作成
   - チャネル名: 例）映画情報通知 Bot
   - カテゴリ: 適切なものを選択
5. **チャネルアクセストークン**を発行
   - 「Messaging API 設定」タブ
   - 「チャネルアクセストークン（長期）」→「発行」
   - **重要**: トークンをコピーして安全に保管

### 2.2 LINE User ID の取得

**方法 1: QR コードで友だち追加**

1. チャネルの「Messaging API 設定」タブの QR コードをスキャン
2. 自分の LINE で友だち追加

**方法 2: LINE Official Account Manager で確認**

1. https://manager.line.biz/ にアクセス
2. 作成したアカウントを選択
3. 設定から User ID を確認

### 2.3 保存する情報

以下の 2 つの情報を控えておいてください：

- ✅ **Channel Access Token**: `YOUR_CHANNEL_ACCESS_TOKEN`
- ✅ **LINE User ID**: `U1234567890abcdef...`（U で始まる文字列）

---

## 🔐 ステップ 3: GitHub Secrets の設定

### 3.1 Secrets ページを開く

1. GitHub リポジトリのページを開く
2. **Settings** タブをクリック
3. 左サイドバーから **Secrets and variables** > **Actions** を選択

### 3.2 Secret を追加

**Secret 1: LINE_CHANNEL_ACCESS_TOKEN**

1. 「New repository secret」をクリック
2. Name: `LINE_CHANNEL_ACCESS_TOKEN`
3. Secret: 先ほど取得したチャネルアクセストークンを貼り付け
4. 「Add secret」をクリック

**Secret 2: LINE_USER_ID**

1. 再度「New repository secret」をクリック
2. Name: `LINE_USER_ID`
3. Secret: 取得した LINE User ID を貼り付け（`U` で始まる文字列）
4. 「Add secret」をクリック

### 3.3 確認

設定後、以下の 2 つの Secret が表示されているはずです：

- ✅ `LINE_CHANNEL_ACCESS_TOKEN`
- ✅ `LINE_USER_ID`

---

## ⚙️ ステップ 4: GitHub Actions の権限設定

### 4.1 Workflow permissions の設定

これにより、GitHub Actions がデータファイルを自動コミットできるようになります。

1. リポジトリの **Settings** タブを開く
2. 左サイドバーから **Actions** > **General** を選択
3. 下にスクロールして「Workflow permissions」セクションを探す
4. **「Read and write permissions」** を選択
5. 「Save」をクリック

---

## 🧪 ステップ 5: 動作テスト

### 5.1 手動実行でテスト

1. リポジトリの **Actions** タブを開く
2. 左サイドバーから **「映画情報チェック & LINE 通知」** を選択
3. 右側の **「Run workflow」** ボタンをクリック
4. Branch は `main` を選択
5. **「Run workflow」** をクリック

### 5.2 実行結果の確認

1. ワークフローの実行が開始されます（数十秒～ 1 分程度）
2. 完了したら、ワークフロー名をクリックして詳細を確認
3. **緑色のチェックマーク ✓** が表示されれば成功！
4. **LINE に通知が届くか確認**（初回は全映画が通知されます）

### 5.3 エラーが発生した場合

1. ワークフロー実行をクリックして詳細ログを確認
2. エラーメッセージを読んで原因を特定
3. よくある問題：
   - Secret が正しく設定されていない
   - LINE User ID が間違っている
   - Bot を友だち追加していない

詳しくは [docs/faq.md](docs/faq.md) のトラブルシューティングを参照してください。

---

## 🎉 ステップ 6: 自動実行の確認

セットアップが完了すると、以下のスケジュールで自動実行されます：

- **毎日日本時間 9 時**（UTC 0 時）に自動実行
- 新作映画があれば LINE に通知

### 翌日の確認

翌日の午前 9 時以降に：

1. **LINE 通知を確認**（新作映画がある場合のみ届きます）
2. **GitHub リポジトリを確認**
   - `data/movies.json` が自動更新されているか
   - GitHub Actions の実行履歴を確認

---

## 📚 追加のカスタマイズ（オプション）

### 実行時刻の変更

`.github/workflows/check-movies.yml` の cron 設定を変更：

```yaml
schedule:
  - cron: '0 0 * * *' # UTC 0時 = JST 9時
  # 例: UTC 12時 = JST 21時 にしたい場合
  # - cron: "0 12 * * *"
```

変更後、コミット・プッシュすれば適用されます。

### 通知メッセージのカスタマイズ

`src/line_notifier.py` の `_format_movie_message()` メソッドを編集して、
好みのフォーマットに変更できます。

詳しくは [docs/development_guide.md](docs/development_guide.md) を参照してください。

---

## ✅ チェックリスト

すべて完了したか確認しましょう：

- [ ] GitHub にリポジトリを作成してプッシュ
- [ ] LINE Messaging API のチャネルを作成
- [ ] Channel Access Token を取得
- [ ] LINE User ID を取得
- [ ] GitHub Secrets を設定（2 つ）
- [ ] GitHub Actions の権限を設定
- [ ] 手動実行でテスト
- [ ] LINE に通知が届くことを確認
- [ ] 自動実行の設定を確認

---

## 🆘 困ったときは

### ドキュメント

- [README.md](README.md) - プロジェクト概要
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 詳細なセットアップ手順
- [docs/faq.md](docs/faq.md) - よくある質問
- [docs/troubleshooting.md](docs/troubleshooting.md) - トラブルシューティング

### サポート

- GitHub Issues で質問
- ドキュメントを再確認
- エラーログを詳しく確認

---

## 🎊 完了！

すべてのステップが完了したら、毎日自動で新作映画情報が LINE に届くようになります！

映画ライフをお楽しみください！🎬
