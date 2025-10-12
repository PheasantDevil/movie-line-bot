# 📐 技術仕様書

## システム仕様

### 環境

- **プログラミング言語**: Python 3.11+
- **実行環境**: GitHub Actions (Ubuntu latest)
- **依存ライブラリ**:
  - `requests>=2.31.0` - HTTP通信
  - `beautifulsoup4>=4.12.0` - HTMLパース
  - `lxml>=4.9.0` - パーサーバックエンド
  - `python-dotenv>=1.0.0` - 環境変数管理（開発用）

### 外部API

#### LINE Messaging API

- **バージョン**: v2
- **使用機能**: Push Message
- **制限**: 無料プラン 1,000通/月
- **エンドポイント**: `https://api.line.me/v2/bot/message/push`
- **認証**: Bearer Token

#### 映画.com

- **スクレイピング対象**: https://eiga.com/movie/
- **取得情報**: 今週公開の映画一覧
- **アクセス頻度**: 1回/日

### データ仕様

#### movies.json 構造

```typescript
interface MovieData {
  updated_at: string;     // ISO 8601形式の更新日時
  count: number;          // 映画数
  movies: Movie[];        // 映画配列
}

interface Movie {
  title: string;          // 映画タイトル
  url: string;           // 映画.comの詳細URL
  release_date: string;  // 公開日（例: "10月10日"）
  thumbnail: string;     // サムネイル画像URL
  scraped_at: string;    // 取得日時（ISO 8601）
}
```

## API仕様

### MovieScraper

```python
class MovieScraper:
    def __init__(self):
        """スクレイパーを初期化"""
        
    def fetch_upcoming_movies(self) -> List[Dict]:
        """
        今週公開の映画情報を取得
        
        Returns:
            List[Dict]: 映画情報のリスト
            
        Raises:
            requests.RequestException: HTTP通信エラー
        """
```

### MovieStorage

```python
class MovieStorage:
    def __init__(self, data_dir: str = "data"):
        """ストレージを初期化"""
        
    def save_movies(self, movies: List[Dict]) -> bool:
        """
        映画情報を保存
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            bool: 保存成功したか
        """
        
    def load_movies(self) -> Optional[Dict]:
        """
        映画情報を読み込み
        
        Returns:
            Dict | None: 映画データ、存在しない場合はNone
        """
        
    def get_movie_titles(self, data: Optional[Dict] = None) -> set:
        """
        映画タイトルのセットを取得
        
        Args:
            data: 映画データ（Noneの場合は保存データを読み込み）
            
        Returns:
            set: タイトルのセット
        """
```

### MovieDiffDetector

```python
class MovieDiffDetector:
    @staticmethod
    def detect_new_movies(
        current_movies: List[Dict],
        previous_movies: List[Dict]
    ) -> Tuple[List[Dict], List[str]]:
        """
        新着映画を検出
        
        Args:
            current_movies: 現在の映画リスト
            previous_movies: 前回の映画リスト
            
        Returns:
            Tuple[List[Dict], List[str]]: (新着映画リスト, タイトルリスト)
        """
        
    @staticmethod
    def format_summary(
        current_count: int,
        previous_count: int,
        new_count: int
    ) -> str:
        """
        サマリー文字列を生成
        
        Args:
            current_count: 現在の映画数
            previous_count: 前回の映画数
            new_count: 新着映画数
            
        Returns:
            str: フォーマットされたサマリー
        """
```

### LineNotifier

```python
class LineNotifier:
    def __init__(
        self,
        channel_access_token: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        """
        LINE通知クライアントを初期化
        
        Args:
            channel_access_token: LINEチャネルアクセストークン
            user_id: 通知先のユーザーID
            
        Raises:
            ValueError: 必要な環境変数が設定されていない
        """
        
    def send_text_message(self, text: str) -> bool:
        """
        テキストメッセージを送信
        
        Args:
            text: 送信するテキスト
            
        Returns:
            bool: 送信成功したか
            
        Raises:
            requests.RequestException: API通信エラー
        """
        
    def send_movie_notifications(self, movies: List[Dict]) -> bool:
        """
        映画情報を通知
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            bool: 送信成功したか
        """
        
    def test_connection(self) -> bool:
        """
        接続テスト
        
        Returns:
            bool: テスト成功したか
        """
```

## GitHub Actions 仕様

### ワークフロー: check-movies.yml

```yaml
name: 映画情報チェック & LINE通知

on:
  schedule:
    - cron: "0 0 * * *"  # 毎日UTC 0時（JST 9時）
  workflow_dispatch:     # 手動実行可能

jobs:
  check-and-notify:
    runs-on: ubuntu-latest
    
    steps:
      - チェックアウト
      - Python環境セットアップ
      - 依存関係インストール
      - メインスクリプト実行
      - データファイルコミット
      - 変更プッシュ
```

