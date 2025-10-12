"""映画情報収集とLINE通知のメインスクリプト"""

import sys
import os
from scraper import MovieScraper
from storage import MovieStorage
from diff_detector import MovieDiffDetector
from line_notifier import LineNotifier


def main():
    """メイン処理"""
    print("=" * 60)
    print("映画情報通知 LINE Bot - 実行開始")
    print("=" * 60)
    print()
    
    # 1. 前回のデータを読み込み
    storage = MovieStorage()
    previous_data = storage.load_movies()
    previous_movies = previous_data['movies'] if previous_data else []
    print()
    
    # 2. 最新の映画情報を取得
    print("--- 映画情報の取得 ---")
    scraper = MovieScraper()
    current_movies = scraper.fetch_upcoming_movies()
    print()
    
    if not current_movies:
        print("エラー: 映画情報の取得に失敗しました")
        sys.exit(1)
    
    # 3. 差分検知
    print("--- 差分検知 ---")
    detector = MovieDiffDetector()
    new_movies, new_titles = detector.detect_new_movies(
        current_movies,
        previous_movies
    )
    
    summary = detector.format_summary(
        len(current_movies),
        len(previous_movies),
        len(new_movies)
    )
    print(summary)
    print()
    
    # 4. 新着映画の表示とLINE通知
    if new_movies:
        print(f"🎬 新着映画が {len(new_movies)}件 見つかりました！")
        print()
        for i, movie in enumerate(new_movies, 1):
            print(f"【{i}】 {movie['title']}")
            print(f"     公開日: {movie['release_date']}")
            print(f"     URL: {movie['url']}")
            print()
        
        # LINE通知を送信
        print("--- LINE通知 ---")
        if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') and os.getenv('LINE_USER_ID'):
            try:
                notifier = LineNotifier()
                success = notifier.send_movie_notifications(new_movies)
                if success:
                    print("✓ LINE通知を送信しました")
                else:
                    print("⚠️  LINE通知の送信に失敗しました")
            except Exception as e:
                print(f"エラー: LINE通知でエラーが発生しました - {e}")
        else:
            print("ℹ️  LINE通知は環境変数が設定されていないためスキップされました")
            print("   環境変数を設定すると、新着映画をLINEで受け取ることができます")
        print()
    else:
        print("ℹ️  新着映画はありません")
        print()
    
    # 5. データを保存
    print("--- データの保存 ---")
    storage.save_movies(current_movies)
    print()
    
    print("=" * 60)
    print("処理が完了しました")
    print("=" * 60)


if __name__ == "__main__":
    main()

