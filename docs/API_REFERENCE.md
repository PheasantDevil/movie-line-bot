# 📚 API リファレンス

映画情報LINE Botの各モジュールのAPI仕様書です。

## 📋 目次

- [MovieScraper](#moviescraper)
- [LineNotifier](#linenotifier)
- [SessionManager](#sessionmanager)
- [RichMenuManager](#richmenumanager)
- [TheaterSearchManager](#theatersearchmanager)
- [MovieStorage](#moviestorage)

---

## MovieScraper

映画情報のスクレイピングを行うクラス。

### 初期化

```python
from scraper import MovieScraper

scraper = MovieScraper()
```

### メソッド

#### `fetch_upcoming_movies() -> List[Dict]`

今週公開予定の映画情報を取得します。

**返り値:**
```python
[
    {
        'title': '映画タイトル',
        'url': 'https://eiga.com/movie/12345/',
        'release_date': '10月20日',
        'thumbnail': 'https://...',
        'scraped_at': '2025-10-19T12:00:00'
    },
    ...
]
```

**使用例:**
```python
scraper = MovieScraper()
movies = scraper.fetch_upcoming_movies()
print(f"取得件数: {len(movies)}件")
```

#### `fetch_movies_released_in_past_week() -> List[Dict]`

過去1週間以内に公開された映画情報を取得します。

**返り値:**
```python
[
    {
        'title': '映画タイトル',
        'url': 'https://eiga.com/movie/12345/',
        'release_date': '10月15日',
        'thumbnail': 'https://...',
        'theater_count': 300,
        'is_limited_release': False,
        'scraped_at': '2025-10-19T12:00:00'
    },
    ...
]
```

#### `fetch_movies_coming_in_next_week() -> List[Dict]`

先1週間以内に公開予定の映画情報を取得します。

**返り値:** `fetch_movies_released_in_past_week()`と同様

#### `search_movie_by_keyword(keyword: str) -> List[Dict]`

キーワードで映画を検索します。

**パラメータ:**
- `keyword`: 検索キーワード

**返り値:**
```python
[
    {
        'title': '映画タイトル',
        'url': 'https://eiga.com/movie/12345/',
        'release_date': '10月20日',
        'thumbnail': 'https://...',
        'scraped_at': '2025-10-19T12:00:00'
    },
    ...
]
```

**使用例:**
```python
results = scraper.search_movie_by_keyword("アベンジャーズ")
for movie in results:
    print(f"{movie['title']} - {movie['release_date']}")
```

---

## LineNotifier

LINE Messaging APIを使用した通知機能を提供するクラス。

### 初期化

```python
from line_notifier import LineNotifier

notifier = LineNotifier(
    channel_access_token='your_token',  # 省略可（環境変数から取得）
    user_id='your_user_id',              # 省略可（環境変数から取得）
    channel_secret='your_secret'         # 省略可（環境変数から取得）
)
```

### メソッド

#### `send_text_message(text: str) -> bool`

テキストメッセージをPush送信します。

**パラメータ:**
- `text`: 送信するテキスト（最大5,000文字）

**返り値:** 成功時`True`、失敗時`False`

**使用例:**
```python
notifier.send_text_message("テストメッセージ")
```

#### `reply_text_message(reply_token: str, text: str) -> bool`

テキストメッセージをReply送信します。

**パラメータ:**
- `reply_token`: リプライトークン（Webhookイベントから取得）
- `text`: 送信するテキスト

**返り値:** 成功時`True`、失敗時`False`

#### `send_weekly_new_movies_notification(movies: List[Dict]) -> bool`

今週公開映画の週次通知を送信します。

**パラメータ:**
- `movies`: 映画情報のリスト

**返り値:** 成功時`True`、失敗時`False`

**使用例:**
```python
movies = scraper.fetch_upcoming_movies()
notifier.send_weekly_new_movies_notification(movies)
```

#### `send_weekly_now_showing_notification(movies: List[Dict]) -> bool`

上映中映画の週次通知を送信します。

#### `reply_movie_info(reply_token: str, movies: List[Dict]) -> bool`

映画検索結果をReply送信します。

**パラメータ:**
- `reply_token`: リプライトークン
- `movies`: 映画情報のリスト

**使用例:**
```python
# Webhookイベント内で
results = scraper.search_movie_by_keyword(query)
notifier.reply_movie_info(reply_token, results)
```

#### `reply_theater_search_result(reply_token: str, theater_name: str) -> bool`

映画館検索結果（ボタン付き）をReply送信します。

**パラメータ:**
- `reply_token`: リプライトークン
- `theater_name`: 映画館名

#### `reply_with_menu_guidance(reply_token: str) -> bool`

メニュー誘導メッセージをReply送信します。

#### `verify_signature(body: str, signature: str) -> bool`

Webhook署名を検証します。

**パラメータ:**
- `body`: リクエストボディ
- `signature`: X-Line-Signatureヘッダーの値

**返り値:** 署名が正しい場合`True`

---

## SessionManager

ユーザーセッション管理を提供するクラス。

### 初期化

```python
from session_manager import SessionManager

session_manager = SessionManager(data_dir="data")
```

### メソッド

#### `set_user_state(user_id: str, state: str, expires_minutes: int = 30) -> bool`

ユーザーの状態を設定します。

**パラメータ:**
- `user_id`: ユーザーID
- `state`: 状態（'movie_search', 'theater_search', 'idle'など）
- `expires_minutes`: セッション有効期限（分）

**返り値:** 成功時`True`

**使用例:**
```python
# 映画検索モードに設定
session_manager.set_user_state(user_id, 'movie_search', expires_minutes=10)
```

#### `get_user_state(user_id: str) -> Optional[str]`

ユーザーの状態を取得します。

**パラメータ:**
- `user_id`: ユーザーID

**返り値:** 状態文字列、セッションがない場合は`None`

**使用例:**
```python
state = session_manager.get_user_state(user_id)
if state == 'movie_search':
    # 映画検索処理
    pass
```

#### `clear_user_state(user_id: str) -> bool`

ユーザーの状態をクリアします。

**パラメータ:**
- `user_id`: ユーザーID

**返り値:** 成功時`True`

#### `get_session_info(user_id: str) -> Optional[Dict]`

ユーザーのセッション情報を取得します。

**返り値:**
```python
{
    'state': 'movie_search',
    'created_at': '2025-10-19T12:00:00',
    'expires_at': '2025-10-19T12:30:00',
    'last_activity': '2025-10-19T12:15:00'
}
```

#### `get_active_sessions_count() -> int`

アクティブなセッション数を取得します。

#### `cleanup_all_expired_sessions() -> int`

すべての期限切れセッションをクリーンアップします。

**返り値:** クリーンアップしたセッション数

---

## RichMenuManager

リッチメニュー管理を提供するクラス。

### 初期化

```python
from rich_menu_manager import RichMenuManager

manager = RichMenuManager(channel_access_token='your_token')
```

### メソッド

#### `create_movie_search_menu() -> str`

映画検索用リッチメニューを作成します。

**返り値:** 作成されたリッチメニューID

**使用例:**
```python
menu_id = manager.create_movie_search_menu()
print(f"メニューID: {menu_id}")
```

#### `upload_menu_image(menu_id: str, image_path: str) -> bool`

リッチメニュー画像をアップロードします。

**パラメータ:**
- `menu_id`: リッチメニューID
- `image_path`: 画像ファイルのパス

**返り値:** 成功時`True`

#### `set_default_menu(menu_id: str) -> bool`

デフォルトリッチメニューに設定します。

#### `link_menu_to_user(user_id: str, menu_id: str) -> bool`

特定のユーザーにリッチメニューを紐付けます。

#### `get_menu_list() -> List[Dict]`

リッチメニュー一覧を取得します。

**返り値:**
```python
[
    {
        'richMenuId': 'richmenu-xxx',
        'name': '映画Bot メインメニュー',
        'size': {'width': 2500, 'height': 1686},
        'selected': True,
        ...
    },
    ...
]
```

#### `delete_menu(menu_id: str) -> bool`

リッチメニューを削除します。

#### `setup_complete_menu(image_path: str) -> Optional[str]`

完全なリッチメニューセットアップ（作成→画像アップロード→デフォルト設定）を実行します。

**パラメータ:**
- `image_path`: 画像ファイルのパス

**返り値:** 作成されたリッチメニューID、失敗時`None`

**使用例:**
```python
menu_id = manager.setup_complete_menu('assets/rich_menu.png')
if menu_id:
    print(f"リッチメニュー設定完了: {menu_id}")
```

---

## TheaterSearchManager

映画館検索機能を提供するクラス。

### 初期化

```python
from movie_theater_search import TheaterSearchManager

theater_search = TheaterSearchManager()
```

### メソッド

#### `generate_google_search_url(theater_name: str, search_type: str = 'general', location: Optional[str] = None) -> str`

Google検索URLを生成します。

**パラメータ:**
- `theater_name`: 映画館名
- `search_type`: 検索タイプ（'general', 'location', 'movie', 'maps'）
- `location`: 場所（locationタイプの場合）

**返り値:** Google検索URL

**使用例:**
```python
url = theater_search.generate_google_search_url("TOHOシネマズ渋谷")
# https://www.google.com/search?q=TOHO%E3%82%B7%E3%83%8D%E3%83%9E%E3%82%BA...
```

#### `create_search_button_message(theater_name: str, search_type: str = 'general', location: Optional[str] = None) -> Dict`

検索ボタン付きメッセージを作成します。

**返り値:**
```python
{
    'type': 'template',
    'altText': 'TOHOシネマズ渋谷の検索結果',
    'template': {
        'type': 'buttons',
        'text': '「TOHOシネマズ渋谷」の検索結果を表示します',
        'actions': [...]
    }
}
```

#### `validate_theater_name(theater_name: str) -> bool`

映画館名の妥当性をチェックします。

**パラメータ:**
- `theater_name`: 映画館名

**返り値:** 妥当な場合`True`

**使用例:**
```python
if theater_search.validate_theater_name(query):
    # 検索処理
    pass
else:
    print("映画館名が不正です")
```

#### `suggest_search_terms(partial_name: str) -> List[str]`

部分的な映画館名から検索候補を提案します。

**パラメータ:**
- `partial_name`: 部分的な映画館名

**返り値:** 検索候補のリスト

**使用例:**
```python
suggestions = theater_search.suggest_search_terms("TOHO")
# ['TOHOシネマズ']
```

#### `extract_location_from_query(query: str) -> Optional[str]`

クエリから場所情報を抽出します。

**返り値:** 抽出された場所、見つからない場合は`None`

---

## MovieStorage

映画情報の永続化を提供するクラス。

### 初期化

```python
from storage import MovieStorage

storage = MovieStorage(data_dir="data")
```

### メソッド

#### `save_movies(movies: List[Dict]) -> bool`

映画情報を保存します。

**パラメータ:**
- `movies`: 映画情報のリスト

**返り値:** 成功時`True`

**使用例:**
```python
movies = scraper.fetch_upcoming_movies()
storage.save_movies(movies)
```

#### `load_movies() -> Optional[Dict]`

保存された映画情報を読み込みます。

**返り値:**
```python
{
    'movies': [...],
    'last_updated': '2025-10-19T12:00:00'
}
```

#### `get_movies_by_date(date_str: str) -> List[Dict]`

特定の日付の映画情報を取得します。

**パラメータ:**
- `date_str`: 日付文字列（例: '10月20日'）

**返り値:** 該当する映画情報のリスト

---

## エラーハンドリング

すべてのメソッドは例外をキャッチし、エラーメッセージを出力します。

```python
try:
    movies = scraper.fetch_upcoming_movies()
except Exception as e:
    print(f"エラー: {e}")
    import traceback
    traceback.print_exc()
```

## ベストプラクティス

### 1. 環境変数の使用

```python
import os

# 環境変数から取得
token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
user_id = os.getenv('LINE_USER_ID')
```

### 2. エラーハンドリング

```python
notifier = LineNotifier()
success = notifier.send_text_message("テスト")
if not success:
    print("送信に失敗しました")
```

### 3. セッション管理

```python
# セッションの設定
session_manager.set_user_state(user_id, 'movie_search', expires_minutes=10)

# セッションの確認
state = session_manager.get_user_state(user_id)
if state:
    # 状態に応じた処理
    pass

# セッションのクリア
session_manager.clear_user_state(user_id)
```

---

## 更新履歴

- 2025-10-19: 初版作成

