"""映画情報をスクレイピングするモジュール"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from datetime import datetime


class MovieScraper:
    """映画.comから映画情報を取得するクラス"""
    
    BASE_URL = "https://eiga.com"
    # 複数のURLパターンを試す
    POSSIBLE_URLS = [
        f"{BASE_URL}/now/",
        f"{BASE_URL}/soon/",
        f"{BASE_URL}/movie/",
        f"{BASE_URL}/ranking/",
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def fetch_upcoming_movies(self) -> List[Dict]:
        """
        今週公開の映画情報を取得
        
        Returns:
            List[Dict]: 映画情報のリスト
        """
        url = f"{self.BASE_URL}/movie/"
        
        try:
            print(f"映画情報を取得中: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            movies = self._parse_this_week_movies(soup)
            
            print(f"✓ {len(movies)}件の映画情報を取得しました")
            return movies
            
        except requests.RequestException as e:
            print(f"エラー: 映画情報の取得に失敗しました - {e}")
            return []
    
    def _parse_this_week_movies(self, soup: BeautifulSoup) -> List[Dict]:
        """
        「今週公開の映画」セクションから映画情報をパース
        
        Args:
            soup: BeautifulSoupオブジェクト
            
        Returns:
            List[Dict]: パースされた映画情報
        """
        movies = []
        
        # 「今週公開の映画」セクションを探す
        this_week_header = soup.find('h2', class_=['title-xlarge', 'margin-top20'])
        
        if not this_week_header:
            print("警告: 「今週公開の映画」セクションが見つかりません")
            return movies
        
        # 次の<ul>要素を取得
        movie_list = this_week_header.find_next('ul', class_='slide-menu')
        
        if not movie_list:
            print("警告: 映画リストが見つかりません")
            return movies
        
        # 各<li>要素から映画情報を抽出
        for li in movie_list.find_all('li'):
            try:
                movie_data = self._extract_movie_from_li(li)
                if movie_data:
                    movies.append(movie_data)
            except Exception as e:
                print(f"警告: 映画情報のパースに失敗しました - {e}")
                continue
        
        return movies
    
    def _extract_movie_from_li(self, li) -> Optional[Dict]:
        """
        <li>要素から映画データを抽出
        
        Args:
            li: BeautifulSoupの<li>要素
            
        Returns:
            Dict: 映画データ
        """
        try:
            # リンクとタイトル
            link = li.find('a', href=lambda h: h and '/movie/' in h)
            if not link:
                return None
            
            movie_url = self.BASE_URL + link['href']
            
            # タイトル（imgのalt属性から取得）
            img = link.find('img')
            if not img or not img.get('alt'):
                return None
            
            title = img['alt']
            thumbnail = img.get('src', '')
            
            # 公開日
            published_elem = li.find('p', class_='published')
            release_date = published_elem.get_text(strip=True) if published_elem else "未定"
            
            # 基本情報を取得
            movie_data = {
                'title': title,
                'url': movie_url,
                'release_date': release_date,
                'thumbnail': thumbnail,
                'scraped_at': datetime.now().isoformat()
            }
            
            return movie_data
            
        except Exception as e:
            print(f"データ抽出エラー: {e}")
            return None
    


def test_scraper():
    """スクレイパーのテスト"""
    print("映画情報のスクレイピングを開始します...")
    scraper = MovieScraper()
    movies = scraper.fetch_upcoming_movies()
    
    print(f"\n取得した映画数: {len(movies)}\n")
    
    # 最初の5件を表示
    for i, movie in enumerate(movies[:5], 1):
        print(f"--- 映画 {i} ---")
        print(f"タイトル: {movie['title']}")
        print(f"公開日: {movie['release_date']}")
        print(f"URL: {movie['url']}")
        print(f"サムネイル: {movie['thumbnail'][:60]}...")
        print()


if __name__ == "__main__":
    test_scraper()

