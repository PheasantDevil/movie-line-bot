"""データの永続化を管理するモジュール"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class MovieStorage:
    """映画情報を保存・読み込みするクラス"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "movies.json"
        
        # dataディレクトリが存在しない場合は作成
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_movies(self, movies: List[Dict]) -> bool:
        """
        映画情報をJSONファイルに保存
        
        Args:
            movies: 映画情報のリスト
            
        Returns:
            bool: 保存が成功したかどうか
        """
        try:
            data = {
                'updated_at': datetime.now().isoformat(),
                'count': len(movies),
                'movies': movies
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ {len(movies)}件の映画情報を保存しました: {self.data_file}")
            return True
            
        except Exception as e:
            print(f"エラー: データの保存に失敗しました - {e}")
            return False
    
    def load_movies(self) -> Optional[Dict]:
        """
        JSONファイルから映画情報を読み込み
        
        Returns:
            Dict: 映画情報（updated_at, count, moviesを含む）。ファイルが存在しない場合はNone
        """
        if not self.data_file.exists():
            print(f"ℹ️  前回のデータファイルが見つかりません: {self.data_file}")
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated_at = data.get('updated_at', '不明')
            count = data.get('count', 0)
            print(f"✓ 前回のデータを読み込みました: {count}件（最終更新: {updated_at}）")
            
            return data
            
        except Exception as e:
            print(f"エラー: データの読み込みに失敗しました - {e}")
            return None
    
    def get_movie_titles(self, data: Optional[Dict] = None) -> set:
        """
        映画タイトルのセットを取得（差分検知用）
        
        Args:
            data: 映画データ。Noneの場合は保存されているデータを読み込む
            
        Returns:
            set: 映画タイトルのセット
        """
        if data is None:
            data = self.load_movies()
        
        if data is None or 'movies' not in data:
            return set()
        
        return {movie['title'] for movie in data['movies']}


def test_storage():
    """ストレージのテスト"""
    print("データ永続化機能のテスト...\n")
    
    storage = MovieStorage()
    
    # テストデータ
    test_movies = [
        {
            'title': 'テスト映画1',
            'url': 'https://eiga.com/movie/12345/',
            'release_date': '10月10日',
            'thumbnail': 'https://example.com/image1.jpg',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'title': 'テスト映画2',
            'url': 'https://eiga.com/movie/12346/',
            'release_date': '10月11日',
            'thumbnail': 'https://example.com/image2.jpg',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    # 保存テスト
    print("1. 保存テスト")
    storage.save_movies(test_movies)
    print()
    
    # 読み込みテスト
    print("2. 読み込みテスト")
    loaded_data = storage.load_movies()
    if loaded_data:
        print(f"読み込んだ映画数: {loaded_data['count']}")
        print(f"最初の映画: {loaded_data['movies'][0]['title']}")
    print()
    
    # タイトル取得テスト
    print("3. タイトルセット取得テスト")
    titles = storage.get_movie_titles()
    print(f"タイトルセット: {titles}")
    print()


if __name__ == "__main__":
    test_storage()

