"""映画館検索機能"""

import urllib.parse
from typing import Dict, List, Optional


class TheaterSearchManager:
    """映画館検索管理クラス"""
    
    def __init__(self):
        """初期化"""
        self.google_search_base = "https://www.google.com/search"
        self.google_maps_base = "https://www.google.com/maps/search"
        
        # 検索クエリのテンプレート
        self.search_templates = {
            'general': '{theater_name} 映画館',
            'location': '{theater_name} 映画館 {location}',
            'movie': '{theater_name} 映画館 上映スケジュール',
            'maps': '{theater_name} 映画館 地図'
        }
    
    def generate_google_search_url(
        self,
        theater_name: str,
        search_type: str = 'general',
        location: Optional[str] = None
    ) -> str:
        """
        Google検索URLを生成
        
        Args:
            theater_name: 映画館名
            search_type: 検索タイプ（'general', 'location', 'movie', 'maps'）
            location: 場所（locationタイプの場合）
            
        Returns:
            str: Google検索URL
        """
        # 検索クエリを生成
        if search_type == 'location' and location:
            query = self.search_templates['location'].format(
                theater_name=theater_name,
                location=location
            )
        else:
            query = self.search_templates.get(search_type, self.search_templates['general']).format(
                theater_name=theater_name
            )
        
        # URLエンコード
        encoded_query = urllib.parse.quote(query)
        
        # 検索URLを生成
        if search_type == 'maps':
            search_url = f"{self.google_maps_base}?q={encoded_query}"
        else:
            search_url = f"{self.google_search_base}?q={encoded_query}"
        
        return search_url
    
    def create_search_button_message(
        self,
        theater_name: str,
        search_type: str = 'general',
        location: Optional[str] = None
    ) -> Dict:
        """
        検索ボタン付きメッセージを作成
        
        Args:
            theater_name: 映画館名
            search_type: 検索タイプ
            location: 場所
            
        Returns:
            Dict: LINEメッセージオブジェクト
        """
        search_url = self.generate_google_search_url(theater_name, search_type, location)
        
        # ボタンテンプレートメッセージを作成
        message = {
            'type': 'template',
            'altText': f'{theater_name}の検索結果',
            'template': {
                'type': 'buttons',
                'text': f'「{theater_name}」の検索結果を表示します',
                'actions': [
                    {
                        'type': 'uri',
                        'label': '🔍 検索結果を見る',
                        'uri': search_url
                    }
                ]
            }
        }
        
        return message
    
    def create_multiple_search_options(
        self,
        theater_name: str,
        location: Optional[str] = None
    ) -> Dict:
        """
        複数の検索オプション付きメッセージを作成
        
        Args:
            theater_name: 映画館名
            location: 場所
            
        Returns:
            Dict: LINEメッセージオブジェクト
        """
        # 各検索タイプのURLを生成
        general_url = self.generate_google_search_url(theater_name, 'general', location)
        movie_url = self.generate_google_search_url(theater_name, 'movie', location)
        maps_url = self.generate_google_search_url(theater_name, 'maps', location)
        
        # カルーセルテンプレートメッセージを作成
        message = {
            'type': 'template',
            'altText': f'{theater_name}の検索オプション',
            'template': {
                'type': 'carousel',
                'columns': [
                    {
                        'title': '🔍 一般検索',
                        'text': f'「{theater_name}」の基本情報を検索',
                        'actions': [
                            {
                                'type': 'uri',
                                'label': '検索する',
                                'uri': general_url
                            }
                        ]
                    },
                    {
                        'title': '🎬 上映スケジュール',
                        'text': f'「{theater_name}」の上映スケジュールを検索',
                        'actions': [
                            {
                                'type': 'uri',
                                'label': '検索する',
                                'uri': movie_url
                            }
                        ]
                    },
                    {
                        'title': '📍 地図・場所',
                        'text': f'「{theater_name}」の場所を地図で確認',
                        'actions': [
                            {
                                'type': 'uri',
                                'label': '地図を見る',
                                'uri': maps_url
                            }
                        ]
                    }
                ]
            }
        }
        
        return message
    
    def create_quick_search_message(
        self,
        theater_name: str,
        location: Optional[str] = None
    ) -> Dict:
        """
        クイック検索メッセージを作成（シンプル版）
        
        Args:
            theater_name: 映画館名
            location: 場所
            
        Returns:
            Dict: LINEメッセージオブジェクト
        """
        search_url = self.generate_google_search_url(theater_name, 'general', location)
        
        # シンプルなテキストメッセージ + Quick Reply
        message = {
            'type': 'text',
            'text': f'「{theater_name}」の検索結果を表示します',
            'quickReply': {
                'items': [
                    {
                        'type': 'action',
                        'action': {
                            'type': 'uri',
                            'label': '🔍 検索結果を見る',
                            'uri': search_url
                        }
                    },
                    {
                        'type': 'action',
                        'action': {
                            'type': 'uri',
                            'label': '📍 地図で確認',
                            'uri': self.generate_google_search_url(theater_name, 'maps', location)
                        }
                    }
                ]
            }
        }
        
        return message
    
    def validate_theater_name(self, theater_name: str) -> bool:
        """
        映画館名の妥当性をチェック
        
        Args:
            theater_name: 映画館名
            
        Returns:
            bool: 妥当な場合True
        """
        if not theater_name or not theater_name.strip():
            return False
        
        # 最小文字数チェック
        if len(theater_name.strip()) < 2:
            return False
        
        # 最大文字数チェック（Google検索の制限を考慮）
        if len(theater_name.strip()) > 100:
            return False
        
        return True
    
    def suggest_search_terms(self, partial_name: str) -> List[str]:
        """
        部分的な映画館名から検索候補を提案
        
        Args:
            partial_name: 部分的な映画館名
            
        Returns:
            List[str]: 検索候補のリスト
        """
        if not partial_name or len(partial_name.strip()) < 2:
            return []
        
        # 一般的な映画館チェーンの候補
        common_chains = [
            'TOHOシネマズ',
            'イオンシネマ',
            'ユナイテッド・シネマ',
            'MOVIX',
            'シネマサンシャイン',
            '109シネマズ',
            'ワーナー・マイカル・シネマズ',
            '角川シネマ',
            '新宿ピカデリー',
            '渋谷シネマ',
            '有楽町スバル座',
            '丸の内TOEI'
        ]
        
        # 部分一致する候補をフィルタリング
        suggestions = []
        partial_lower = partial_name.lower()
        
        for chain in common_chains:
            if partial_lower in chain.lower():
                suggestions.append(chain)
        
        # 最大5件まで返す
        return suggestions[:5]
    
    def extract_location_from_query(self, query: str) -> Optional[str]:
        """
        クエリから場所情報を抽出
        
        Args:
            query: 検索クエリ
            
        Returns:
            str: 抽出された場所、見つからない場合はNone
        """
        # 一般的な都道府県名
        prefectures = [
            '北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島',
            '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川',
            '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜',
            '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫',
            '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口',
            '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎',
            '熊本', '大分', '宮崎', '鹿児島', '沖縄'
        ]
        
        # 主要都市名
        cities = [
            '札幌', '仙台', 'さいたま', '千葉', '横浜', '川崎', '相模原',
            '新潟', '静岡', '浜松', '名古屋', '豊田', '津', '大津',
            '京都', '大阪', '堺', '神戸', '姫路', '奈良', '和歌山',
            '鳥取', '松江', '岡山', '広島', '山口', '徳島', '高松',
            '松山', '高知', '福岡', '北九州', '熊本', '大分', '宮崎',
            '鹿児島', '那覇'
        ]
        
        # 区名（東京23区）
        tokyo_wards = [
            '千代田', '中央', '港', '新宿', '文京', '台東', '墨田',
            '江東', '品川', '目黒', '大田', '世田谷', '渋谷', '中野',
            '杉並', '豊島', '北', '荒川', '板橋', '練馬', '足立',
            '葛飾', '江戸川'
        ]
        
        all_locations = prefectures + cities + tokyo_wards
        
        for location in all_locations:
            if location in query:
                return location
        
        return None


