"""LINE Webhook サーバー"""

import os
import json
from flask import Flask, request, abort

from line_notifier import LineNotifier
from scraper import MovieScraper
from storage import MovieStorage


app = Flask(__name__)


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
    # 署名検証
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        notifier = LineNotifier()
        
        # 署名を検証
        if notifier.channel_secret and not notifier.verify_signature(body, signature):
            print("署名検証失敗")
            abort(400)
        
    except ValueError as e:
        print(f"LINE Notifierの初期化エラー: {e}")
        abort(500)
    
    # イベントを処理
    try:
        events = json.loads(body)['events']
        
        for event in events:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                handle_text_message(event, notifier)
        
        return 'OK', 200
        
    except Exception as e:
        print(f"Webhookエラー: {e}")
        abort(500)


def handle_text_message(event: dict, notifier: LineNotifier):
    """
    テキストメッセージを処理
    
    Args:
        event: LINEイベント
        notifier: LineNotifierインスタンス
    """
    reply_token = event['replyToken']
    message_text = event['message']['text']
    
    print(f"受信メッセージ: {message_text}")
    
    # 映画検索クエリかどうか判定
    if is_movie_search_query(message_text):
        # 映画を検索
        scraper = MovieScraper()
        search_results = scraper.search_movie_by_keyword(message_text)
        
        # ローカルストレージからも検索（過去/未来の映画情報）
        storage = MovieStorage()
        stored_data = storage.load_movies()
        
        # ストレージからも候補を探す
        if stored_data and 'movies' in stored_data:
            stored_movies = stored_data['movies']
            for movie in stored_movies:
                if message_text.lower() in movie['title'].lower():
                    # 重複チェック
                    if not any(m['title'] == movie['title'] for m in search_results):
                        search_results.append(movie)
        
        # 結果をReply
        notifier.reply_movie_info(reply_token, search_results)
    else:
        # 一般的なメッセージへの応答
        notifier.reply_text_message(
            reply_token,
            "映画のタイトルを入力すると、その映画の情報を検索できます。"
        )


@app.route('/health', methods=['GET'])
def health():
    """
    ヘルスチェックエンドポイント
    """
    return 'OK', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

