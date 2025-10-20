"""Webhook URLの接続テストスクリプト"""

import requests


def test_webhook_url():
    """Webhook URLにアクセスして接続テスト"""
    
    # Render.comのWebhook URL
    webhook_url = "https://movie-line-bot-webhook.onrender.com/webhook"
    root_url = "https://movie-line-bot-webhook.onrender.com/"
    
    print("=" * 60)
    print("Webhook URL 接続テスト")
    print("=" * 60)
    print()
    
    # 1. ルートパスのテスト
    print("--- ルートパス (/) のテスト ---")
    try:
        response = requests.get(root_url, timeout=10)
        print(f"✓ ステータスコード: {response.status_code}")
        print(f"✓ レスポンス: {response.text}")
        print()
    except Exception as e:
        print(f"❌ エラー: {e}")
        print()
    
    # 2. Webhook エンドポイントのテスト (GET)
    print("--- Webhook エンドポイント (/webhook) のテスト (GET) ---")
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")
        print("注: GETは405エラーが正常（POSTのみ受け付け）")
        print()
    except Exception as e:
        print(f"エラー: {e}")
        print()
    
    # 3. Webhook エンドポイントのテスト (POST - ダミーデータ)
    print("--- Webhook エンドポイント (/webhook) のテスト (POST) ---")
    try:
        # ダミーのLINE Webhookデータ
        dummy_data = {
            "events": []
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": "dummy_signature_for_test"
        }
        
        response = requests.post(
            webhook_url,
            json=dummy_data,
            headers=headers,
            timeout=10
        )
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")
        
        if response.status_code == 200:
            print("✓ Webhook エンドポイントは正常に動作しています")
        else:
            print("⚠️  エラーが発生しましたが、エンドポイントは存在します")
        print()
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        print()
    
    print("=" * 60)
    print("テスト完了")
    print("=" * 60)
    print()
    print("次のステップ:")
    print("1. ルートパスが200を返していることを確認")
    print("2. LINE Developers コンソールで Webhook URL を設定:")
    print(f"   {webhook_url}")
    print("3. 「検証」ボタンをクリックして接続テスト")
    print()


if __name__ == "__main__":
    test_webhook_url()

