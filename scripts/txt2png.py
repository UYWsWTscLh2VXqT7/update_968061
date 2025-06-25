from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

INPUT_FILE = 'output.txt'
OUTPUT_FILE = 'output.png'

def main():
    with open(INPUT_FILE, encoding='utf-8') as f:
        text = f.read()

    # 自动换行，80字符一行
    lines = textwrap.wrap(text, width=80)

    # 计算图片尺寸（宽度800，高度根据行数算）
    width = 800
    line_height = 20
    height = line_height * len(lines) + 20

    # 创建黑底图像
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)

    # 尝试加载 Courier 字体，失败则用默认字体
    try:
        font = ImageFont.truetype("Courier.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # 文字起始位置
    x, y = 10, 10

    # 绘制每一行白色文字
    for line in lines:
        draw.text((x, y), line, font=font, fill='white')
        y += line_height

    # 保存图片
    img.save(OUTPUT_FILE)
    print(f"Saved image to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
