"""新着映画を検知するモジュール"""

from typing import Dict, List, Tuple


class MovieDiffDetector:
    """映画情報の差分を検出するクラス"""
    
    @staticmethod
    def detect_new_movies(
        current_movies: List[Dict],
        previous_movies: List[Dict]
    ) -> Tuple[List[Dict], List[str]]:
        """
        新着映画を検出
        
        Args:
            current_movies: 現在の映画リスト
            previous_movies: 前回の映画リスト
            
        Returns:
            Tuple[List[Dict], List[str]]: (新着映画リスト, 新着映画タイトルリスト)
        """
        # 前回の映画タイトルセットを作成
        previous_titles = {movie['title'] for movie in previous_movies}
        
        # 新着映画を検出
        new_movies = []
        new_titles = []
        
        for movie in current_movies:
            if movie['title'] not in previous_titles:
                new_movies.append(movie)
                new_titles.append(movie['title'])
        
        return new_movies, new_titles
    
    @staticmethod
    def format_summary(
        current_count: int,
        previous_count: int,
        new_count: int
    ) -> str:
        """
        差分検知結果のサマリーを整形
        
        Args:
            current_count: 現在の映画数
            previous_count: 前回の映画数
            new_count: 新着映画数
            
        Returns:
            str: サマリー文字列
        """
        summary = f"""
=== 映画情報チェック結果 ===
現在の公開予定映画: {current_count}件
前回の公開予定映画: {previous_count}件
新着映画: {new_count}件
========================
"""
        return summary.strip()


def test_diff_detector():
    """差分検知のテスト"""
    print("差分検知機能のテスト...\n")
    
    # テストデータ
    previous_movies = [
        {'title': '映画A', 'url': 'https://eiga.com/movie/1/', 'release_date': '10月1日'},
        {'title': '映画B', 'url': 'https://eiga.com/movie/2/', 'release_date': '10月2日'},
        {'title': '映画C', 'url': 'https://eiga.com/movie/3/', 'release_date': '10月3日'},
    ]
    
    current_movies = [
        {'title': '映画B', 'url': 'https://eiga.com/movie/2/', 'release_date': '10月2日'},
        {'title': '映画C', 'url': 'https://eiga.com/movie/3/', 'release_date': '10月3日'},
        {'title': '映画D', 'url': 'https://eiga.com/movie/4/', 'release_date': '10月4日'},  # 新着
        {'title': '映画E', 'url': 'https://eiga.com/movie/5/', 'release_date': '10月5日'},  # 新着
    ]
    
    detector = MovieDiffDetector()
    
    # 差分検知
    new_movies, new_titles = detector.detect_new_movies(current_movies, previous_movies)
    
    # サマリー表示
    summary = detector.format_summary(
        len(current_movies),
        len(previous_movies),
        len(new_movies)
    )
    print(summary)
    print()
    
    # 新着映画の詳細
    if new_movies:
        print("新着映画の詳細:")
        for i, movie in enumerate(new_movies, 1):
            print(f"{i}. {movie['title']} ({movie['release_date']})")
            print(f"   URL: {movie['url']}")
    else:
        print("新着映画はありません")
    print()


if __name__ == "__main__":
    test_diff_detector()