### 必要な Secrets

| Secret名 | 説明 | 取得方法 |
|---------|------|---------|
| LINE_CHANNEL_ACCESS_TOKEN | LINEチャネルアクセストークン | LINE Developers Console |
| LINE_USER_ID | 通知先のLINE User ID | LINE公式アカウントで確認 |

### 必要な Permissions

```yaml
Settings > Actions > General > Workflow permissions:
  - Read and write permissions ✓
```

## セキュリティ仕様

### 機密情報管理

1. **環境変数**
   - すべての機密情報は環境変数で管理
   - GitHub Secretsで暗号化保存
   - コードには一切含めない

2. **アクセス制御**
   - GitHub Actionsのみがデータファイルを変更可能
   - ユーザーはSecrets設定権限が必要

3. **ログ出力**
   - トークンや機密情報はログに出力しない
   - エラーメッセージに機密情報を含めない

### スクレイピング倫理

1. **アクセス頻度**
   - 1日1回のみアクセス
   - サーバー負荷を最小化

2. **User-Agent設定**
   ```python
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
   ```

3. **エラーハンドリング**
   - 失敗時の自動リトライなし
   - 次回実行まで待機

## パフォーマンス仕様

### レスポンス時間目標

| 処理 | 目標時間 | 実測値 |
|------|----------|--------|
| スクレイピング | < 30秒 | ~10秒 |
| 差分検知 | < 5秒 | <1秒 |
| LINE通知 | < 10秒 | ~2秒 |
| データ保存 | < 5秒 | <1秒 |
| **合計** | **< 60秒** | **~15秒** |

### メモリ使用量

- 最大メモリ使用量: ~100MB
- 通常時: ~50MB

### ネットワーク

- データ転送量: ~500KB/実行
- 月間合計: ~15MB

## エラーハンドリング仕様

### エラー種別と対応

| エラー種別 | 対応 | リトライ |
|-----------|------|---------|
| HTTP 404 | ログ出力、処理継続 | なし |
| HTTP 500 | ログ出力、処理終了 | なし |
| タイムアウト | ログ出力、処理終了 | なし |
| パースエラー | 警告出力、処理継続 | なし |
| LINE APIエラー | エラー出力、処理継続 | なし |

### ログレベル

- **INFO**: 正常な処理の進行状況
- **WARNING**: 部分的な失敗（処理は継続）
- **ERROR**: 致命的なエラー（処理終了）

## テスト仕様

### 各モジュールのテスト関数

すべてのモジュールには `test_*()` 関数が実装されています：

```python
# 実行方法
python src/scraper.py        # スクレイパーのテスト
python src/storage.py         # ストレージのテスト
python src/diff_detector.py   # 差分検知のテスト
python src/line_notifier.py   # LINE通知のテスト（環境変数必要）
```

### 統合テスト

```bash
# メインスクリプトの実行（全体テスト）
export LINE_CHANNEL_ACCESS_TOKEN="your_token"
export LINE_USER_ID="your_user_id"
python src/main.py
```

## 拡張仕様

### プラグイン可能な設計

各モジュールは独立しており、容易に拡張可能：

1. **スクレイパーの追加**
   - 新しいサイト用のスクレイパークラスを作成
   - 同じインターフェース（`fetch_upcoming_movies()`）を実装

2. **通知先の追加**
   - Slack, Discord, Telegram などに対応可能
   - 新しい通知クラスを作成

3. **データ保存先の変更**
   - データベース（SQLite, PostgreSQL）に変更可能
   - 同じインターフェース（`save_movies()`, `load_movies()`）を実装

## バージョン管理

### セマンティックバージョニング

```
MAJOR.MINOR.PATCH

MAJOR: 破壊的変更
MINOR: 機能追加（後方互換性あり）
PATCH: バグフィックス
```

現在のバージョン: **1.0.0**

## 制限事項

1. **スクレイピング依存**
   - 映画.comのHTML構造変更に影響を受ける
   - 定期的なメンテナンスが必要な可能性

2. **単一ユーザー対応**
   - 現在は1ユーザーのみに通知
   - 複数ユーザーへの対応は要実装

3. **リアルタイム性**
   - 1日1回の実行のため、即時性はない
   - より頻繁な実行も可能だが推奨しない

4. **データ量制限**
   - JSON保存のため大量データには不向き
   - 現在の映画数（~30件）では問題なし

## 今後の改善案

1. **詳細情報の追加**
   - ジャンル、監督、キャストなど
   - 個別映画ページのスクレイピングが必要

2. **画像付き通知**
   - LINE Flex Messageで画像表示
   - よりリッチな通知

3. **フィルタリング機能**
   - ユーザーの好みに応じた通知
   - 設定ファイルで管理

4. **統計機能**
   - 公開映画数の推移
   - 人気ジャンルの分析

