"""リッチメニュー管理システム"""

import os
from typing import Dict, List, Optional

import requests


class RichMenuManager:
    """リッチメニュー管理クラス"""
    
    def __init__(self, channel_access_token: Optional[str] = None):
        """
        初期化
        
        Args:
            channel_access_token: LINEチャネルアクセストークン
        """
        self.channel_access_token = channel_access_token or os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.api_base_url = 'https://api.line.me/v2/bot'
        self.api_data_url = 'https://api-data.line.me/v2/bot'
        
        if not self.channel_access_token:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
    
    def _get_headers(self) -> Dict[str, str]:
        """APIリクエスト用のヘッダーを取得"""
        return {
            'Authorization': f'Bearer {self.channel_access_token}',
            'Content-Type': 'application/json'
        }
    
    def _get_image_headers(self) -> Dict[str, str]:
        """画像アップロード用のヘッダーを取得"""
        return {
            'Authorization': f'Bearer {self.channel_access_token}',
            'Content-Type': 'image/png'
        }
    
    def create_movie_search_menu(self) -> str:
        """
        映画検索用リッチメニューを作成
        
        Returns:
            str: 作成されたリッチメニューのID
        """
        menu_data = {
            'size': {
                'width': 2500,
                'height': 1686
            },
            'selected': True,
            'name': '映画Bot メインメニュー',
            'chatBarText': 'メニュー',
            'areas': [
                # 映画検索ボタン（左上）
                {
                    'bounds': {
                        'x': 0,
                        'y': 0,
                        'width': 1250,
                        'height': 843
                    },
                    'action': {
                        'type': 'postback',
                        'data': 'action=movie_search',
                        'displayText': '映画検索'
                    }
                },
                # 映画館検索ボタン（右上）
                {
                    'bounds': {
                        'x': 1250,
                        'y': 0,
                        'width': 1250,
                        'height': 843
                    },
                    'action': {
                        'type': 'postback',
                        'data': 'action=theater_search',
                        'displayText': '映画館検索'
                    }
                },
                # 今週公開ボタン（左下）
                {
                    'bounds': {
                        'x': 0,
                        'y': 843,
                        'width': 1250,
                        'height': 843
                    },
                    'action': {
                        'type': 'postback',
                        'data': 'action=weekly_new',
                        'displayText': '今週公開'
                    }
                },
                # 上映中ボタン（右下）
                {
                    'bounds': {
                        'x': 1250,
                        'y': 843,
                        'width': 1250,
                        'height': 843
                    },
                    'action': {
                        'type': 'postback',
                        'data': 'action=now_showing',
                        'displayText': '上映中'
                    }
                }
            ]
        }
        
        try:
            url = f'{self.api_base_url}/richmenu'
            response = requests.post(url, headers=self._get_headers(), json=menu_data)
            response.raise_for_status()
            
            menu_id = response.json()['richMenuId']
            print(f"✓ リッチメニューを作成しました: {menu_id}")
            return menu_id
            
        except requests.RequestException as e:
            print(f"エラー: リッチメニューの作成に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            raise
    
    def upload_menu_image(self, menu_id: str, image_path: str) -> bool:
        """
        リッチメニュー画像をアップロード
        
        Args:
            menu_id: リッチメニューID
            image_path: 画像ファイルのパス
            
        Returns:
            bool: アップロードが成功したかどうか
        """
        if not os.path.exists(image_path):
            print(f"エラー: 画像ファイルが見つかりません: {image_path}")
            return False
        
        try:
            url = f'{self.api_data_url}/richmenu/{menu_id}/content'
            
            with open(image_path, 'rb') as f:
                response = requests.post(url, headers=self._get_image_headers(), data=f)
                response.raise_for_status()
            
            print(f"✓ リッチメニュー画像をアップロードしました: {image_path}")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: 画像のアップロードに失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def set_default_menu(self, menu_id: str) -> bool:
        """
        デフォルトリッチメニューに設定
        
        Args:
            menu_id: リッチメニューID
            
        Returns:
            bool: 設定が成功したかどうか
        """
        try:
            url = f'{self.api_base_url}/user/all/richmenu/{menu_id}'
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            
            print(f"✓ デフォルトリッチメニューに設定しました: {menu_id}")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: デフォルトメニューの設定に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def link_menu_to_user(self, user_id: str, menu_id: str) -> bool:
        """
        特定のユーザーにリッチメニューを紐付け
        
        Args:
            user_id: ユーザーID
            menu_id: リッチメニューID
            
        Returns:
            bool: 紐付けが成功したかどうか
        """
        try:
            url = f'{self.api_base_url}/user/{user_id}/richmenu/{menu_id}'
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            
            print(f"✓ ユーザー {user_id} にリッチメニューを紐付けました: {menu_id}")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: ユーザーへの紐付けに失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def unlink_menu_from_user(self, user_id: str) -> bool:
        """
        ユーザーからリッチメニューを解除
        
        Args:
            user_id: ユーザーID
            
        Returns:
            bool: 解除が成功したかどうか
        """
        try:
            url = f'{self.api_base_url}/user/{user_id}/richmenu'
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            
            print(f"✓ ユーザー {user_id} からリッチメニューを解除しました")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: リッチメニューの解除に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def get_menu_list(self) -> List[Dict]:
        """
        リッチメニュー一覧を取得
        
        Returns:
            List[Dict]: リッチメニュー一覧
        """
        try:
            url = f'{self.api_base_url}/richmenu/list'
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            menus = response.json()['richmenus']
            print(f"✓ {len(menus)}個のリッチメニューを取得しました")
            return menus
            
        except requests.RequestException as e:
            print(f"エラー: リッチメニュー一覧の取得に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return []
    
    def get_menu_info(self, menu_id: str) -> Optional[Dict]:
        """
        リッチメニューの詳細情報を取得
        
        Args:
            menu_id: リッチメニューID
            
        Returns:
            Dict: リッチメニュー情報、取得できない場合はNone
        """
        try:
            url = f'{self.api_base_url}/richmenu/{menu_id}'
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            menu_info = response.json()
            print(f"✓ リッチメニュー情報を取得しました: {menu_id}")
            return menu_info
            
        except requests.RequestException as e:
            print(f"エラー: リッチメニュー情報の取得に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return None
    
    def delete_menu(self, menu_id: str) -> bool:
        """
        リッチメニューを削除
        
        Args:
            menu_id: リッチメニューID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            url = f'{self.api_base_url}/richmenu/{menu_id}'
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            
            print(f"✓ リッチメニューを削除しました: {menu_id}")
            return True
            
        except requests.RequestException as e:
            print(f"エラー: リッチメニューの削除に失敗しました - {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス: {e.response.text}")
            return False
    
    def setup_complete_menu(self, image_path: str) -> Optional[str]:
        """
        完全なリッチメニューセットアップ（作成→画像アップロード→デフォルト設定）
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            str: 作成されたリッチメニューID、失敗した場合はNone
        """
        try:
            # 1. リッチメニューを作成
            menu_id = self.create_movie_search_menu()
            
            # 2. 画像をアップロード
            if not self.upload_menu_image(menu_id, image_path):
                print("画像のアップロードに失敗しました")
                return None
            
            # 3. デフォルトメニューに設定
            if not self.set_default_menu(menu_id):
                print("デフォルトメニューの設定に失敗しました")
                return None
            
            print(f"✓ リッチメニューの完全セットアップが完了しました: {menu_id}")
            return menu_id
            
        except Exception as e:
            print(f"エラー: リッチメニューのセットアップに失敗しました - {e}")
            return None


def test_rich_menu_manager():
    """リッチメニュー管理のテスト"""
    print("リッチメニュー管理システムのテスト...\n")
    
    # 環境変数の確認
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("⚠️  LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
        print("環境変数を設定してからテストを実行してください")
        return
    
    try:
        # リッチメニューマネージャーを初期化
        manager = RichMenuManager()
        
        print("1. リッチメニュー一覧の取得テスト")
        menus = manager.get_menu_list()
        print(f"   既存のリッチメニュー数: {len(menus)}")
        
        print("\n2. リッチメニューの作成テスト")
        menu_id = manager.create_movie_search_menu()
        print(f"   作成されたメニューID: {menu_id}")
        
        print("\n3. リッチメニュー情報の取得テスト")
        menu_info = manager.get_menu_info(menu_id)
        if menu_info:
            print(f"   メニュー名: {menu_info.get('name', 'N/A')}")
            print(f"   メニューサイズ: {menu_info.get('size', {})}")
            print(f"   エリア数: {len(menu_info.get('areas', []))}")
        
        print("\n4. テスト用リッチメニューの削除")
        success = manager.delete_menu(menu_id)
        print(f"   削除: {'成功' if success else '失敗'}")
        
        print("\n✓ リッチメニュー管理システムのテストが完了しました")
        
    except Exception as e:
        print(f"エラー: テストの実行に失敗しました - {e}")


if __name__ == "__main__":
    test_rich_menu_manager()
