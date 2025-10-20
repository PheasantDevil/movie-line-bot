"""LINE Webhook サーバー"""

import json
import os

from flask import Flask, abort, request

from line_notifier import LineNotifier
from movie_theater_search import TheaterSearchManager
from scraper import MovieScraper
from session_manager import SessionManager
from storage import MovieStorage

app = Flask(__name__)

# グローバルセッションマネージャー
session_manager = SessionManager()


def is_movie_search_query(text: str) -> bool:
    """
    メッセージが映画検索クエリかどうかを判定
    
    Args:
        text: メッセージテキスト
        
    Returns:
        bool: 映画検索クエリの場合True
    """
    # シンプルに、テキストに映画名が含まれているかチェック
    # より高度な実装では、自然言語処理やキーワードリストを使用可能
    return len(text) > 0 and len(text) < 100


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    LINE Webhookエンドポイント
    """
    print("=" * 60)
    print("Webhook受信")
    print("=" * 60)
    
    # 署名検証
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    print(f"Body長: {len(body)} bytes")
    print(f"Signature: {signature[:20]}..." if signature else "Signature: なし")
    
    try:
        notifier = LineNotifier()
        print("✓ LineNotifier初期化成功")
        
        # 署名を検証
        if notifier.channel_secret:
            if not notifier.verify_signature(body, signature):
                print("❌ 署名検証失敗")
                abort(400)
            print("✓ 署名検証成功")
        else:
            print("⚠️  チャネルシークレット未設定（署名検証スキップ）")
        
    except ValueError as e:
        print(f"❌ LINE Notifierの初期化エラー: {e}")
        abort(500)
    
    # イベントを処理
    try:
        events = json.loads(body)['events']
        print(f"イベント数: {len(events)}")
        
        for i, event in enumerate(events, 1):
            event_type = event.get('type')
            print(f"\n--- イベント {i}/{len(events)} ---")
            print(f"タイプ: {event_type}")
            
            # メッセージイベント
            if event_type == 'message':
                message_type = event['message'].get('type')
                print(f"メッセージタイプ: {message_type}")
                
                if message_type == 'text':
                    handle_text_message(event, notifier)
                elif message_type in ['image', 'sticker', 'location', 'video', 'audio']:
                    handle_unsupported_message(event, notifier)
            
            # Postbackイベント（リッチメニューボタンなど）
            elif event_type == 'postback':
                print(f"Postback data: {event['postback'].get('data')}")
                handle_postback_event(event, notifier)
            
            # Follow/Unfollowイベント
            elif event_type == 'follow':
                handle_follow_event(event, notifier)
            elif event_type == 'unfollow':
                handle_unfollow_event(event)
        
        print("\n" + "=" * 60)
        print("Webhook処理完了")
        print("=" * 60)
        return 'OK', 200
        
    except Exception as e:
        print(f"❌ Webhookエラー: {e}")
        import traceback
        traceback.print_exc()
        abort(500)


def handle_text_message(event: dict, notifier: LineNotifier):
    """
    テキストメッセージを処理（セッション管理統合版）
    
    Args:
        event: LINEイベント
        notifier: LineNotifierインスタンス
    """
    reply_token = event['replyToken']
    message_text = event['message']['text']
    user_id = event['source'].get('userId', 'unknown')
    
    print(f"受信メッセージ: {message_text} (ユーザーID: {user_id})")
    
    # ユーザーの現在の状態を取得
    user_state = session_manager.get_user_state(user_id)
    
    # セッション状態に応じて処理を分岐
    if user_state == 'movie_search':
        # 映画検索モード
        handle_movie_search(message_text, reply_token, user_id, notifier)
        session_manager.clear_user_state(user_id)
    
    elif user_state == 'theater_search':
        # 映画館検索モード
        handle_theater_search(message_text, reply_token, user_id, notifier)
        session_manager.clear_user_state(user_id)
    
    else:
        # 通常モード：映画検索クエリかどうか判定
        if is_movie_search_query(message_text):
            handle_movie_search(message_text, reply_token, user_id, notifier)
        else:
            # メニュー誘導メッセージ
            notifier.reply_with_menu_guidance(reply_token)


def handle_postback_event(event: dict, notifier: LineNotifier):
    """
    Postbackイベントを処理（リッチメニューボタンなど）
    
    Args:
        event: LINEイベント
        notifier: LineNotifierインスタンス
    """
    reply_token = event['replyToken']
    postback_data = event['postback']['data']
    user_id = event['source'].get('userId', 'unknown')
    
    print(f"▶ Postback受信: {postback_data} (ユーザーID: {user_id})")
    print(f"  Reply Token: {reply_token[:20]}...")
    
    # postback dataをパース
    if postback_data == 'action=movie_search':
        print("  → 映画検索モードに設定")
        # 映画検索モードに設定
        session_manager.set_user_state(user_id, 'movie_search', expires_minutes=10)
        # Quick Reply付きで応答
        quick_reply_items = notifier._get_main_menu_quick_reply_items()
        success = notifier.reply_text_message_with_quick_reply(
            reply_token,
            "🎬 映画検索モードです\n映画のタイトルを入力してください",
            quick_reply_items
        )
        print(f"  Reply結果: {'成功' if success else '失敗'}")
    
    elif postback_data == 'action=theater_search':
        print("  → 映画館検索モードに設定")
        # 映画館検索モードに設定
        session_manager.set_user_state(user_id, 'theater_search', expires_minutes=10)
        # Quick Reply付きで応答
        quick_reply_items = notifier._get_main_menu_quick_reply_items()
        success = notifier.reply_text_message_with_quick_reply(
            reply_token,
            "🎪 映画館検索モードです\n映画館の名前を入力してください\n※入力後、ブラウザが起動します",
            quick_reply_items
        )
        print(f"  Reply結果: {'成功' if success else '失敗'}")
    
    elif postback_data == 'action=weekly_new':
        print("  → 今週公開映画を表示")
        # 今週公開映画を表示
        try:
            scraper = MovieScraper()
            movies = scraper.fetch_upcoming_movies()
            
            if movies:
                print(f"  今週公開映画: {len(movies)}件")
                success = notifier.reply_movie_info(reply_token, movies)
                print(f"  Reply結果: {'成功' if success else '失敗'}")
            else:
                print("  今週公開映画なし")
                quick_reply_items = notifier._get_main_menu_quick_reply_items()
                success = notifier.reply_text_message_with_quick_reply(
                    reply_token,
                    "今週公開予定の映画はありません",
                    quick_reply_items
                )
                print(f"  Reply結果: {'成功' if success else '失敗'}")
        except Exception as e:
            print(f"  ❌ エラー: 今週公開映画の処理に失敗 - {e}")
            import traceback
            traceback.print_exc()
    
    elif postback_data == 'action=now_showing':
        print("  → 上映中映画を表示")
        # 上映中映画を表示
        try:
            scraper = MovieScraper()
            movies = scraper.fetch_movies_released_in_past_week()
            
            if movies:
                print(f"  上映中映画: {len(movies)}件")
                success = notifier.reply_movie_info(reply_token, movies)
                print(f"  Reply結果: {'成功' if success else '失敗'}")
            else:
                print("  上映中映画なし")
                quick_reply_items = notifier._get_main_menu_quick_reply_items()
                success = notifier.reply_text_message_with_quick_reply(
                    reply_token,
                    "現在上映中の映画はありません",
                    quick_reply_items
                )
                print(f"  Reply結果: {'成功' if success else '失敗'}")
        except Exception as e:
            print(f"  ❌ エラー: 上映中映画の処理に失敗 - {e}")
            import traceback
            traceback.print_exc()


def handle_movie_search(query: str, reply_token: str, user_id: str, notifier: LineNotifier):
    """
    映画検索を実行
    
    Args:
        query: 検索クエリ
        reply_token: リプライトークン
        user_id: ユーザーID
        notifier: LineNotifierインスタンス
    """
    print(f"映画検索実行: {query}")
    
    # 映画を検索
    scraper = MovieScraper()
    search_results = scraper.search_movie_by_keyword(query)
    
    # ローカルストレージからも検索（過去/未来の映画情報）
    storage = MovieStorage()
    stored_data = storage.load_movies()
    
    # ストレージからも候補を探す
    if stored_data and 'movies' in stored_data:
        stored_movies = stored_data['movies']
        for movie in stored_movies:
            if query.lower() in movie['title'].lower():
                # 重複チェック
                if not any(m['title'] == movie['title'] for m in search_results):
                    search_results.append(movie)
    
    # 結果をReply
    notifier.reply_movie_info(reply_token, search_results)


def handle_theater_search(query: str, reply_token: str, user_id: str, notifier: LineNotifier):
    """
    映画館検索を実行
    
    Args:
        query: 検索クエリ（映画館名）
        reply_token: リプライトークン
        user_id: ユーザーID
        notifier: LineNotifierインスタンス
    """
    print(f"映画館検索実行: {query}")
    
    # 映画館検索マネージャーを使用
    theater_search = TheaterSearchManager()
    
    # 映画館名の妥当性チェック
    if not theater_search.validate_theater_name(query):
        notifier.reply_text_message(
            reply_token,
            "映画館名が不正です。2文字以上で入力してください。"
        )
        return
    
    # 検索ボタン付きメッセージを送信
    notifier.reply_theater_search_result(reply_token, query)


def handle_unsupported_message(event: dict, notifier: LineNotifier):
    """
    サポートしていないメッセージタイプへの対応
    
    Args:
        event: LINEイベント
        notifier: LineNotifierインスタンス
    """
    reply_token = event['replyToken']
    message_type = event['message'].get('type', 'unknown')
    
    print(f"サポート外メッセージ: {message_type}")
    
    # メニュー誘導メッセージを送信
    notifier.reply_with_menu_guidance(reply_token)


def handle_follow_event(event: dict, notifier: LineNotifier):
    """
    Followイベント（友だち追加）を処理
    
    Args:
        event: LINEイベント
        notifier: LineNotifierインスタンス
    """
    reply_token = event['replyToken']
    user_id = event['source'].get('userId', 'unknown')
    
    print(f"友だち追加: {user_id}")
    
    # ウェルカムメッセージを送信（Quick Reply付き）
    welcome_message = """🎬 映画情報BOTへようこそ！

以下の機能をご利用いただけます：

📅 今週公開：今週公開予定の映画一覧
🎭 上映中：現在上映中の映画一覧
🎬 映画検索：映画名で詳細情報を検索
🎪 映画館検索：映画館を検索

下部のメニューからお選びください！"""
    
    # Quick Reply付きで送信
    quick_reply_items = notifier._get_main_menu_quick_reply_items()
    notifier.reply_text_message_with_quick_reply(reply_token, welcome_message, quick_reply_items)


def handle_unfollow_event(event: dict):
    """
    Unfollowイベント（ブロック）を処理
    
    Args:
        event: LINEイベント
    """
    user_id = event['source'].get('userId', 'unknown')
    print(f"友だち解除: {user_id}")
    
    # セッション情報をクリア
    session_manager.clear_user_state(user_id)


@app.route('/', methods=['GET'])
def index():
    """
    ルートエンドポイント
    """
    return '🎬 Movie LINE Bot Webhook Server is running!', 200


@app.route('/health', methods=['GET'])
def health():
    """
    ヘルスチェックエンドポイント
    """
    return 'OK', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

