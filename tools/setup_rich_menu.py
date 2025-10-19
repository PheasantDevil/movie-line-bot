"""リッチメニュー設定スクリプト

リッチメニューを作成し、画像をアップロードして、デフォルトメニューに設定します。
"""

import os
import sys

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rich_menu_manager import RichMenuManager


def main():
    """メイン処理"""
    print("=" * 60)
    print("リッチメニュー設定")
    print("=" * 60)
    print()
    
    # 環境変数の確認
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("❌ エラー: LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
        print()
        print("環境変数を設定してください:")
        print("  export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
        print()
        return False
    
    print("✓ 環境変数が設定されています")
    print(f"  TOKEN: {token[:20]}...")
    print()
    
    # 画像ファイルの確認
    image_path = "assets/rich_menu.png"
    if not os.path.exists(image_path):
        print(f"❌ エラー: リッチメニュー画像が見つかりません: {image_path}")
        print()
        print("画像を生成してください:")
        print("  python tools/generate_rich_menu_image.py")
        print()
        return False
    
    print(f"✓ リッチメニュー画像が見つかりました: {image_path}")
    print()
    
    try:
        # リッチメニューマネージャーを初期化
        manager = RichMenuManager()
        
        # 既存のリッチメニュー一覧を取得
        print("--- 既存のリッチメニュー ---")
        existing_menus = manager.get_menu_list()
        
        if existing_menus:
            print(f"既存のリッチメニュー数: {len(existing_menus)}")
            for i, menu in enumerate(existing_menus, 1):
                print(f"  {i}. {menu.get('name', 'N/A')} (ID: {menu.get('richMenuId', 'N/A')})")
            
            # 削除確認
            print()
            response = input("既存のリッチメニューを削除しますか？ (y/N): ")
            if response.lower() == 'y':
                for menu in existing_menus:
                    menu_id = menu.get('richMenuId')
                    if menu_id:
                        print(f"  削除中: {menu_id}")
                        manager.delete_menu(menu_id)
                print("✓ 既存のリッチメニューを削除しました")
        else:
            print("既存のリッチメニューはありません")
        print()
        
        # 新しいリッチメニューを設定
        print("--- 新しいリッチメニューの設定 ---")
        menu_id = manager.setup_complete_menu(image_path)
        
        if menu_id:
            print()
            print("=" * 60)
            print("リッチメニューの設定が完了しました！")
            print("=" * 60)
            print()
            print(f"リッチメニューID: {menu_id}")
            print()
            print("次のステップ:")
            print("1. LINEアプリでBotのトーク画面を開く")
            print("2. 画面下部にリッチメニューが表示されることを確認")
            print("3. 各ボタンをタップして動作を確認")
            print()
            print("ボタン機能:")
            print("  🎬 映画検索：映画名を入力して検索")
            print("  🎪 映画館検索：映画館名を入力して検索")
            print("  📅 今週公開：今週公開予定の映画一覧")
            print("  🎭 上映中：現在上映中の映画一覧")
            print()
            return True
        else:
            print("❌ エラー: リッチメニューの設定に失敗しました")
            return False
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