def test_theater_search_manager():
    """映画館検索管理のテスト"""
    print("映画館検索管理システムのテスト...\n")
    
    # 映画館検索マネージャーを初期化
    manager = TheaterSearchManager()
    
    print("1. Google検索URL生成テスト")
    test_theaters = [
        "TOHOシネマズ渋谷",
        "イオンシネマ",
        "新宿ピカデリー"
    ]
    
    for theater in test_theaters:
        url = manager.generate_google_search_url(theater)
        print(f"   {theater}: {url}")
    
    print("\n2. 検索ボタン付きメッセージ作成テスト")
    message = manager.create_search_button_message("TOHOシネマズ渋谷")
    print(f"   メッセージタイプ: {message['type']}")
    print(f"   テンプレートタイプ: {message['template']['type']}")
    
    print("\n3. 複数検索オプション作成テスト")
    multi_message = manager.create_multiple_search_options("イオンシネマ", "東京")
    print(f"   カルーセルカラム数: {len(multi_message['template']['columns'])}")
    
    print("\n4. 映画館名妥当性チェックテスト")
    test_names = [
        "TOHOシネマズ",  # 妥当
        "A",             # 短すぎる
        "",              # 空
        "X" * 150,       # 長すぎる
        "   ",           # 空白のみ
    ]
    
    for name in test_names:
        is_valid = manager.validate_theater_name(name)
        print(f"   '{name[:20]}...': {'妥当' if is_valid else '不正'}")
    
    print("\n5. 検索候補提案テスト")
    partial_queries = ["TOHO", "イオン", "シネマ", "新宿"]
    
    for query in partial_queries:
        suggestions = manager.suggest_search_terms(query)
        print(f"   '{query}': {suggestions}")
    
    print("\n6. 場所抽出テスト")
    test_queries = [
        "TOHOシネマズ渋谷",
        "イオンシネマ大阪",
        "新宿ピカデリー",
        "映画館",
        "TOHOシネマズ東京都渋谷区"
    ]
    
    for query in test_queries:
        location = manager.extract_location_from_query(query)
        print(f"   '{query}': {location if location else '場所なし'}")
    
    print("\n✓ 映画館検索管理システムのテストが完了しました")


if __name__ == "__main__":
    test_theater_search_manager()
