"""映画情報をスクレイピングするモジュール"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


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
    
    def fetch_movies_released_in_past_week(self) -> List[Dict]:
        """
        過去1週間以内に公開された映画情報を取得
        
        Returns:
            List[Dict]: 映画情報のリスト
        """
        url = f"{self.BASE_URL}/now/"
        
        try:
            print(f"公開中の映画情報を取得中: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            movies = self._parse_now_showing_movies(soup)
            
            # 過去1週間以内の映画のみにフィルタリング
            one_week_ago = datetime.now() - timedelta(days=7)
            recent_movies = []
            
            for movie in movies:
                release_date_str = movie.get('release_date', '')
                release_date = self._parse_release_date(release_date_str)
                
                if release_date and release_date >= one_week_ago:
                    recent_movies.append(movie)
            
            print(f"✓ {len(recent_movies)}件の過去1週間以内の映画情報を取得しました")
            return recent_movies
            
        except requests.RequestException as e:
            print(f"エラー: 公開中映画情報の取得に失敗しました - {e}")
            return []
    
    def fetch_movies_coming_in_next_week(self) -> List[Dict]:
        """
        先1週間以内に公開予定の映画情報を取得
        
        Returns:
            List[Dict]: 映画情報のリスト（上映館数情報も含む）
        """
        url = f"{self.BASE_URL}/soon/"
        
        try:
            print(f"公開予定の映画情報を取得中: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            movies = self._parse_coming_soon_movies(soup)
            
            # 先1週間以内の映画のみにフィルタリング
            one_week_later = datetime.now() + timedelta(days=7)
            upcoming_movies = []
            
            for movie in movies:
                release_date_str = movie.get('release_date', '')
                release_date = self._parse_release_date(release_date_str)
                
                if release_date and release_date <= one_week_later:
                    # 上映館数情報を取得
                    theater_count = self._fetch_theater_count(movie['url'])
                    movie['theater_count'] = theater_count
                    movie['is_limited_release'] = self._is_limited_release(theater_count)
                    upcoming_movies.append(movie)
            
            print(f"✓ {len(upcoming_movies)}件の先1週間以内の映画情報を取得しました")
            return upcoming_movies
            
        except requests.RequestException as e:
            print(f"エラー: 公開予定映画情報の取得に失敗しました - {e}")
            return []
    
    def search_movie_by_keyword(self, keyword: str) -> List[Dict]:
        """
        キーワードで映画を検索
        
        Args:
            keyword: 検索キーワード
            
        Returns:
            List[Dict]: マッチした映画情報のリスト
        """
        # 映画.comの検索機能を使用
        search_url = f"{self.BASE_URL}/search/"
        
        try:
            print(f"映画を検索中: {keyword}")
            response = self.session.get(
                search_url,
                params={'search': keyword},
                timeout=30
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            movies = self._parse_search_results(soup)
            
            print(f"✓ {len(movies)}件の検索結果を取得しました")
            return movies
            
        except requests.RequestException as e:
            print(f"エラー: 映画検索に失敗しました - {e}")
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
    
    def _parse_now_showing_movies(self, soup: BeautifulSoup) -> List[Dict]:
        """
        公開中の映画一覧ページから映画情報をパース
        
        Args:
            soup: BeautifulSoupオブジェクト
            
        Returns:
            List[Dict]: パースされた映画情報
        """
        movies = []
        
        # 方法1: 従来のパターン（ul.slide-menu）
        movie_list = soup.find('ul', class_='slide-menu')
        
        if movie_list:
            print("✓ slide-menuから映画情報を取得")
            # 各映画情報を抽出
            for li in movie_list.find_all('li'):
                try:
                    movie_data = self._extract_movie_from_li(li)
                    if movie_data:
                        movies.append(movie_data)
                except Exception as e:
                    print(f"警告: 映画情報のパースに失敗しました - {e}")
                    continue
        
        # 方法2: imgタグから直接取得（バックアッププラン）
        if not movies:
            print("代替方法: imgタグから映画情報を取得")
            imgs = soup.find_all('img', alt=True, limit=100)
            
            for img in imgs:
                # altがあり、親にリンクがある画像を探す
                if not img.get('alt') or len(img.get('alt')) < 2:
                    continue
                
                parent_link = img.find_parent('a')
                if not parent_link:
                    continue
                
                href = parent_link.get('href', '')
                if '/movie/' not in href:
                    continue
                
                # 基本情報を抽出
                movie_url = self.BASE_URL + href if href.startswith('/') else href
                title = img.get('alt')
                thumbnail = img.get('src', '')
                
                # 公開日を探す（親要素やコンテナから）
                release_date = "公開中"
                container = parent_link.find_parent('div') or parent_link.find_parent('li')
                
                if container:
                    # published, date などのクラスを持つ要素を探す
                    date_elem = container.find(['p', 'span', 'div'], 
                                              class_=lambda c: c and ('published' in str(c) or 'date' in str(c)))
                    if date_elem:
                        release_date = date_elem.get_text(strip=True)
                    else:
                        # テキストから日付を抽出
                        text = container.get_text()
                        import re
                        date_match = re.search(r'(\d{1,2}月\d{1,2}日)', text)
                        if date_match:
                            release_date = date_match.group(1)
                
                movie_data = {
                    'title': title,
                    'url': movie_url,
                    'release_date': release_date,
                    'thumbnail': thumbnail,
                    'scraped_at': datetime.now().isoformat()
                }
                
                # 重複チェック
                if not any(m['url'] == movie_url for m in movies):
                    movies.append(movie_data)
        
        if not movies:
            print("警告: 公開中映画が見つかりません")
        else:
            print(f"✓ {len(movies)}件の公開中映画を取得しました")
        
        return movies
    
    def _parse_coming_soon_movies(self, soup: BeautifulSoup) -> List[Dict]:
        """
        公開予定の映画一覧ページから映画情報をパース
        
        Args:
            soup: BeautifulSoupオブジェクト
            
        Returns:
            List[Dict]: パースされた映画情報
        """
        movies = []
        
        # 映画リストを探す
        movie_list = soup.find('ul', class_='slide-menu')
        
        if not movie_list:
            movie_list = soup.find('div', class_='movielist')
        
        if not movie_list:
            print("警告: 公開予定映画リストが見つかりません")
            return movies
        
        # 各映画情報を抽出
        for li in movie_list.find_all('li'):
            try:
                movie_data = self._extract_movie_from_li(li)
                if movie_data:
                    movies.append(movie_data)
            except Exception as e:
                print(f"警告: 映画情報のパースに失敗しました - {e}")
                continue
        
        return movies
    
    def _parse_search_results(self, soup: BeautifulSoup) -> List[Dict]:
        """
        検索結果ページから映画情報をパース
        
        Args:
            soup: BeautifulSoupオブジェクト
            
        Returns:
            List[Dict]: パースされた映画情報
        """
        movies = []
        
        # 検索結果から映画情報を抽出
        search_results = soup.find_all('div', class_='search-item')
        
        if not search_results:
            # 別のパターン
            search_results = soup.find_all('li', class_='movie-item')
        
        for item in search_results:
            try:
                link = item.find('a', href=lambda h: h and '/movie/' in h)
                if not link:
                    continue
                
                movie_url = self.BASE_URL + link['href'] if not link['href'].startswith('http') else link['href']
                
                # タイトル
                title_elem = item.find(['h3', 'h2', 'h4'])
                if not title_elem:
                    title_elem = link
                
                title = title_elem.get_text(strip=True)
                
                # サムネイル
                img = item.find('img')
                thumbnail = img.get('src', '') if img else ''
                
                # 公開日（あれば）
                date_elem = item.find('p', class_='published')
                release_date = date_elem.get_text(strip=True) if date_elem else "未定"
                
                movie_data = {
                    'title': title,
                    'url': movie_url,
                    'release_date': release_date,
                    'thumbnail': thumbnail,
                    'scraped_at': datetime.now().isoformat()
                }
                
                movies.append(movie_data)
                
            except Exception as e:
                print(f"警告: 検索結果のパースに失敗しました - {e}")
                continue
        
        return movies
    
    def _parse_release_date(self, date_str: str) -> Optional[datetime]:
        """
        公開日文字列をdatetimeオブジェクトに変換
        
        Args:
            date_str: 公開日文字列（例: "10月18日", "2025年10月18日"）
            
        Returns:
            datetime: 変換された日付、パースできない場合はNone
        """
        if not date_str or date_str == "未定":
            return None
        
        try:
            # パターン1: "10月18日"
            match = re.search(r'(\d{1,2})月(\d{1,2})日', date_str)
            if match:
                month = int(match.group(1))
                day = int(match.group(2))
                year = datetime.now().year
                
                # 月が現在の月より小さい場合は翌年とする
                if month < datetime.now().month:
                    year += 1
                
                return datetime(year, month, day)
            
            # パターン2: "2025年10月18日"
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                return datetime(year, month, day)
            
        except Exception as e:
            print(f"日付のパースに失敗: {date_str} - {e}")
        
        return None
    
    def _fetch_theater_count(self, movie_url: str) -> Optional[int]:
        """
        映画の上映館数を取得
        
        Args:
            movie_url: 映画の詳細ページURL
            
        Returns:
            int: 上映館数、取得できない場合はNone
        """
        try:
            response = self.session.get(movie_url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 上映館数の情報を探す
            # パターン1: "全国XX館で公開"
            text = soup.get_text()
            match = re.search(r'全国[約]?(\d+)館', text)
            if match:
                return int(match.group(1))
            
            # パターン2: "XX館"
            match = re.search(r'(\d+)館', text)
            if match:
                return int(match.group(1))
            
            # パターン3: 上映劇場リストから数える
            theater_list = soup.find('div', class_='theater-list')
            if theater_list:
                theaters = theater_list.find_all('li')
                if theaters:
                    return len(theaters)
            
        except Exception as e:
            print(f"上映館数の取得に失敗: {movie_url} - {e}")
        
        return None
    
    def _is_limited_release(self, theater_count: Optional[int]) -> bool:
        """
        上映館数が少ないかどうかを判定
        
        Args:
            theater_count: 上映館数
            
        Returns:
            bool: 限定公開の場合True（50館以下を限定公開とする）
        """
        if theater_count is None:
            return False
        
        return theater_count <= 50
    


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

