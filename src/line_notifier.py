"""LINE Messaging APIを使った通知機能"""

import os
import hashlib
import hmac
import base64
from typing import Dict, List, Optional

import requests


class LineNotifier:
    """LINE Messaging APIで通知を送信するクラス"""
    
    def __init__(
        self,
        channel_access_token: Optional[str] = None,
        user_id: Optional[str] = None,
        channel_secret: Optional[str] = None
    ):
        """
        初期化
        
        Args:
            channel_access_token: LINEチャネルアクセストークン
            user_id: 通知先のユーザーID
            channel_secret: LINEチャネルシークレット（Webhook署名検証用）
        """
        self.channel_access_token = channel_access_token or os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.user_id = user_id or os.getenv('LINE_USER_ID')
        self.channel_secret = channel_secret or os.getenv('LINE_CHANNEL_SECRET')
        self.push_api_url = 'https://api.line.me/v2/bot/message/push'
        self.reply_api_url = 'https://api.line.me/v2/bot/message/reply'
        
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
            response = requests.post(self.push_api_url, headers=headers, json=data, timeout=30)
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
    
    def send_weekly_notification(
        self,
        past_week_movies: List[Dict],
        next_week_movies: List[Dict]
    ) -> bool:
        """
        週次通知を送信（過去1週間と先1週間の映画情報）
        
        Args:
            past_week_movies: 過去1週間以内に公開された映画リスト
            next_week_movies: 先1週間以内に公開予定の映画リスト
            
        Returns:
            bool: 送信が成功したかどうか
        """
        message = self._format_weekly_message(past_week_movies, next_week_movies)
        return self.send_text_message(message)
    
    def _format_weekly_message(
        self,
        past_week_movies: List[Dict],
        next_week_movies: List[Dict]
    ) -> str:
        """
        週次通知メッセージを整形
        
        Args:
            past_week_movies: 過去1週間以内に公開された映画リスト
            next_week_movies: 先1週間以内に公開予定の映画リスト
            
        Returns:
            str: 整形されたメッセージ
        """
        lines = []
        lines.append("🎬 週刊映画情報")
        lines.append("=" * 30)
        lines.append("")
        
        # 過去1週間以内に公開された映画
        lines.append("【過去1週間以内に公開された映画】")
        if past_week_movies:
            for i, movie in enumerate(past_week_movies[:10], 1):
                lines.append(f"{i}. {movie['title']}")
                lines.append(f"   公開日: {movie['release_date']}")
                lines.append(f"   {movie['url']}")
                lines.append("")
        else:
            lines.append("該当する映画はありません")
            lines.append("")
        
        lines.append("=" * 30)
        lines.append("")
        
        # 先1週間以内に公開予定の映画
        lines.append("【先1週間以内に公開予定の映画】")
        if next_week_movies:
            for i, movie in enumerate(next_week_movies[:10], 1):
                title_line = f"{i}. {movie['title']}"
                
                # 上映館数情報を追加
                if movie.get('is_limited_release'):
                    theater_count = movie.get('theater_count')
                    if theater_count:
                        title_line += f" ⚠️ 限定公開({theater_count}館)"
                    else:
                        title_line += " ⚠️ 限定公開"
                elif movie.get('theater_count'):
                    title_line += f" ({movie['theater_count']}館)"
                
                lines.append(title_line)
                lines.append(f"   公開日: {movie['release_date']}")
                lines.append(f"   {movie['url']}")
                lines.append("")
        else:
            lines.append("該当する映画はありません")
            lines.append("")
        
        return "\n".join(lines)
    
    def reply_text_message(self, reply_token: str, text: str) -> bool:
        """
        テキストメッセージをReply
        
        Args:
            reply_token: リプライトークン
            text: 送信するテキスト
            
        Returns:
            bool: 送信が成功したかどうか
        """
        headers = {
            'Authorization': f'Bearer {self.channel_access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'replyToken': reply_token,
            'messages': [
                {
                    'type': 'text',
                    'text': text
                }
            ]
        }
        
        try:
            response = requests.post(self.reply_api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            print("✓ LINE Replyを送信しました")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: LINE Replyの送信に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def reply_movie_info(self, reply_token: str, movies: List[Dict]) -> bool:
        """
        映画情報をReply
        
        Args:
            reply_token: リプライトークン
            movies: 映画情報のリスト
            
        Returns:
            bool: 送信が成功したかどうか
        """
        if not movies:
            message = "該当する映画が見つかりませんでした。"
        else:
            message = self._format_search_result_message(movies)
        
        return self.reply_text_message(reply_token, message)
    
    def _format_search_result_message(self, movies: List[Dict]) -> str:
        """
        検索結果メッセージを整形
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            str: 整形されたメッセージ
        """
        lines = []
        lines.append(f"🎬 検索結果 ({len(movies)}件)")
        lines.append("=" * 30)
        lines.append("")
        
        for i, movie in enumerate(movies[:5], 1):  # 最大5件まで
            lines.append(f"【{i}】{movie['title']}")
            lines.append(f"公開日: {movie['release_date']}")
            
            # 上映館数情報があれば追加
            if movie.get('theater_count'):
                lines.append(f"上映館数: {movie['theater_count']}館")
            if movie.get('is_limited_release'):
                lines.append("⚠️ 限定公開")
            
            lines.append(f"詳細: {movie['url']}")
            lines.append("")
        
        if len(movies) > 5:
            lines.append(f"...他 {len(movies) - 5}件")
        
        return "\n".join(lines)
    
    def verify_signature(self, body: str, signature: str) -> bool:
        """
        Webhook署名を検証
        
        Args:
            body: リクエストボディ
            signature: X-Line-Signatureヘッダーの値
            
        Returns:
            bool: 署名が正しい場合True
        """
        if not self.channel_secret:
            print("警告: チャネルシークレットが設定されていません")
            return False
        
        hash_digest = hmac.new(
            self.channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        expected_signature = base64.b64encode(hash_digest).decode('utf-8')
        
        return signature == expected_signature
    
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

