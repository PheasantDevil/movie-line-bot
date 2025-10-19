# 📚 映画情報通知 LINE Bot ドキュメント

このディレクトリには、映画情報通知 LINE Bot の実装に関する詳細なドキュメントが含まれています。

## 📑 ドキュメント一覧

### 基本ドキュメント

- [実装詳細](implementation_details.md) - 実装の全体像と各モジュールの詳細
- [技術仕様書](technical_specifications.md) - 技術的な仕様とアーキテクチャ
- [LINE API 機能一覧](LINE_API_CAPABILITIES.md) - LINE Messaging API で利用可能な全機能の詳細
- [API 仕様](api_specifications.md) - 外部 API（LINE、映画.com）の使用方法

### 開発ドキュメント

- [開発ガイド](development_guide.md) - ローカル開発環境のセットアップと開発手順
- [テストガイド](testing_guide.md) - テスト方法とデバッグ手順
- [デプロイガイド](deployment_guide.md) - デプロイと CI/CD 設定

### その他

- [FAQ](faq.md) - よくある質問と回答
- [変更履歴](changelog.md) - バージョン履歴と変更内容
- [トラブルシューティング](troubleshooting.md) - 問題解決ガイド

## 📖 クイックリンク

- [プロジェクト README](../README.md)
- [セットアップガイド](../SETUP_GUIDE.md)
- [GitHub Actions ワークフロー](../.github/workflows/README.md)

## 🎯 このプロジェクトについて

映画情報通知 LINE Bot は、映画.com から最新の映画情報を自動取得し、新作映画を LINE で通知するシステムです。

### 主な特徴

- 🔄 **完全自動化**: GitHub Actions で毎日自動実行
- 💰 **完全無料**: 無料枠内で運用可能
- 🎬 **リアルタイム通知**: 新作映画を即座に通知
- 📊 **データ管理**: 映画情報を Git で履歴管理

### 技術スタック

- **言語**: Python 3.11+
- **スクレイピング**: Beautiful Soup 4, Requests
- **通知**: LINE Messaging API
- **CI/CD**: GitHub Actions
- **データ保存**: JSON (Git 管理)

## 🚀 はじめに

1. [README](../README.md)でプロジェクト概要を確認
2. [SETUP_GUIDE](../SETUP_GUIDE.md)でセットアップ
3. [実装詳細](implementation_details.md)で実装内容を理解
4. [開発ガイド](development_guide.md)でローカル開発を開始

## 🤝 貢献

ドキュメントの改善や追加は常に歓迎です！プルリクエストをお待ちしています。
