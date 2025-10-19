# LINE Messaging API 機能一覧

このドキュメントでは、LINE Messaging API を使用してコードから管理・実装できる機能を網羅的に記載しています。

## 📋 目次

- [メッセージ送信機能](#メッセージ送信機能)
- [リッチコンテンツ](#リッチコンテンツ)
- [インタラクティブ機能](#インタラクティブ機能)
- [ユーザー・グループ管理](#ユーザーグループ管理)
- [リッチメニュー](#リッチメニュー)
- [LIFF（LINE Front-end Framework）](#liffline-front-end-framework)
- [Beacon](#beacon)
- [LINE Login](#line-login)
- [その他の機能](#その他の機能)
- [制限事項](#制限事項)

---

## メッセージ送信機能

### 1. Push API（プッシュメッセージ）

Bot 側から能動的にメッセージを送信できる機能。

**特徴:**

- ユーザーやグループに対して自由なタイミングで送信可能
- 月 1,000 通まで無料（無料プラン）
- 複数のメッセージを一度に送信可能（最大 5 件）

**実装例:**

```python
def send_push_message(user_id: str, text: str):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'to': user_id,
        'messages': [{'type': 'text', 'text': text}]
    }
    requests.post(url, headers=headers, json=data)
```

**使用例:**

- 定期通知（週次映画情報など）
- リマインダー
- アラート通知

### 2. Reply API（返信メッセージ）

ユーザーからのメッセージに対して返信する機能。

**特徴:**

- reply token を使用（1 回のみ有効、発行から 1 分間有効）
- 通知料金が無料
- 複数のメッセージを一度に送信可能（最大 5 件）

**実装例:**

```python
def send_reply_message(reply_token: str, text: str):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': text}]
    }
    requests.post(url, headers=headers, json=data)
```

**使用例:**

- ユーザーの質問への回答
- キーワード検索結果の返信
- インタラクティブな会話

### 3. Multicast API（複数ユーザーへの一斉送信）

複数のユーザーに同じメッセージを一斉送信。

**特徴:**

- 最大 500 人まで同時送信可能
- 各ユーザーへの送信として課金される

**実装例:**

```python
def send_multicast(user_ids: list, text: str):
    url = 'https://api.line.me/v2/bot/message/multicast'
    data = {
        'to': user_ids,
        'messages': [{'type': 'text', 'text': text}]
    }
    # 送信処理...
```

### 4. Broadcast API（全ユーザーへの一斉送信）

Bot の全友だちに一斉送信。

**特徴:**

- ユーザー ID を指定する必要がない
- 大量送信に適している
- 有料プランのみ利用可能

**実装例:**

```python
def send_broadcast(text: str):
    url = 'https://api.line.me/v2/bot/message/broadcast'
    data = {
        'messages': [{'type': 'text', 'text': text}]
    }
    # 送信処理...
```

### 5. Narrowcast API（セグメント配信）

ユーザーをセグメント（属性）で絞り込んで配信。

**特徴:**

- 年齢、性別、地域、OS などでフィルタリング可能
- 有料プランのみ利用可能

---

## リッチコンテンツ

### 1. テキストメッセージ

基本的なテキストメッセージ。

**特徴:**

- 最大 5,000 文字
- 絵文字使用可能
- URL は自動リンク化

**実装例:**

```python
{
    'type': 'text',
    'text': 'こんにちは！\n映画情報をお届けします。',
    'emojis': [
        {'index': 0, 'productId': '5ac1bfd5040ab15980c9b435', 'emojiId': '001'}
    ]
}
```

### 2. スタンプメッセージ

LINE スタンプを送信。

**実装例:**

```python
{
    'type': 'sticker',
    'packageId': '446',
    'stickerId': '1988'
}
```

### 3. 画像メッセージ

画像を送信。

**特徴:**

- JPEG、PNG 形式
- 最大 10MB
- プレビュー画像とオリジナル画像の URL が必要

**実装例:**

```python
{
    'type': 'image',
    'originalContentUrl': 'https://example.com/image.jpg',
    'previewImageUrl': 'https://example.com/preview.jpg'
}
```

### 4. 動画メッセージ

動画を送信。

**特徴:**

- MP4 形式
- 最大 200MB
- 最長 1 分

**実装例:**

```python
{
    'type': 'video',
    'originalContentUrl': 'https://example.com/video.mp4',
    'previewImageUrl': 'https://example.com/preview.jpg'
}
```

### 5. 音声メッセージ

音声を送信。

**特徴:**

- M4A 形式
- 最大 200MB
- 最長 1 分

**実装例:**

```python
{
    'type': 'audio',
    'originalContentUrl': 'https://example.com/audio.m4a',
    'duration': 60000  # ミリ秒
}
```

### 6. 位置情報メッセージ

地図と位置情報を送信。

**実装例:**

```python
{
    'type': 'location',
    'title': '映画館',
    'address': '東京都渋谷区',
    'latitude': 35.6581,
    'longitude': 139.7414
}
```

### 7. Flex Message（フレックスメッセージ）

カスタマイズ可能なリッチメッセージ。

**特徴:**

- 柔軟なレイアウト設計
- 画像、テキスト、ボタンを自由に配置
- レスポンシブ対応

**実装例:**

```python
{
    'type': 'flex',
    'altText': '映画情報カード',
    'contents': {
        'type': 'bubble',
        'hero': {
            'type': 'image',
            'url': 'https://example.com/movie-poster.jpg',
            'size': 'full',
            'aspectRatio': '20:13',
            'aspectMode': 'cover'
        },
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents': [
                {
                    'type': 'text',
                    'text': '映画タイトル',
                    'weight': 'bold',
                    'size': 'xl'
                },
                {
                    'type': 'box',
                    'layout': 'baseline',
                    'margin': 'md',
                    'contents': [
                        {
                            'type': 'text',
                            'text': '公開日: 2025年10月18日',
                            'size': 'sm',
                            'color': '#999999'
                        }
                    ]
                }
            ]
        },
        'footer': {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'sm',
            'contents': [
                {
                    'type': 'button',
                    'style': 'primary',
                    'action': {
                        'type': 'uri',
                        'label': '詳細を見る',
                        'uri': 'https://eiga.com/movie/12345/'
                    }
                }
            ]
        }
    }
}
```

**Flex Message の種類:**

- **Bubble**: 1 つのカード
- **Carousel**: 複数のカードを横スクロール

### 8. Template Message（テンプレートメッセージ）

事前定義されたテンプレート。

#### Buttons Template（ボタンテンプレート）

```python
{
    'type': 'template',
    'altText': '映画を選択',
    'template': {
        'type': 'buttons',
        'thumbnailImageUrl': 'https://example.com/image.jpg',
        'title': '映画情報',
        'text': 'どの映画の情報を見ますか？',
        'actions': [
            {
                'type': 'message',
                'label': '過去1週間',
                'text': '過去1週間の映画'
            },
            {
                'type': 'message',
                'label': '今後1週間',
                'text': '今後1週間の映画'
            }
        ]
    }
}
```

#### Confirm Template（確認テンプレート）

```python
{
    'type': 'template',
    'altText': '確認',
    'template': {
        'type': 'confirm',
        'text': '通知を受け取りますか？',
        'actions': [
            {'type': 'message', 'label': 'はい', 'text': 'はい'},
            {'type': 'message', 'label': 'いいえ', 'text': 'いいえ'}
        ]
    }
}
```

#### Carousel Template（カルーセルテンプレート）

```python
{
    'type': 'template',
    'altText': '映画一覧',
    'template': {
        'type': 'carousel',
        'columns': [
            {
                'thumbnailImageUrl': 'https://example.com/movie1.jpg',
                'title': '映画1',
                'text': '説明文',
                'actions': [
                    {'type': 'uri', 'label': '詳細', 'uri': 'https://...'}
                ]
            },
            # 最大10カラムまで
        ]
    }
}
```

#### Image Carousel Template（画像カルーセル）

```python
{
    'type': 'template',
    'altText': '映画ポスター',
    'template': {
        'type': 'image_carousel',
        'columns': [
            {
                'imageUrl': 'https://example.com/poster1.jpg',
                'action': {
                    'type': 'uri',
                    'uri': 'https://eiga.com/movie/1/'
                }
            }
        ]
    }
}
```

---

## インタラクティブ機能

### 1. Quick Reply（クイックリプライ）

メッセージ下部に表示される選択肢ボタン。

**特徴:**

- 最大 13 個まで設定可能
- タップすると自動的にメッセージ送信
- アイコン画像を設定可能

**実装例:**

```python
{
    'type': 'text',
    'text': 'どの期間の映画を見ますか？',
    'quickReply': {
        'items': [
            {
                'type': 'action',
                'imageUrl': 'https://example.com/icon1.png',
                'action': {
                    'type': 'message',
                    'label': '過去1週間',
                    'text': '過去1週間の映画'
                }
            },
            {
                'type': 'action',
                'action': {
                    'type': 'message',
                    'label': '今後1週間',
                    'text': '今後1週間の映画'
                }
            },
            {
                'type': 'action',
                'action': {
                    'type': 'location',
                    'label': '位置情報を送信'
                }
            },
            {
                'type': 'action',
                'action': {
                    'type': 'camera',
                    'label': 'カメラを起動'
                }
            },
            {
                'type': 'action',
                'action': {
                    'type': 'cameraRoll',
                    'label': 'カメラロール'
                }
            }
        ]
    }
}
```

**Quick Reply で利用可能なアクション:**

- `message`: テキスト送信
- `postback`: データ送信（非表示）
- `uri`: URL 起動
- `location`: 位置情報送信
- `camera`: カメラ起動
- `cameraRoll`: カメラロール開く
- `datetimepicker`: 日時選択

### 2. Action Objects（アクションオブジェクト）

ボタンやリンクに設定できるアクション。

#### Postback Action

```python
{
    'type': 'postback',
    'label': '詳細を見る',
    'data': 'action=detail&movieId=12345',
    'displayText': '詳細を表示しました'
}
```

#### Message Action

```python
{
    'type': 'message',
    'label': '検索',
    'text': '映画を検索'
}
```

#### URI Action

```python
{
    'type': 'uri',
    'label': 'Webサイトを開く',
    'uri': 'https://eiga.com'
}
```

#### Datetime Picker Action

```python
{
    'type': 'datetimepicker',
    'label': '日付を選択',
    'data': 'action=selectDate',
    'mode': 'datetime',  # date, time, datetime
    'initial': '2025-10-18T00:00',
    'max': '2025-12-31T23:59',
    'min': '2025-01-01T00:00'
}
```

#### Camera Action

```python
{
    'type': 'camera',
    'label': 'カメラ'
}
```

#### Camera Roll Action

```python
{
    'type': 'cameraRoll',
    'label': 'カメラロール'
}
```

#### Location Action

```python
{
    'type': 'location',
    'label': '位置情報'
}
```

### 3. Imagemap Message（イメージマップメッセージ）

画像の特定領域にリンクやアクションを設定。

**実装例:**

```python
{
    'type': 'imagemap',
    'baseUrl': 'https://example.com/image',
    'altText': '映画館マップ',
    'baseSize': {
        'width': 1040,
        'height': 1040
    },
    'actions': [
        {
            'type': 'uri',
            'linkUri': 'https://example.com/theater1',
            'area': {
                'x': 0,
                'y': 0,
                'width': 520,
                'height': 520
            }
        }
    ]
}
```

---

## ユーザー・グループ管理

### 1. ユーザープロフィール取得

友だち追加したユーザーの情報を取得。

**取得可能な情報:**

- 表示名（displayName）
- ユーザー ID（userId）
- プロフィール画像 URL（pictureUrl）
- ステータスメッセージ（statusMessage）

**実装例:**

```python
def get_user_profile(user_id: str):
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
    # {
    #   "displayName": "山田太郎",
    #   "userId": "U1234567890abcdef",
    #   "pictureUrl": "https://...",
    #   "statusMessage": "よろしくお願いします"
    # }
```

### 2. グループ情報取得

Bot が参加しているグループの情報を取得。

**取得可能な情報:**

- グループ名（groupName）
- グループ ID（groupId）
- グループアイコン URL（pictureUrl）

**実装例:**

```python
def get_group_summary(group_id: str):
    url = f'https://api.line.me/v2/bot/group/{group_id}/summary'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
```

### 3. グループメンバー情報取得

グループ内のメンバーリストを取得。

**実装例:**

```python
def get_group_members(group_id: str):
    url = f'https://api.line.me/v2/bot/group/{group_id}/members/ids'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
```

### 4. グループメンバー数取得

グループの参加人数を取得。

**実装例:**

```python
def get_group_members_count(group_id: str):
    url = f'https://api.line.me/v2/bot/group/{group_id}/members/count'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()['count']
```

### 5. グループ・トークルームからの退出

Bot をグループやトークルームから退出させる。

**実装例:**

```python
def leave_group(group_id: str):
    url = f'https://api.line.me/v2/bot/group/{group_id}/leave'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    requests.post(url, headers=headers)
```

---

## リッチメニュー

トーク画面下部に固定表示されるメニュー。

### 1. リッチメニューの作成

**特徴:**

- 画像とタップ領域を設定
- 最大 6 つのアクション領域
- ユーザーごとに異なるメニュー表示可能

**実装例:**

```python
def create_rich_menu():
    url = 'https://api.line.me/v2/bot/richmenu'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'size': {
            'width': 2500,
            'height': 1686
        },
        'selected': True,
        'name': '映画情報メニュー',
        'chatBarText': 'メニューを開く',
        'areas': [
            {
                'bounds': {
                    'x': 0,
                    'y': 0,
                    'width': 1250,
                    'height': 843
                },
                'action': {
                    'type': 'message',
                    'text': '過去1週間の映画'
                }
            },
            {
                'bounds': {
                    'x': 1250,
                    'y': 0,
                    'width': 1250,
                    'height': 843
                },
                'action': {
                    'type': 'message',
                    'text': '今後1週間の映画'
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['richMenuId']
```

### 2. リッチメニュー画像のアップロード

```python
def upload_rich_menu_image(rich_menu_id: str, image_path: str):
    url = f'https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'image/png'
    }
    with open(image_path, 'rb') as f:
        requests.post(url, headers=headers, data=f)
```

### 3. リッチメニューとユーザーの紐付け

```python
def link_rich_menu_to_user(user_id: str, rich_menu_id: str):
    url = f'https://api.line.me/v2/bot/user/{user_id}/richmenu/{rich_menu_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    requests.post(url, headers=headers)
```

### 4. デフォルトリッチメニューの設定

```python
def set_default_rich_menu(rich_menu_id: str):
    url = f'https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    requests.post(url, headers=headers)
```

---

## LIFF（LINE Front-end Framework）

LINE 内で動作する Web アプリケーション。

### 特徴

- LINE 内ブラウザで動作
- LINE のユーザー情報を取得可能
- JavaScript の SDK を使用
- トーク画面に情報を送信可能

### LIFF URL の生成

```python
def create_liff_app(view_type: str, url: str):
    """
    view_type: 'compact', 'tall', 'full'
    """
    api_url = 'https://api.line.me/liff/v1/apps'
    headers = {
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'view': {
            'type': view_type,
            'url': url
        }
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()['liffId']
```

### LIFF アプリ内での実装（JavaScript）

```javascript
// LIFF初期化
liff.init({ liffId: 'YOUR_LIFF_ID' }).then(() => {
  if (!liff.isLoggedIn()) {
    liff.login();
  } else {
    // ユーザープロフィール取得
    liff.getProfile().then(profile => {
      console.log(profile.displayName);
      console.log(profile.userId);
    });

    // メッセージ送信
    liff.sendMessages([
      {
        type: 'text',
        text: '送信するメッセージ',
      },
    ]);
  }
});
```

---

## Beacon

LINE Beacon を使った位置ベースのメッセージング。

### 特徴

- Bluetooth Low Energy (BLE) を使用
- ユーザーが Beacon の近くに来たときにイベント発火
- 店舗やイベント会場での活用

### Beacon イベントの受信

```python
# Webhookで受信
{
    'type': 'beacon',
    'replyToken': 'xxxx',
    'source': {...},
    'timestamp': 1234567890,
    'beacon': {
        'hwid': 'beacon-hardware-id',
        'type': 'enter'  # or 'leave', 'banner'
    }
}
```

---

## LINE Login

LINE 認証を使ったログイン機能。

### 特徴

- ユーザーの LINE アカウントで認証
- プロフィール情報の取得
- メールアドレスの取得（要申請）

### 実装フロー

1. 認証 URL にリダイレクト
2. ユーザーが認証を許可
3. アクセストークンを取得
4. ユーザー情報を取得

**認証 URL:**

```
https://access.line.me/oauth2/v2.1/authorize?
  response_type=code&
  client_id={CHANNEL_ID}&
  redirect_uri={REDIRECT_URI}&
  state={STATE}&
  scope=profile%20openid%20email
```

---

## その他の機能

### 1. Account Link（アカウント連携）

外部サービスのアカウントと LINE アカウントを連携。

### 2. Webhook 統計情報

Webhook の配信状況を取得。

```python
def get_webhook_endpoint():
    url = 'https://api.line.me/v2/bot/channel/webhook/endpoint'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
```

### 3. メッセージ配信統計

送信したメッセージの統計情報を取得。

```python
def get_message_delivery(date: str):
    """date: YYYYMMDD形式"""
    url = f'https://api.line.me/v2/bot/insight/message/delivery?date={date}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
```

### 4. 友だち追加数の取得

```python
def get_followers_count():
    url = 'https://api.line.me/v2/bot/insight/followers'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
```

### 5. コンテンツの取得

ユーザーが送信した画像・動画・音声を取得。

```python
def get_message_content(message_id: str):
    url = f'https://api-data.line.me/v2/bot/message/{message_id}/content'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.content  # バイナリデータ
```

### 6. Webhook 検証

署名検証で Webhook の正当性を確認。

```python
import hmac
import hashlib
import base64

def verify_signature(body: str, signature: str, channel_secret: str):
    hash_digest = hmac.new(
        channel_secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash_digest).decode('utf-8')
    return signature == expected_signature
```

---

## 制限事項

### ❌ できないこと

1. **過去のメッセージの操作**

   - 送信済みメッセージの編集・削除不可
   - ユーザーのメッセージ履歴の閲覧不可
   - メッセージの既読状態の管理不可

2. **トーク画面の外観変更**

   - 背景色、フォント、レイアウトの変更不可
   - リッチメニュー以外の UI 要素の追加不可

3. **ユーザー操作の制限**

   - ユーザーのブロック/ブロック解除の操作不可
   - 友だち追加の強制不可
   - トーク画面の開閉制御不可

4. **全メッセージの監視**

   - グループ内の全メッセージの取得不可
   - Bot がメンションされた/DM されたメッセージのみ受信可能

5. **プッシュ通知の細かい制御**
   - 通知音、バイブレーションのカスタマイズ不可
   - 通知の優先度設定不可

### 📊 利用制限

| 項目                   | 制限                           |
| ---------------------- | ------------------------------ |
| Push API（無料プラン） | 月 1,000 通まで                |
| Reply API              | 無制限（但し通信料として課金） |
| メッセージ同時送信数   | 最大 5 件                      |
| Multicast 送信先       | 最大 500 人                    |
| Quick Reply 項目数     | 最大 13 個                     |
| Carousel カラム数      | 最大 10 個                     |
| 画像サイズ             | 最大 10MB（JPEG, PNG）         |
| 動画サイズ             | 最大 200MB（MP4、最長 1 分）   |
| 音声サイズ             | 最大 200MB（M4A、最長 1 分）   |
| リッチメニューエリア数 | 最大 20 個                     |

---

## 参考リンク

- [LINE Messaging API 公式ドキュメント](https://developers.line.biz/ja/docs/messaging-api/)
- [LINE Developers Console](https://developers.line.biz/console/)
- [Flex Message Simulator](https://developers.line.biz/flex-simulator/)
- [LINE API Reference](https://developers.line.biz/ja/reference/messaging-api/)

---

## 更新履歴

- 2025-10-19: 初版作成
