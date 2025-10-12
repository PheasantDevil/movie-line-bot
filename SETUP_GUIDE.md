# 🚀 詳細セットアップガイド

このガイドでは、映画情報通知LINE Botを完全にセットアップする手順を詳しく説明します。

## 📋 前提条件

- GitHubアカウント
- LINEアカウント
- 基本的なGitの知識

## ステップ1: GitHubリポジトリの準備

### 1.1 リポジトリをフォーク（推奨）

1. GitHubでこのリポジトリのページを開く
2. 右上の「Fork」ボタンをクリック
3. 自分のアカウントにリポジトリがコピーされる

### 1.2 または、クローンして新規リポジトリ作成

```bash
# クローン
git clone https://github.com/original-repo/movie-line-bot.git
cd movie-line-bot

# 新規リポジトリを作成してプッシュ
git remote remove origin
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

## ステップ2: LINE Botの設定

### 2.1 LINE Developers Consoleにアクセス

1. https://developers.line.biz/console/ を開く
2. LINEアカウントでログイン

### 2.2 プロバイダーの作成

1. 「プロバイダーを作成」をクリック
2. プロバイダー名を入力（例: MyMovieBot）
3. 「作成」をクリック

### 2.3 Messaging APIチャネルの作成

1. 作成したプロバイダーを選択
2. 「チャネルを作成」→「Messaging API」を選択
3. 以下の情報を入力：
   - **チャネル名**: 映画情報通知Bot（任意の名前）
   - **チャネル説明**: 新作映画情報を自動通知
   - **カテゴリー**: 適切なものを選択
   - **サブカテゴリー**: 適切なものを選択
4. 利用規約に同意して「作成」をクリック

### 2.4 チャネルアクセストークンの取得

1. 作成したチャネルを選択
2. 「Messaging API設定」タブを開く
3. 「チャネルアクセストークン（長期）」セクションまでスクロール
4. 「発行」ボタンをクリック
5. 表示されたトークンをコピー（**重要**: このトークンは後で確認できないので安全に保存）

### 2.5 Webhook設定（オプション）

今回はPush型通知のみを使用するため、Webhookは不要ですが、応答メッセージを無効化しておくことを推奨：

1. 「Messaging API設定」タブ内の「応答メッセージ」を「オフ」に設定

### 2.6 LINE User IDの取得

#### 方法A: QRコードで友だち追加

1. 「Messaging API設定」タブのQRコードをスキャン
2. 自分のLINEアカウントで友だち追加

#### 方法B: User IDを取得するスクリプト

簡易的な方法として、LINE Official Account Managerを使用：

1. https://manager.line.biz/ にアクセス
2. 作成したアカウントを選択
3. 「設定」→「応答設定」で User ID を確認

または、Botにメッセージを送って、一時的にWebhookを設定してUser IDを取得する方法もあります。

## ステップ3: GitHub Secretsの設定

### 3.1 Secretsページを開く

1. フォークしたGitHubリポジトリのページを開く
2. 「Settings」タブをクリック
3. 左サイドバーから「Secrets and variables」→「Actions」を選択

### 3.2 Secretを追加

**Secret 1: LINE_CHANNEL_ACCESS_TOKEN**

1. 「New repository secret」をクリック
2. Name: `LINE_CHANNEL_ACCESS_TOKEN`
3. Secret: 先ほどコピーしたチャネルアクセストークンを貼り付け
4. 「Add secret」をクリック

**Secret 2: LINE_USER_ID**

1. 再度「New repository secret」をクリック
2. Name: `LINE_USER_ID`
3. Secret: 取得したLINE User IDを貼り付け（`U` で始まる文字列）
4. 「Add secret」をクリック

## ステップ4: GitHub Actionsの権限設定

### 4.1 Workflow権限の設定

1. リポジトリの「Settings」→「Actions」→「General」を開く
2. 「Workflow permissions」セクションまでスクロール
3. 「Read and write permissions」を選択
4. 「Save」をクリック

これにより、GitHub Actionsがmovies.jsonファイルを自動でコミット・プッシュできるようになります。

## ステップ5: 動作テスト

### 5.1 手動実行でテスト

1. リポジトリの「Actions」タブを開く
2. 左サイドバーから「映画情報チェック & LINE通知」を選択
3. 「Run workflow」ボタンをクリック
4. ブランチ（通常は`main`）を選択
5. 「Run workflow」をクリック

### 5.2 実行結果の確認

1. ワークフロー実行が開始される（数十秒〜1分程度）
2. 実行が完了すると、LINEに通知が届く（初回は全映画が新着として通知されます）
3. 緑色のチェックマークが表示されれば成功

### 5.3 エラーが発生した場合

1. 実行ログをクリックして詳細を確認
2. エラーメッセージを読んで原因を特定
3. よくある問題：
   - Secret が正しく設定されていない
   - LINE User IDが間違っている
   - Botを友だち追加していない

## ステップ6: 自動実行の確認

セットアップが完了すると、毎日日本時間の午前9時に自動で実行されます。

翌日の午前9時以降に：
1. LINEに通知が届くか確認（新作映画がある場合のみ）
2. GitHubリポジトリの「data/movies.json」が更新されているか確認

## 🎉 セットアップ完了！

これで、毎日自動で新作映画情報がLINEに届くようになりました。

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](README.md#トラブルシューティング)を参照してください。

## 次のステップ

- [カスタマイズ方法](README.md#カスタマイズ) を確認
- 通知メッセージのフォーマットを変更
- 実行時刻を好みの時間に変更

