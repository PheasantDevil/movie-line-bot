# ❓ よくある質問（FAQ）

## セットアップ関連

### Q1: LINE Bot を作るのにお金はかかりますか？

**A**: いいえ、完全無料で運用できます。

- LINE Messaging API: 無料枠（1,000 通/月）
- GitHub Actions: 無料枠（2,000 分/月）
- データ保存: GitHub で無料

このプロジェクトの使用量は両方の無料枠内に収まります。

---

### Q2: LINE User ID はどうやって取得しますか？

**A**: 以下の方法があります：

**方法 1: LINE Official Account Manager で確認**

1. https://manager.line.biz/ にアクセス
2. 作成したアカウントを選択
3. 設定から確認可能

**方法 2: Webhook で取得**

1. 一時的に Webhook を設定
2. Bot にメッセージを送信
3. Webhook のログで user ID を確認

**方法 3: 友人に協力してもらう**

- 既に LINE Bot を持っている友人に確認してもらう

---

### Q3: GitHub Actions が実行されません

**A**: 以下を確認してください：

1. **Secrets が正しく設定されているか**

   - Settings > Secrets and variables > Actions
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_USER_ID`

2. **Workflow permissions が正しいか**

   - Settings > Actions > General
   - "Read and write permissions" を選択

3. **ワークフローが有効か**
   - Actions タブで確認
   - 必要に応じて有効化

---

### Q4: 通知が届きません

**A**: チェックリスト：

- [ ] LINE Bot を友だち追加しているか
- [ ] User ID が正しいか（`U`で始まる文字列）
- [ ] Channel Access Token が正しいか
- [ ] GitHub Actions のログにエラーがないか
- [ ] LINE Bot がブロックされていないか

---

## 機能関連

### Q5: 通知の時刻を変更できますか？

**A**: はい、できます。

`.github/workflows/check-movies.yml` の cron 設定を変更：

```yaml
schedule:
  - cron: '0 0 * * *' # UTC 0時 = JST 9時
  # 例: UTC 12時 = JST 21時 にしたい場合
  # - cron: "0 12 * * *"
```

**注意**: 時刻は UTC（協定世界時）で指定します。日本時間（JST）は UTC+9 時間です。

---

### Q6: 複数のユーザーに通知できますか？

**A**: 現在のバージョンでは 1 ユーザーのみ対応です。

複数ユーザー対応は今後のバージョンで実装予定ですが、コードを修正すれば可能です：

```python
# src/line_notifier.py を修正
user_ids = ['U1234...', 'U5678...', 'U9012...']
for user_id in user_ids:
    # 各ユーザーに送信
```

---

### Q7: 通知される映画の数を増やせますか？

**A**: はい、`src/line_notifier.py` を編集します：

```python
# 現在: 最大10件
for i, movie in enumerate(movies[:10], 1):

# 変更例: 最大20件
for i, movie in enumerate(movies[:20], 1):
```

**注意**: LINE メッセージには文字数制限（5,000 文字）があります。

---

### Q8: アニメ映画だけ通知することはできますか？

**A**: 現在のバージョンではジャンル情報を取得していないため、フィルタリングできません。

将来のバージョンで対応予定です。現状で実装したい場合は、`src/scraper.py` でジャンル情報も取得し、`src/main.py` でフィルタリングする必要があります。

---

## トラブルシューティング

### Q9: スクレイピングが突然失敗しました

**A**: 考えられる原因：

1. **映画.com の HTML 構造が変更された**

   - 最も可能性が高い
   - `src/scraper.py` の修正が必要
   - GitHub で Issue を作成してください

2. **ネットワークエラー**

   - 一時的な問題の可能性
   - 次回実行で解決する場合がある

3. **映画.com がダウンしている**
   - https://eiga.com/ にアクセスして確認

---

### Q10: データファイルが更新されません

**A**: GitHub Actions の権限を確認：

1. Settings > Actions > General
2. Workflow permissions
3. "Read and write permissions" を選択
4. Save

これにより、GitHub Actions がファイルをコミット・プッシュできるようになります。

---

### Q11: エラーログはどこで見れますか？

**A**: GitHub Actions のログで確認できます：

1. リポジトリの「Actions」タブを開く
2. 失敗した実行をクリック
3. 「check-and-notify」ジョブをクリック
4. 各ステップのログを確認

---

## カスタマイズ

### Q12: 通知メッセージのフォーマットを変更できますか？

**A**: はい、`src/line_notifier.py` の `_format_movie_message()` メソッドを編集します：

```python
def _format_movie_message(self, movies: List[Dict]) -> str:
    # ここでフォーマットをカスタマイズ
    header = f"🎬 新作映画 ({len(movies)}件)\n"
    # ...
```

---

### Q13: 他の映画サイトからも情報を取得できますか？

**A**: はい、新しいスクレイパークラスを作成すれば可能です：

```python
# src/yahoo_scraper.py を作成
class YahooMovieScraper:
    def fetch_upcoming_movies(self):
        # Yahoo!映画をスクレイピング
        pass
```

詳しくは[開発ガイド](development_guide.md)を参照してください。

---

### Q14: データベースを使いたいです

**A**: `src/storage.py` を修正すれば可能です。

SQLite の例：

```python
import sqlite3

class MovieStorage:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db')
        self._create_table()

    def save_movies(self, movies):
        # SQLiteに保存
        pass
```

詳しくは[技術仕様書](technical_specifications.md)の拡張セクションを参照。

---

## その他

### Q15: このプロジェクトに貢献できますか？

**A**: もちろんです！大歓迎です。

1. リポジトリをフォーク
2. 新機能を実装またはバグを修正
3. プルリクエストを作成

詳しくは[開発ガイド](development_guide.md)を参照してください。

---

### Q16: 商用利用できますか？

**A**: はい、MIT ライセンスのため商用利用可能です。

ただし、以下の点にご注意ください：

- 映画.com のスクレイピングは個人利用の範囲で
- LINE Messaging API の利用規約を遵守
- 大量のトラフィックはサーバーに負荷をかける

---

### Q17: モバイルアプリ版はありますか？

**A**: 現在はありません。LINE で通知を受け取る形式です。

LINE Bot の利点：

- アプリインストール不要
- プッシュ通知が届く
- シンプルで使いやすい

---

### Q18: 実行頻度を増やせますか？

**A**: 技術的には可能ですが、推奨しません。

理由：

- 映画.com のサーバー負荷を考慮
- 新作映画は 1 日に数回も追加されない
- GitHub Actions の無料枠を消費

どうしても必要な場合は、cron を変更してください：

```yaml
schedule:
  - cron: '0 */6 * * *' # 6時間ごと
```

---

### Q19: 他のメッセージングサービスに対応していますか？

**A**: 現在は LINE のみ対応です。

他のサービスへの対応も可能です：

- Slack
- Discord
- Telegram
- Email

新しい通知クラスを作成すれば実装できます。

---

### Q20: プロジェクトのロードマップはありますか？

**A**: はい、[変更履歴](changelog.md)に今後の予定を記載しています。

主な予定：

- v1.1.0: 複数ユーザー対応、フィルタリング
- v1.2.0: 複数サイト対応、データベース
- v2.0.0: Web UI、統計機能

---

## 質問がここにない場合

GitHub Issues で質問してください：
https://github.com/your-username/movie-line-bot/issues

または、プルリクエストで FAQ を追加してください！
