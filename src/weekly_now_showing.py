"""上映中映画の週次通知スクリプト"""

import os
import sys
from datetime import datetime

from line_notifier import LineNotifier
from scraper import MovieScraper


def main():
    """上映中映画の週次通知メイン処理"""
    print("=" * 60)
    print("上映中映画 週次通知 - 実行開始")
    print("=" * 60)
    print()
    
    # 1. スクレイパーを初期化
    scraper = MovieScraper()
    
    # 2. 上映中の映画を取得（過去1週間以内に公開された映画）
    print("--- 上映中映画の取得 ---")
    movies = scraper.fetch_movies_released_in_past_week()
    print(f"取得件数: {len(movies)}件")
    print()
    
    # 3. 映画がない場合でも通知を送信（情報提供として）
    if not movies:
        print("ℹ️  上映中の映画が見つかりませんでした")
        print("   空の通知を送信します")
    
    # 4. 通知を送信
    print("--- LINE通知 ---")
    if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') and os.getenv('LINE_USER_ID'):
        try:
            notifier = LineNotifier()
            success = notifier.send_weekly_now_showing_notification(movies)
            
            if success:
                print("✓ 上映中映画の通知を送信しました")
                print()
                if movies:
                    print("【上映中の映画】")
                    for i, movie in enumerate(movies[:10], 1):  # 最大10件まで表示
                        theater_info = ""
                        if movie.get('is_limited_release'):
                            theater_info = " ⚠️ 限定公開"
                        elif movie.get('theater_count'):
                            theater_info = f" ({movie['theater_count']}館)"
                        print(f"  {i}. {movie['title']} ({movie['release_date']}){theater_info}")
                    if len(movies) > 10:
                        print(f"  ...他 {len(movies) - 10}件")
                else:
                    print("  現在上映中の映画はありません")
                print()
            else:
                print("⚠️  上映中映画の通知送信に失敗しました")
                
        except Exception as e:
            print(f"エラー: 上映中映画の通知でエラーが発生しました - {e}")
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


def test_weekly_now_showing():
    """上映中映画通知のテスト"""
    print("上映中映画通知のテスト...\n")
    
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
        print("  python3 src/weekly_now_showing.py")
        return
    
    print("✓ 環境変数が設定されています")
    print(f"  TOKEN: {token[:20]}...")
    print(f"  USER_ID: {user_id}")
    print()
    
    try:
        # スクレイパーのテスト
        print("1. 上映中映画情報の取得テスト")
        scraper = MovieScraper()
        movies = scraper.fetch_movies_released_in_past_week()
        print(f"   取得件数: {len(movies)}件")
        
        if movies:
            print("   取得した映画（最初の3件）:")
            for i, movie in enumerate(movies[:3], 1):
                theater_info = ""
                if movie.get('is_limited_release'):
                    theater_info = " ⚠️ 限定公開"
                elif movie.get('theater_count'):
                    theater_info = f" ({movie['theater_count']}館)"
                print(f"     {i}. {movie['title']} ({movie['release_date']}){theater_info}")
        
        print("\n2. LINE通知のテスト")
        notifier = LineNotifier()
        
        # サンプル映画情報でテスト
        sample_movies = [
            {
                'title': 'テスト上映中映画1',
                'url': 'https://eiga.com/movie/showing1/',
                'release_date': '10月15日',
                'thumbnail': 'https://example.com/showing1.jpg',
                'scraped_at': datetime.now().isoformat(),
                'theater_count': 300,
                'is_limited_release': False
            },
            {
                'title': 'テスト上映中映画2',
                'url': 'https://eiga.com/movie/showing2/',
                'release_date': '10月16日',
                'thumbnail': 'https://example.com/showing2.jpg',
                'scraped_at': datetime.now().isoformat(),
                'theater_count': 25,
                'is_limited_release': True
            }
        ]
        
        print("   サンプル上映中映画情報で通知をテストします...")
        success = notifier.send_weekly_now_showing_notification(sample_movies)
        print(f"   通知結果: {'成功' if success else '失敗'}")
        
    except Exception as e:
        print(f"エラー: テストの実行に失敗しました - {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_weekly_now_showing()
    else:
        main()
