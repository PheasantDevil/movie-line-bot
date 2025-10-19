"""今週公開映画の週次通知スクリプト"""

import os
import sys
from datetime import datetime

from line_notifier import LineNotifier
from scraper import MovieScraper


def main():
    """今週公開映画の週次通知メイン処理"""
    print("=" * 60)
    print("今週公開映画 週次通知 - 実行開始")
    print("=" * 60)
    print()
    
    # 1. スクレイパーを初期化
    scraper = MovieScraper()
    
    # 2. 今週公開の映画を取得
    print("--- 今週公開映画の取得 ---")
    movies = scraper.fetch_upcoming_movies()
    print(f"取得件数: {len(movies)}件")
    print()
    
    # 3. 映画がない場合は通知をスキップ
    if not movies:
        print("ℹ️  今週公開の映画がないため、通知をスキップします")
        print("=" * 60)
        print("処理が完了しました")
        print("=" * 60)
        return
    
    # 4. 通知を送信
    print("--- LINE通知 ---")
    if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') and os.getenv('LINE_USER_ID'):
        try:
            notifier = LineNotifier()
            success = notifier.send_weekly_new_movies_notification(movies)
            
            if success:
                print("✓ 今週公開映画の通知を送信しました")
                print()
                print("【今週公開の映画】")
                for i, movie in enumerate(movies[:10], 1):  # 最大10件まで表示
                    print(f"  {i}. {movie['title']} ({movie['release_date']})")
                if len(movies) > 10:
                    print(f"  ...他 {len(movies) - 10}件")
                print()
            else:
                print("⚠️  今週公開映画の通知送信に失敗しました")
                
        except Exception as e:
            print(f"エラー: 今週公開映画の通知でエラーが発生しました - {e}")
            import traceback
            traceback.print_exc()
    else:
        print("ℹ️  LINE通知は環境変数が設定されていないためスキップされました")
        print("   以下の環境変数を設定してください:")
        print("   - LINE_CHANNEL_ACCESS_TOKEN")
        print("   - LINE_USER_ID")
    print()
    
    print("=" * 60)
    print("処理が完了しました")
    print("=" * 60)


def test_weekly_new_movies():
    """今週公開映画通知のテスト"""
    print("今週公開映画通知のテスト...\n")
    
    # 環境変数の確認
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not token or not user_id:
        print("⚠️  環境変数が設定されていません")
        print("以下の環境変数を設定してください:")
        print("  export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
        print("  export LINE_USER_ID='your_user_id_here'")
        print()
        print("環境変数設定後、以下のコマンドでテストを実行してください:")
        print("  python3 src/weekly_new_movies.py")
        return
    
    print("✓ 環境変数が設定されています")
    print(f"  TOKEN: {token[:20]}...")
    print(f"  USER_ID: {user_id}")
    print()
    
    try:
        # スクレイパーのテスト
        print("1. 映画情報の取得テスト")
        scraper = MovieScraper()
        movies = scraper.fetch_upcoming_movies()
        print(f"   取得件数: {len(movies)}件")
        
        if movies:
            print("   取得した映画（最初の3件）:")
            for i, movie in enumerate(movies[:3], 1):
                print(f"     {i}. {movie['title']} ({movie['release_date']})")
        
        print("\n2. LINE通知のテスト")
        notifier = LineNotifier()
        
        # サンプル映画情報でテスト
        sample_movies = [
            {
                'title': 'テスト映画1',
                'url': 'https://eiga.com/movie/test1/',
                'release_date': '10月20日',
                'thumbnail': 'https://example.com/test1.jpg',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'テスト映画2',
                'url': 'https://eiga.com/movie/test2/',
                'release_date': '10月21日',
                'thumbnail': 'https://example.com/test2.jpg',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        print("   サンプル映画情報で通知をテストします...")
        success = notifier.send_weekly_new_movies_notification(sample_movies)
        print(f"   通知結果: {'成功' if success else '失敗'}")
        
    except Exception as e:
        print(f"エラー: テストの実行に失敗しました - {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_weekly_new_movies()
    else:
        main()
