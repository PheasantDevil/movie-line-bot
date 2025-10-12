"""LINE Messaging APIを使った通知機能"""

import os
import requests
from typing import List, Dict, Optional


class LineNotifier:
    """LINE Messaging APIで通知を送信するクラス"""
    
    def __init__(
        self,
        channel_access_token: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        """
        初期化
        
        Args:
            channel_access_token: LINEチャネルアクセストークン
            user_id: 通知先のユーザーID
        """
        self.channel_access_token = channel_access_token or os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.user_id = user_id or os.getenv('LINE_USER_ID')
        self.api_url = 'https://api.line.me/v2/bot/message/push'
        
        if not self.channel_access_token:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
        if not self.user_id:
            raise ValueError("LINE_USER_ID が設定されていません")
    
    def send_text_message(self, text: str) -> bool:
        """
        テキストメッセージを送信
        
        Args:
            text: 送信するテキスト
            
        Returns:
            bool: 送信が成功したかどうか
        """
        headers = {
            'Authorization': f'Bearer {self.channel_access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'to': self.user_id,
            'messages': [
                {
                    'type': 'text',
                    'text': text
                }
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            print("✓ LINE通知を送信しました")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: LINE通知の送信に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def send_movie_notifications(self, movies: List[Dict]) -> bool:
        """
        新作映画情報を通知
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            bool: 送信が成功したかどうか
        """
        if not movies:
            print("通知する映画がありません")
            return True
        
        # メッセージを作成
        message = self._format_movie_message(movies)
        
        # 送信
        return self.send_text_message(message)
    
    def _format_movie_message(self, movies: List[Dict]) -> str:
        """
        映画情報をメッセージ形式に整形
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            str: 整形されたメッセージ
        """
        header = f"🎬 新作映画情報 ({len(movies)}件)\n"
        header += "=" * 30 + "\n\n"
        
        movie_texts = []
        for i, movie in enumerate(movies[:10], 1):  # 最大10件まで
            text = f"【{i}】{movie['title']}\n"
            text += f"📅 公開日: {movie['release_date']}\n"
            text += f"🔗 {movie['url']}\n"
            movie_texts.append(text)
        
        footer = ""
        if len(movies) > 10:
            footer = f"\n...他 {len(movies) - 10}件"
        
        return header + "\n".join(movie_texts) + footer
    
    def test_connection(self) -> bool:
        """
        接続テスト（簡単なメッセージを送信）
        
        Returns:
            bool: テストが成功したかどうか
        """
        test_message = "🎬 映画情報通知BOT\n接続テストメッセージです"
        print("LINE通知の接続テストを実行します...")
        return self.send_text_message(test_message)


def test_notifier():
    """通知機能のテスト"""
    print("LINE通知機能のテスト...\n")
    
    # 環境変数の確認
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not token or not user_id:
        print("⚠️  環境変数が設定されていません")
        print()
        print("以下の環境変数を設定してください:")
        print("  export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
        print("  export LINE_USER_ID='your_user_id_here'")
        print()
        print("環境変数設定後、以下のコマンドでテストを実行してください:")
        print("  python3 src/line_notifier.py")
        return
    
    print("✓ 環境変数が設定されています")
    print(f"  TOKEN: {token[:20]}...")
    print(f"  USER_ID: {user_id}")
    print()
    
    try:
        notifier = LineNotifier()
        
        # 接続テスト
        notifier.test_connection()
        print()
        
        # サンプル映画情報でテスト
        sample_movies = [
            {
                'title': 'テスト映画1',
                'url': 'https://eiga.com/movie/12345/',
                'release_date': '10月10日'
            },
            {
                'title': 'テスト映画2',
                'url': 'https://eiga.com/movie/12346/',
                'release_date': '10月11日'
            }
        ]
        
        print("サンプル映画情報で通知をテストします...")
        notifier.send_movie_notifications(sample_movies)
        
    except ValueError as e:
        print(f"エラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")


if __name__ == "__main__":
    test_notifier()

