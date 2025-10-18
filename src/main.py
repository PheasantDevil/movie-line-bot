"""映画情報収集とLINE通知のメインスクリプト"""

import os
import sys

from line_notifier import LineNotifier
from scraper import MovieScraper
from storage import MovieStorage


def main():
    """メイン処理（週次通知）"""
    print("=" * 60)
    print("映画情報週次通知 LINE Bot - 実行開始")
    print("=" * 60)
    print()
    
    # 1. スクレイパーを初期化
    scraper = MovieScraper()
    
    # 2. 過去1週間以内に公開された映画を取得
    print("--- 過去1週間以内に公開された映画を取得 ---")
    past_week_movies = scraper.fetch_movies_released_in_past_week()
    print(f"取得件数: {len(past_week_movies)}件")
    print()
    
    # 3. 先1週間以内に公開予定の映画を取得
    print("--- 先1週間以内に公開予定の映画を取得 ---")
    next_week_movies = scraper.fetch_movies_coming_in_next_week()
    print(f"取得件数: {len(next_week_movies)}件")
    print()
    
    # 4. データを保存（検索用）
    print("--- データの保存 ---")
    storage = MovieStorage()
    
    # 過去と未来の映画を統合して保存
    all_movies = past_week_movies + next_week_movies
    storage.save_movies(all_movies)
    print()
    
    # 5. 週次通知を送信
    print("--- LINE通知 ---")
    if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') and os.getenv('LINE_USER_ID'):
        try:
            notifier = LineNotifier()
            success = notifier.send_weekly_notification(
                past_week_movies,
                next_week_movies
            )
            
            if success:
                print("✓ LINE週次通知を送信しました")
                print()
                print("【過去1週間の映画】")
                for i, movie in enumerate(past_week_movies[:5], 1):
                    print(f"  {i}. {movie['title']} ({movie['release_date']})")
                if len(past_week_movies) > 5:
                    print(f"  ...他 {len(past_week_movies) - 5}件")
                print()
                
                print("【先1週間の映画】")
                for i, movie in enumerate(next_week_movies[:5], 1):
                    theater_info = ""
                    if movie.get('is_limited_release'):
                        theater_info = " ⚠️ 限定公開"
                    elif movie.get('theater_count'):
                        theater_info = f" ({movie['theater_count']}館)"
                    print(f"  {i}. {movie['title']} ({movie['release_date']}){theater_info}")
                if len(next_week_movies) > 5:
                    print(f"  ...他 {len(next_week_movies) - 5}件")
                print()
            else:
                print("⚠️  LINE通知の送信に失敗しました")
                
        except Exception as e:
            print(f"エラー: LINE通知でエラーが発生しました - {e}")
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


if __name__ == "__main__":
    main()

