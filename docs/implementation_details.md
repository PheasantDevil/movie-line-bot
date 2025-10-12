# 🔧 実装詳細

映画情報通知 LINE Bot の実装に関する詳細なドキュメントです。

## 📋 目次

- [プロジェクト概要](#プロジェクト概要)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [モジュール詳細](#モジュール詳細)
- [データフロー](#データフロー)
- [実装のポイント](#実装のポイント)

## プロジェクト概要

### 目的

日本国内の新作映画情報を自動で取得し、LINE 経由でユーザーに通知するシステムを構築する。

### 要件

- ✅ 映画.com から今週公開の映画情報を取得
- ✅ 前回との差分を検知して新作のみを通知
- ✅ LINE Messaging API で自動通知
- ✅ GitHub Actions で定期実行（毎日 1 回）
- ✅ 完全無料で運用可能

### 非機能要件

- **可用性**: GitHub Actions の稼働率に依存（99.9%+）
- **パフォーマンス**: 実行時間 < 3 分
- **拡張性**: 簡単に通知内容をカスタマイズ可能
- **保守性**: コードは読みやすく、モジュール化

## システムアーキテクチャ

### 全体構成

```
┌─────────────────┐
│  GitHub Actions │
│   (Scheduler)   │
└────────┬────────┘
         │ 毎日9時実行
         ▼
┌─────────────────┐
│   main.py       │
│  (メイン処理)    │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ▼         ▼        ▼          ▼
┌────────┐ ┌─────┐ ┌──────┐ ┌──────────┐
│scraper │ │store│ │ diff │ │ notifier │
└───┬────┘ └──┬──┘ └──┬───┘ └────┬─────┘
    │         │       │          │
    ▼         ▼       ▼          ▼
 映画.com   JSON   新着検知   LINE API
```

### コンポーネント図

```
┌──────────────────────────────────────────┐
│         映画情報通知システム              │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────┐      ┌────────────┐    │
│  │  Scraper   │─────>│  Storage   │    │
│  └────────────┘      └────────────┘    │
│         │                   │           │
│         │                   ▼           │
│         │            ┌────────────┐    │
│         └───────────>│   Diff     │    │
│                      │ Detector   │    │
│                      └────────────┘    │
│                             │           │
│                             ▼           │
│                      ┌────────────┐    │
│                      │   LINE     │    │
│                      │ Notifier   │    │
│                      └────────────┘    │
│                                          │
└──────────────────────────────────────────┘
```

## モジュール詳細

### 1. `main.py` - メインエントリーポイント

**役割**: システム全体の制御フロー

**処理フロー**:

```python
1. 前回のデータを読み込み (storage.load_movies())
2. 最新の映画情報を取得 (scraper.fetch_upcoming_movies())
3. 差分を検知 (detector.detect_new_movies())
4. 新作があればLINE通知 (notifier.send_movie_notifications())
5. 最新データを保存 (storage.save_movies())
```

**実装詳細**:

```python
def main():
    # 1. データ読み込み
    storage = MovieStorage()
    previous_data = storage.load_movies()
    previous_movies = previous_data['movies'] if previous_data else []

    # 2. 最新情報取得
    scraper = MovieScraper()
    current_movies = scraper.fetch_upcoming_movies()

    # 3. 差分検知
    detector = MovieDiffDetector()
    new_movies, new_titles = detector.detect_new_movies(
        current_movies, previous_movies
    )

    # 4. LINE通知（新作がある場合のみ）
    if new_movies and 環境変数が設定されている:
        notifier = LineNotifier()
        notifier.send_movie_notifications(new_movies)

    # 5. データ保存
    storage.save_movies(current_movies)
```

### 2. `scraper.py` - スクレイピングモジュール

**役割**: 映画.com から映画情報を取得

**主要クラス**: `MovieScraper`

**実装のポイント**:

1. **HTML 構造の解析**

   ```python
   # 「今週公開の映画」セクションを探す
   this_week_header = soup.find('h2', class_=['title-xlarge', 'margin-top20'])
   movie_list = this_week_header.find_next('ul', class_='slide-menu')
   ```

2. **データ抽出**

   ```python
   for li in movie_list.find_all('li'):
       # タイトル: imgのalt属性から取得
       img = link.find('img')
       title = img['alt']

       # 公開日: pタグから取得
       published_elem = li.find('p', class_='published')
       release_date = published_elem.get_text(strip=True)
   ```

3. **エラーハンドリング**
   - タイムアウト: 30 秒
   - リトライ: なし（GitHub Actions で再実行）
   - 部分的な失敗: 個別の映画で失敗しても続行

**取得データ構造**:

```python
{
    'title': str,           # 映画タイトル
    'url': str,            # 映画.comのURL
    'release_date': str,   # 公開日（例: "10月10日"）
    'thumbnail': str,      # サムネイル画像URL
    'scraped_at': str      # 取得日時（ISO 8601形式）
}
```

### 3. `storage.py` - データ永続化モジュール

**役割**: 映画データの保存と読み込み

**主要クラス**: `MovieStorage`

**データ形式** (`data/movies.json`):

```json
{
  "updated_at": "2025-10-12T19:56:34.452419",
  "count": 28,
  "movies": [
    {
      "title": "映画タイトル",
      "url": "https://eiga.com/movie/12345/",
      "release_date": "10月10日",
      "thumbnail": "https://...",
      "scraped_at": "2025-10-12T19:56:30.123456"
    }
  ]
}
```

**実装のポイント**:

1. **JSON ファイルによる永続化**

   - シンプルで読みやすい
   - Git で履歴管理可能
   - データベース不要（コスト削減）

2. **データの完全性**

   ```python
   # 保存時に必ず updated_at と count を含める
   data = {
       'updated_at': datetime.now().isoformat(),
       'count': len(movies),
       'movies': movies
   }
   ```

3. **差分検知用のユーティリティ**
   ```python
   def get_movie_titles(self, data=None) -> set:
       """タイトルのセットを返す（高速な差分検知用）"""
       return {movie['title'] for movie in data['movies']}
   ```

### 4. `diff_detector.py` - 差分検知モジュール

**役割**: 新作映画を検出

**主要クラス**: `MovieDiffDetector`

**アルゴリズム**:

```python
def detect_new_movies(current_movies, previous_movies):
    # 1. 前回のタイトルセットを作成（O(n)）
    previous_titles = {movie['title'] for movie in previous_movies}

    # 2. 現在の映画から新作を検出（O(m)）
    new_movies = []
    for movie in current_movies:
        if movie['title'] not in previous_titles:  # O(1) ハッシュテーブル検索
            new_movies.append(movie)

    return new_movies
```

**計算量**: O(n + m)

- n: 前回の映画数
- m: 現在の映画数

**実装のポイント**:

1. **セットを使った高速検索**

   - リストでの検索: O(n)
   - セットでの検索: O(1)

2. **シンプルな差分ロジック**
   - タイトルのみで判定（URL は変わる可能性がある）
   - 削除された映画は通知しない

### 5. `line_notifier.py` - LINE 通知モジュール

**役割**: LINE Messaging API で通知を送信

**主要クラス**: `LineNotifier`

**LINE Messaging API 仕様**:

- **エンドポイント**: `https://api.line.me/v2/bot/message/push`
- **認証**: Bearer Token
- **制限**: 無料プランで 1,000 通/月

**メッセージフォーマット**:

```python
def _format_movie_message(self, movies: List[Dict]) -> str:
    header = f"🎬 新作映画情報 ({len(movies)}件)\n"
    header += "=" * 30 + "\n\n"

    movie_texts = []
    for i, movie in enumerate(movies[:10], 1):  # 最大10件
        text = f"【{i}】{movie['title']}\n"
        text += f"📅 公開日: {movie['release_date']}\n"
        text += f"🔗 {movie['url']}\n"
        movie_texts.append(text)

    return header + "\n".join(movie_texts)
```

**実装のポイント**:

1. **環境変数による設定**

   ```python
   self.channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
   self.user_id = os.getenv('LINE_USER_ID')
   ```

2. **エラーハンドリング**

   - API エラー時は詳細なログを出力
   - 失敗してもプログラムは継続

3. **メッセージの最適化**
   - 最大 10 件まで通知（LINE の文字数制限考慮）
   - 絵文字で視認性向上

## データフロー

### 通常実行時のフロー

```
1. GitHub Actions トリガー
   ↓
2. 環境変数読み込み
   ↓
3. 前回データ読み込み (movies.json)
   ↓
4. 映画.comスクレイピング
   ↓
5. 差分検知
   ↓
6. 新作あり？
   ├─ YES → LINE通知送信
   └─ NO  → スキップ
   ↓
7. 最新データ保存 (movies.json)
   ↓
8. Gitコミット & プッシュ
   ↓
9. 完了
```

### 初回実行時のフロー

```
1. 前回データなし
   ↓
2. 映画.comスクレイピング
   ↓
3. 全映画が「新作」扱い
   ↓
4. LINE通知送信（全件）
   ↓
5. データ保存
```

## 実装のポイント

### 1. なぜスクレイピングなのか？

**理由**:

- 映画.com に公式 API が存在しない
- RSS フィードも提供されていない
- スクレイピングが唯一の手段

**配慮点**:

- User-Agent を設定してボットであることを明示
- 1 日 1 回のみアクセス（サーバー負荷を最小化）
- robots.txt に準拠

### 2. なぜ GitHub Actions なのか？

**メリット**:

- ✅ 無料（2,000 分/月）
- ✅ サーバー不要
- ✅ 設定が簡単
- ✅ ログが見やすい

**代替案との比較**:
| 方法 | コスト | メンテナンス | 可用性 |
|------|--------|------------|--------|
| GitHub Actions | 無料 | 簡単 | 高 |
| AWS Lambda | 無料枠あり | 中 | 非常に高 |
| VPS | 有料 | 難 | 中 |
| ローカル PC | 無料 | 難 | 低 |

### 3. なぜ JSON で保存するのか？

**メリット**:

- ✅ シンプルで読みやすい
- ✅ Git で履歴管理可能
- ✅ データベース不要
- ✅ バックアップ不要（Git 履歴がバックアップ）

**デメリット**:

- ❌ データ量が増えると遅くなる（現状 28 件なので問題なし）
- ❌ 複雑なクエリができない（不要）

### 4. エラーハンドリング戦略

**方針**: Fail-fast but continue

```python
try:
    # 個別の映画情報取得
    movie_data = extract_movie_data(item)
except Exception as e:
    print(f"警告: {e}")
    continue  # 次の映画へ
```

**理由**:

- 一部の映画で失敗しても、他の映画は通知したい
- GitHub Actions のログで問題を確認できる
- 次回実行で自動リカバリー

### 5. セキュリティ

**環境変数による機密情報管理**:

```yaml
env:
  LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
  LINE_USER_ID: ${{ secrets.LINE_USER_ID }}
```

**理由**:

- トークンをコードに含めない
- GitHub Secrets で暗号化保存
- ログに出力されない

## パフォーマンス

### 実行時間

| 処理           | 時間       |
| -------------- | ---------- |
| スクレイピング | ~10 秒     |
| 差分検知       | <1 秒      |
| LINE 通知      | ~2 秒      |
| データ保存     | <1 秒      |
| **合計**       | **~15 秒** |

### リソース使用量

- メモリ: ~50MB
- CPU: 最小限
- ネットワーク: ~500KB（HTML + 画像なし）

## 拡張性

### 簡単に追加できる機能

1. **複数ユーザーへの通知**

   ```python
   user_ids = ['U1234...', 'U5678...']
   for user_id in user_ids:
       notifier.send_to_user(user_id, message)
   ```

2. **フィルタリング**

   ```python
   # アニメ映画のみ通知
   anime_movies = [m for m in movies if 'アニメ' in m.get('genre', '')]
   ```

3. **他のサイトからも取得**

   ```python
   yahoo_scraper = YahooMovieScraper()
   yahoo_movies = yahoo_scraper.fetch_movies()
   all_movies = merge_movies(eiga_movies, yahoo_movies)
   ```

4. **Webhook 対応**
   - LINE Bot で「次週の映画を教えて」などのコマンド対応

## まとめ

このシステムは、シンプルでメンテナンスしやすく、完全無料で運用できる設計になっています。各モジュールは独立しており、テストや拡張が容易です。
