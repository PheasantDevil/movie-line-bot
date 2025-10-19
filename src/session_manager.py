"""ユーザーセッション管理システム"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path


class SessionManager:
    """ユーザーセッション管理クラス"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初期化
        
        Args:
            data_dir: セッションデータを保存するディレクトリ
        """
        self.data_dir = Path(data_dir)
        self.sessions_file = self.data_dir / "sessions.json"
        
        # dataディレクトリが存在しない場合は作成
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # セッションデータを読み込み
        self.sessions = self._load_sessions()
    
    def _load_sessions(self) -> Dict:
        """
        セッションデータを読み込み
        
        Returns:
            Dict: セッションデータ
        """
        if not self.sessions_file.exists():
            return {}
        
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 期限切れのセッションをクリーンアップ
            self._cleanup_expired_sessions(data)
            
            return data
            
        except Exception as e:
            print(f"セッションデータの読み込みエラー: {e}")
            return {}
    
    def _save_sessions(self) -> bool:
        """
        セッションデータを保存
        
        Returns:
            bool: 保存が成功したかどうか
        """
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, ensure_ascii=False, indent=2)
            return True
            
        except Exception as e:
            print(f"セッションデータの保存エラー: {e}")
            return False
    
    def _cleanup_expired_sessions(self, sessions: Dict) -> None:
        """
        期限切れのセッションをクリーンアップ
        
        Args:
            sessions: セッションデータ
        """
        current_time = datetime.now()
        expired_users = []
        
        for user_id, session_data in sessions.items():
            if 'expires_at' in session_data:
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if current_time > expires_at:
                    expired_users.append(user_id)
        
        for user_id in expired_users:
            del sessions[user_id]
    
    def set_user_state(
        self,
        user_id: str,
        state: str,
        expires_minutes: int = 30
    ) -> bool:
        """
        ユーザーの状態を設定
        
        Args:
            user_id: ユーザーID
            state: 状態（'movie_search', 'theater_search', 'idle'など）
            expires_minutes: セッション有効期限（分）
            
        Returns:
            bool: 設定が成功したかどうか
        """
        try:
            expires_at = datetime.now() + timedelta(minutes=expires_minutes)
            
            self.sessions[user_id] = {
                'state': state,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat(),
                'last_activity': datetime.now().isoformat()
            }
            
            return self._save_sessions()
            
        except Exception as e:
            print(f"ユーザー状態の設定エラー: {e}")
            return False
    
    def get_user_state(self, user_id: str) -> Optional[str]:
        """
        ユーザーの状態を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            str: ユーザーの状態、セッションがない場合はNone
        """
        if user_id not in self.sessions:
            return None
        
        session_data = self.sessions[user_id]
        
        # 期限切れチェック
        if 'expires_at' in session_data:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                self.clear_user_state(user_id)
                return None
        
        # 最終活動時間を更新
        session_data['last_activity'] = datetime.now().isoformat()
        self._save_sessions()
        
        return session_data.get('state')
    
    def clear_user_state(self, user_id: str) -> bool:
        """
        ユーザーの状態をクリア
        
        Args:
            user_id: ユーザーID
            
        Returns:
            bool: クリアが成功したかどうか
        """
        try:
            if user_id in self.sessions:
                del self.sessions[user_id]
                return self._save_sessions()
            return True
            
        except Exception as e:
            print(f"ユーザー状態のクリアエラー: {e}")
            return False
    
    def get_session_info(self, user_id: str) -> Optional[Dict]:
        """
        ユーザーのセッション情報を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            Dict: セッション情報、セッションがない場合はNone
        """
        if user_id not in self.sessions:
            return None
        
        session_data = self.sessions[user_id]
        
        # 期限切れチェック
        if 'expires_at' in session_data:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                self.clear_user_state(user_id)
                return None
        
        return session_data
    
    def get_active_sessions_count(self) -> int:
        """
        アクティブなセッション数を取得
        
        Returns:
            int: アクティブなセッション数
        """
        # 期限切れのセッションをクリーンアップ
        self._cleanup_expired_sessions(self.sessions)
        self._save_sessions()
        
        return len(self.sessions)
    
    def cleanup_all_expired_sessions(self) -> int:
        """
        すべての期限切れセッションをクリーンアップ
        
        Returns:
            int: クリーンアップしたセッション数
        """
        before_count = len(self.sessions)
        self._cleanup_expired_sessions(self.sessions)
        self._save_sessions()
        after_count = len(self.sessions)
        
        return before_count - after_count


def test_session_manager():
    """セッション管理のテスト"""
    print("セッション管理システムのテスト...\n")
    
    # セッションマネージャーを初期化
    session_manager = SessionManager()
    
    # テスト用ユーザーID
    test_user_id = "test_user_123"
    
    print("1. ユーザー状態の設定テスト")
    success = session_manager.set_user_state(test_user_id, "movie_search", 5)  # 5分で期限切れ
    print(f"   状態設定: {'成功' if success else '失敗'}")
    
    print("\n2. ユーザー状態の取得テスト")
    state = session_manager.get_user_state(test_user_id)
    print(f"   取得した状態: {state}")
    
    print("\n3. セッション情報の取得テスト")
    session_info = session_manager.get_session_info(test_user_id)
    if session_info:
        print(f"   セッション情報: {session_info}")
    else:
        print("   セッション情報: なし")
    
    print("\n4. アクティブセッション数の取得テスト")
    active_count = session_manager.get_active_sessions_count()
    print(f"   アクティブセッション数: {active_count}")
    
    print("\n5. ユーザー状態のクリアテスト")
    success = session_manager.clear_user_state(test_user_id)
    print(f"   状態クリア: {'成功' if success else '失敗'}")
    
    state_after_clear = session_manager.get_user_state(test_user_id)
    print(f"   クリア後の状態: {state_after_clear}")
    
    print("\n6. 期限切れセッションのクリーンアップテスト")
    # 期限切れのセッションを作成
    session_manager.sessions["expired_user"] = {
        'state': 'test',
        'created_at': (datetime.now() - timedelta(hours=1)).isoformat(),
        'expires_at': (datetime.now() - timedelta(minutes=1)).isoformat(),
        'last_activity': (datetime.now() - timedelta(hours=1)).isoformat()
    }
    
    cleaned_count = session_manager.cleanup_all_expired_sessions()
    print(f"   クリーンアップしたセッション数: {cleaned_count}")
    
    print("\n✓ セッション管理システムのテストが完了しました")


if __name__ == "__main__":
    test_session_manager()
