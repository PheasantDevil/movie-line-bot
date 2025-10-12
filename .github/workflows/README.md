# GitHub Actions ワークフロー

## 映画情報チェック & LINE通知

このワークフローは、映画.comから最新の映画情報を取得し、新作映画があればLINEで通知します。

### 実行タイミング

- **定期実行**: 毎日日本時間の9時（UTC 0時）に自動実行
- **手動実行**: GitHub Actionsのページから手動でトリガー可能

### 必要な設定

GitHub リポジトリの Settings > Secrets and variables > Actions で以下のシークレットを設定してください：

1. `LINE_CHANNEL_ACCESS_TOKEN`
   - LINE Developers Console で取得したチャネルアクセストークン
   
2. `LINE_USER_ID`
   - 通知先のLINE User ID
   - 取得方法: LINE Botに何かメッセージを送ってWebhookで確認、または別の方法で取得

### 動作フロー

1. 映画.comから今週公開の映画情報を取得
2. 前回保存したデータと比較して新作映画を検出
3. 新作映画があればLINEに通知
4. 最新の映画情報をJSONファイルに保存
5. 変更をGitHubリポジトリにコミット・プッシュ

### 手動実行方法

1. GitHubリポジトリのページを開く
2. "Actions" タブをクリック
3. 左サイドバーから "映画情報チェック & LINE通知" を選択
4. "Run workflow" ボタンをクリック
5. ブランチを選択して "Run workflow" を実行

### トラブルシューティング

- ワークフローが失敗する場合は、Actions タブでログを確認してください
- LINE通知が届かない場合は、シークレットが正しく設定されているか確認してください
- 権限エラーが発生する場合は、リポジトリの Settings > Actions > General で Workflow permissions を確認してください

