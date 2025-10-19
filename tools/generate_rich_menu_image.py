"""リッチメニュー画像生成スクリプト

PIL（Pillow）を使用して2500x1686pxのリッチメニュー画像を生成します。
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_rich_menu_image(output_path: str = "assets/rich_menu.png"):
    """
    リッチメニュー画像を生成
    
    Args:
        output_path: 出力ファイルパス
    """
    # 画像サイズ（LINE推奨サイズ）
    width = 2500
    height = 1686
    
    # 背景色（黒）
    bg_color = (0, 0, 0)
    
    # テキスト色（白）
    text_color = (255, 255, 255)
    
    # アクセントカラー
    accent_color = (255, 87, 51)  # オレンジ
    
    # 画像を作成
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # グリッド線を描画（デバッグ用）
    line_color = (50, 50, 50)
    
    # 縦の中心線
    draw.line([(width // 2, 0), (width // 2, height)], fill=line_color, width=3)
    
    # 横の中心線
    draw.line([(0, height // 2), (width, height // 2)], fill=line_color, width=3)
    
    # 各ボタンの境界線を描画
    button_width = width // 2
    button_height = height // 2
    
    # 左上のボタン枠
    draw.rectangle(
        [(5, 5), (button_width - 5, button_height - 5)],
        outline=accent_color,
        width=5
    )
    
    # 右上のボタン枠
    draw.rectangle(
        [(button_width + 5, 5), (width - 5, button_height - 5)],
        outline=accent_color,
        width=5
    )
    
    # 左下のボタン枠
    draw.rectangle(
        [(5, button_height + 5), (button_width - 5, height - 5)],
        outline=accent_color,
        width=5
    )
    
    # 右下のボタン枠
    draw.rectangle(
        [(button_width + 5, button_height + 5), (width - 5, height - 5)],
        outline=accent_color,
        width=5
    )
    
    # フォント設定を試みる（システムにフォントがない場合はデフォルト）
    try:
        # macOSのヒラギノフォント
        font_large = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 150)
        font_emoji = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 200)
    except:
        try:
            # Ubuntuなどのフォント
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 150)
            font_emoji = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 200)
        except:
            print("警告: システムフォントが見つかりません。デフォルトフォントを使用します。")
            font_large = ImageFont.load_default()
            font_emoji = ImageFont.load_default()
    
    # 各ボタンにテキストを描画
    
    # 左上：映画検索
    emoji_y_offset = button_height // 2 - 250
    text_y_offset = button_height // 2 + 50
    
    draw.text(
        (button_width // 2, emoji_y_offset),
        "🎬",
        font=font_emoji,
        fill=text_color,
        anchor="mm"
    )
    draw.text(
        (button_width // 2, text_y_offset),
        "映画検索",
        font=font_large,
        fill=text_color,
        anchor="mm"
    )
    
    # 右上：映画館検索
    draw.text(
        (button_width + button_width // 2, emoji_y_offset),
        "🎪",
        font=font_emoji,
        fill=text_color,
        anchor="mm"
    )
    draw.text(
        (button_width + button_width // 2, text_y_offset),
        "映画館検索",
        font=font_large,
        fill=text_color,
        anchor="mm"
    )
    
    # 左下：今週公開
    draw.text(
        (button_width // 2, button_height + emoji_y_offset),
        "📅",
        font=font_emoji,
        fill=text_color,
        anchor="mm"
    )
    draw.text(
        (button_width // 2, button_height + text_y_offset),
        "今週公開",
        font=font_large,
        fill=text_color,
        anchor="mm"
    )
    
    # 右下：上映中
    draw.text(
        (button_width + button_width // 2, button_height + emoji_y_offset),
        "🎭",
        font=font_emoji,
        fill=text_color,
        anchor="mm"
    )
    draw.text(
        (button_width + button_width // 2, button_height + text_y_offset),
        "上映中",
        font=font_large,
        fill=text_color,
        anchor="mm"
    )
    
    # 画像を保存
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    image.save(output_path, "PNG")
    print(f"✓ リッチメニュー画像を生成しました: {output_path}")
    print(f"  サイズ: {width}x{height}px")
    
    return output_path


def main():
    """メイン処理"""
    print("=" * 60)
    print("リッチメニュー画像生成")
    print("=" * 60)
    print()
    
    # 画像を生成
    output_path = "assets/rich_menu.png"
    create_rich_menu_image(output_path)
    
    print()
    print("=" * 60)
    print("生成完了")
    print("=" * 60)
    print()
    print("次のステップ:")
    print("1. 生成された画像を確認してください")
    print("2. 必要に応じて画像を編集してください")
    print("3. リッチメニュー設定スクリプトを実行してください:")
    print("   python tools/setup_rich_menu.py")


if __name__ == "__main__":
    main()

