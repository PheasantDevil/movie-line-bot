# 📝 変更履歴

映画情報 LINE Bot の変更履歴です。

形式は[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、
このプロジェクトは[セマンティックバージョニング](https://semver.org/lang/ja/)に準拠しています。

## [Unreleased]

### 予定されている機能

- ユーザーごとのお気に入り映画登録
- 特定ジャンルの映画通知
- 映画レビュー機能
- 近隣の映画館検索（位置情報連携）
- AI による映画レコメンド

---

## [1.0.0] - 2025-10-19

### 追加（Added）

#### Phase 1: 基盤機能

- **セッション管理システム** (`src/session_manager.py`)

  - ユーザーごとの状態管理
  - 10 分間の有効期限
  - JSON ファイルでの永続化
  - 期限切れセッションの自動クリーンアップ

- **リッチメニュー管理システム** (`src/rich_menu_manager.py`)

  - リッチメニューの作成・削除・管理
  - 画像アップロード機能
  - デフォルトメニュー設定
  - ユーザー別メニュー紐付け

- **映画館検索機能** (`src/movie_theater_search.py`)
  - Google 検索 URL 生成
  - 検索ボタン付きメッセージ作成
  - 複数検索オプション（一般検索、上映スケジュール、地図）
  - 映画館名の妥当性チェック
  - 検索候補の提案機能
  - 場所情報の抽出

#### Phase 2: 週次通知機能

- **今週公開映画通知** (`src/weekly_new_movies.py`)

  - 今週公開予定の映画を取得・通知
  - 映画がない場合は通知をスキップ
  - テスト機能（--test オプション）

- **上映中映画通知** (`src/weekly_now_showing.py`)

  - 過去 1 週間以内に公開された映画を取得・通知
  - 上映館数と限定公開の情報表示
  - 映画がない場合でも情報提供として通知

- **LINE Notifier の拡張**

  - `send_weekly_new_movies_notification()`メソッド
  - `send_weekly_now_showing_notification()`メソッド
  - 専用メッセージフォーマット関数

- **GitHub Actions ワークフロー** (`.github/workflows/weekly-notifications.yml`)
  - 毎週水曜 日本時間 9 時に自動実行
  - 今週公開映画と上映中映画の両方を通知
  - 手動実行も可能（workflow_dispatch）

#### Phase 3: インタラクティブ機能

- **Webhook 処理の大幅な拡張** (`src/webhook_server.py`)

  - Postback イベント対応（リッチメニューボタン）
  - セッション管理の統合
  - 映画検索モード・映画館検索モード
  - Follow/Unfollow イベント対応
  - サポート外メッセージへの対応

- **リッチメニューボタン対応**

  - 🎬 映画検索：セッションモードに入り映画名入力を受け付ける
  - 🎪 映画館検索：セッションモードに入り Google 検索結果を表示
  - 📅 今週公開：即座に今週公開映画を表示
  - 🎭 上映中：即座に上映中映画を表示

- **LINE Notifier の追加機能**

  - `reply_theater_search_result()`：映画館検索結果（ボタン付き）
  - `reply_with_menu_guidance()`：メニュー誘導メッセージ

- **UX 機能**
  - ウェルカムメッセージ（友だち追加時）
  - 不要入力への警告とメニュー誘導
  - 画像・スタンプなどへの対応

#### Phase 4: UI/UX 改善

- **リッチメニュー画像生成スクリプト** (`tools/generate_rich_menu_image.py`)

  - PIL（Pillow）を使用して 2500x1686px の画像を生成
  - 4 つのボタン配置（映画検索、映画館検索、今週公開、上映中）
  - 絵文字とテキストを配置
  - アクセントカラーでボタン枠を描画

- **リッチメニュー設定スクリプト** (`tools/setup_rich_menu.py`)

  - RichMenuManager を使用した自動設定
  - 既存メニューの削除機能
  - 画像アップロード
  - デフォルトメニューへの設定
  - インタラクティブな確認プロンプト

- **ドキュメントの大幅更新**
  - README.md：Phase 1-3 の全機能を反映、アーキテクチャ図追加
  - SETUP_GUIDE.md：完全なセットアップ手順書

#### Phase 5: ドキュメント整備

- **API リファレンス** (`docs/API_REFERENCE.md`)

  - 各モジュールの API 仕様
  - メソッドの詳細説明
  - 使用例とコードサンプル

- **開発者ガイド** (`docs/DEVELOPER_GUIDE.md`)

  - プロジェクト構造
  - コーディング規約
  - 開発環境のセットアップ
  - テストとデバッグ方法
  - 新機能の追加手順
  - ベストプラクティス

- **デプロイガイド** (`docs/DEPLOYMENT_GUIDE.md`)

  - Render.com へのデプロイ手順（推奨）
  - Heroku へのデプロイ手順
  - その他のプラットフォーム情報
  - トラブルシューティング

- **変更履歴** (`CHANGELOG.md`)
- **コントリビューションガイド** (`CONTRIBUTING.md`)

### 変更（Changed）

- `main.py`：週次通知用にリファクタリング
- `scraper.py`：週次取得用のメソッド追加
- `line_notifier.py`：週次通知と Reply 機能の拡張
- `webhook_server.py`：完全な Webhook 処理の実装

### 修正（Fixed）

- import 順序の最適化
- コードフォーマットの改善
- エラーハンドリングの強化

---

## [0.1.0] - 2025-10-01（初期バージョン）

### 追加（Added）

- 基本的な映画情報スクレイピング機能
- LINE Push 通知機能
- GitHub Actions による毎日の自動実行
- 基本的な README とドキュメント

---

## バージョニングについて

このプロジェクトは[セマンティックバージョニング](https://semver.org/lang/ja/)に従います：

- **メジャーバージョン（X.0.0）**：後方互換性のない大きな変更
- **マイナーバージョン（0.X.0）**：後方互換性のある機能追加
- **パッチバージョン（0.0.X）**：後方互換性のあるバグ修正

## 変更タイプの定義

- **追加（Added）**：新機能
- **変更（Changed）**：既存機能の変更
- **非推奨（Deprecated）**：まもなく削除される機能
- **削除（Removed）**：削除された機能
- **修正（Fixed）**：バグ修正
- **セキュリティ（Security）**：脆弱性対応

---

## リンク

- [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/ja/)
- [GitHub Releases](https://github.com/your-username/movie-line-bot/releases)
