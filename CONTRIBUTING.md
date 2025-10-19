# 🤝 コントリビューションガイド

映画情報LINE Botへのコントリビューションを歓迎します！

## 📋 目次

- [行動規範](#行動規範)
- [貢献の方法](#貢献の方法)
- [開発の流れ](#開発の流れ)
- [コーディングスタイル](#コーディングスタイル)
- [コミットメッセージ](#コミットメッセージ)
- [Pull Requestの提出](#pull-requestの提出)
- [質問とサポート](#質問とサポート)

---

## 行動規範

このプロジェクトは、すべての参加者に対して敬意を持って接することを期待しています。

### 期待される行動

- ✅ 建設的なフィードバックを提供する
- ✅ 他の貢献者の視点を尊重する
- ✅ プロフェッショナルな態度を保つ
- ✅ 親切で協力的であること

### 禁止される行動

- ❌ ハラスメント、差別的な言動
- ❌ 侮辱的・攻撃的なコメント
- ❌ 個人情報の公開
- ❌ 他の参加者への嫌がらせ

---

## 貢献の方法

### バグ報告

バグを見つけた場合は、GitHubのIssueで報告してください。

#### 良いバグ報告に含まれるべき情報

- **タイトル**: 簡潔で明確なタイトル
- **説明**: 問題の詳細な説明
- **再現手順**: バグを再現する手順
- **期待される動作**: 本来どうあるべきか
- **実際の動作**: 実際に何が起こったか
- **環境情報**: OS、Pythonバージョンなど
- **スクリーンショット**: 可能であれば

#### テンプレート

```markdown
## バグの説明
簡潔にバグを説明してください。

## 再現手順
1. '...'に移動
2. '...'をクリック
3. 下にスクロール
4. エラーを確認

## 期待される動作
何が起こるべきだったかを明確に説明してください。

## スクリーンショット
可能であれば、問題を説明するスクリーンショットを追加してください。

## 環境
 - OS: [例: macOS 14.0]
 - Python: [例: 3.11.5]
 - その他の関連情報

## 追加のコンテキスト
問題について他に追加すべき情報があれば記載してください。
```

### 機能リクエスト

新機能の提案もGitHubのIssueで受け付けています。

#### 良い機能リクエストに含まれるべき情報

- **タイトル**: 機能を簡潔に説明
- **問題**: 解決したい問題
- **提案**: 解決策の提案
- **代替案**: 検討した代替案
- **追加情報**: その他の関連情報

### コードの貢献

コードの貢献は大歓迎です！

#### 貢献できる領域

- 🐛 バグ修正
- ✨ 新機能の実装
- 📝 ドキュメントの改善
- 🎨 UIの改善
- ⚡️ パフォーマンスの最適化
- ♻️ リファクタリング
- ✅ テストの追加

---

## 開発の流れ

### 1. リポジトリのフォーク

GitHubでリポジトリをフォークします。

```bash
# フォークしたリポジトリをクローン
git clone https://github.com/your-username/movie-line-bot.git
cd movie-line-bot

# アップストリームを追加
git remote add upstream https://github.com/original-owner/movie-line-bot.git
```

### 2. ブランチの作成

機能ごとに新しいブランチを作成します。

```bash
# 最新のmainブランチを取得
git checkout main
git pull upstream main

# 新しいブランチを作成
git checkout -b feature/your-feature-name
```

#### ブランチ命名規則

- `feature/機能名`: 新機能
- `fix/バグ名`: バグ修正
- `docs/内容`: ドキュメント更新
- `refactor/内容`: リファクタリング
- `test/内容`: テスト追加

例：
- `feature/add-favorite-movies`
- `fix/webhook-timeout`
- `docs/update-api-reference`

### 3. 開発環境のセットアップ

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 開発用パッケージのインストール
pip install black flake8 mypy pillow
```

### 4. 変更の実装

- コードを記述
- テストを追加
- ドキュメントを更新

### 5. コードの確認

```bash
# コードフォーマット
black src/

# リンター
flake8 src/

# 型チェック
mypy src/

# テスト実行
python src/your_module.py
```

### 6. コミット

```bash
git add .
git commit -m "✨ 機能: 新機能の説明"
```

### 7. プッシュ

```bash
git push origin feature/your-feature-name
```

### 8. Pull Requestの作成

GitHubでPull Requestを作成します。

---

## コーディングスタイル

### Pythonスタイル

このプロジェクトは[PEP 8](https://pep8-ja.readthedocs.io/ja/latest/)に準拠しています。

#### フォーマット

```bash
# Blackで自動フォーマット
black src/
```

#### リンター

```bash
# flake8でチェック
flake8 src/
```

#### 型ヒント

```python
from typing import List, Dict, Optional

def fetch_movies(keyword: str) -> List[Dict]:
    """映画を検索"""
    pass

def get_user_state(user_id: str) -> Optional[str]:
    """ユーザー状態を取得"""
    pass
```

#### docstring

```python
def search_movie_by_keyword(self, keyword: str) -> List[Dict]:
    """
    キーワードで映画を検索
    
    Args:
        keyword: 検索キーワード
        
    Returns:
        List[Dict]: 映画情報のリスト
        
    Raises:
        ValueError: キーワードが空の場合
    """
    if not keyword:
        raise ValueError("キーワードを指定してください")
    # 処理
```

---

## コミットメッセージ

### 形式

```
<絵文字> <タイプ>: <説明>

<詳細な説明（オプション）>

<フッター（オプション）>
```

### タイプと絵文字

| タイプ | 絵文字 | 説明 |
|--------|--------|------|
| feat | ✨ | 新機能 |
| fix | 🐛 | バグ修正 |
| docs | 📝 | ドキュメント |
| style | 🎨 | フォーマット |
| refactor | ♻️ | リファクタリング |
| test | ✅ | テスト |
| chore | 🔧 | その他 |

### 例

```bash
# 良い例
git commit -m "✨ feat: 映画のお気に入り機能を追加"
git commit -m "🐛 fix: Webhook署名検証エラーを修正"
git commit -m "📝 docs: APIリファレンスを更新"

# 悪い例
git commit -m "update"
git commit -m "fix bug"
git commit -m "test"
```

### 詳細な説明が必要な場合

```bash
git commit -m "✨ feat: 映画のお気に入り機能を追加

ユーザーが映画をお気に入りに追加できるようになりました。
- お気に入りの追加・削除機能
- お気に入り一覧の表示
- データベースへの保存

Closes #123"
```

---

## Pull Requestの提出

### PRの作成

1. GitHubでPull Requestを作成
2. 以下のテンプレートに従って記入

### PRテンプレート

```markdown
## 変更の概要
この Pull Request の変更内容を簡潔に説明してください。

## 変更の種類
- [ ] バグ修正
- [ ] 新機能
- [ ] ドキュメント更新
- [ ] リファクタリング
- [ ] その他（説明してください）

## 関連するIssue
Closes #（Issue番号）

## 変更内容の詳細
- 変更1
- 変更2
- 変更3

## テスト
どのようにテストしましたか？
- [ ] ユニットテスト
- [ ] 統合テスト
- [ ] 手動テスト

## スクリーンショット
該当する場合、スクリーンショットを追加してください。

## チェックリスト
- [ ] コードがPEP 8に準拠している
- [ ] 型ヒントが付いている
- [ ] docstringが書かれている
- [ ] テストが追加されている
- [ ] ドキュメントが更新されている
- [ ] リンターでエラーがない
- [ ] 動作確認済み
```

### レビュープロセス

1. **自動チェック**: GitHub Actionsが自動的に実行
2. **コードレビュー**: メンテナーがレビュー
3. **修正**: フィードバックに基づいて修正
4. **承認**: レビューが承認されたらマージ

### レビュー後の修正

```bash
# フィードバックに基づいて修正
git add .
git commit -m "🐛 fix: レビューフィードバックに対応"
git push origin feature/your-feature-name
```

---

## テスト

### テストの追加

新機能を追加する場合は、テストも追加してください。

```python
# src/your_module.py
def test_your_function():
    """あなたの関数のテスト"""
    print("テスト実行中...")
    
    # テストケース1
    result = your_function("test")
    assert result == expected_result, "テスト失敗"
    
    print("✓ テスト成功")

if __name__ == "__main__":
    test_your_function()
```

### テストの実行

```bash
python src/your_module.py
```

---

## ドキュメント

### ドキュメントの更新

コードの変更に伴い、以下のドキュメントを更新してください：

- `README.md`: プロジェクト概要、使い方
- `docs/API_REFERENCE.md`: API仕様
- `docs/DEVELOPER_GUIDE.md`: 開発者向け情報
- `CHANGELOG.md`: 変更履歴

### docstringの記述

```python
def fetch_movies(keyword: str, max_count: int = 10) -> List[Dict]:
    """
    キーワードで映画を検索
    
    Args:
        keyword: 検索キーワード
        max_count: 最大取得件数（デフォルト: 10）
        
    Returns:
        List[Dict]: 映画情報のリスト
            - title (str): 映画タイトル
            - url (str): 詳細URL
            - release_date (str): 公開日
        
    Raises:
        ValueError: キーワードが空の場合
        
    Examples:
        >>> movies = fetch_movies("アベンジャーズ")
        >>> print(len(movies))
        10
    """
    pass
```

---

## 質問とサポート

### 質問する前に

1. [README.md](README.md)を確認
2. [ドキュメント](docs/)を確認
3. [既存のIssue](https://github.com/your-username/movie-line-bot/issues)を検索

### 質問方法

質問はGitHubのIssueで受け付けています。

#### 質問のテンプレート

```markdown
## 質問
質問内容を記載してください。

## 試したこと
すでに試したことを記載してください。

## 環境
- OS: 
- Python: 
- その他: 
```

### コミュニティ

- **GitHub Discussions**: 一般的な質問や議論
- **GitHub Issues**: バグ報告や機能リクエスト
- **Pull Requests**: コードの貢献

---

## ライセンス

このプロジェクトに貢献することにより、あなたの貢献がMITライセンスの下でライセンスされることに同意したものとみなされます。

---

## 謝辞

コントリビューターの皆様に感謝します！

---

## 更新履歴

- 2025-10-19: 初版作成

---

**Happy Contributing! 🎬**

