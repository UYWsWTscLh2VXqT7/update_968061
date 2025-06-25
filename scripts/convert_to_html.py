import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_ansi_color import AnsiColorLexer

# 读取 output.txt
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
cleaned_lines = []

for line in lines:
    # 去除 spawn 和 ^C
    if "spawn qdii-value" in line:
        continue
    if "^C" in line or "\x03" in line:
        continue
    # 去除控制码标题行，如 ?25l ... 中文标题
    if "?25" in line and re.search(r'[\u4e00-\u9fa5]', line):
        continue
    # 可选：过滤纯控制字符行
    if re.fullmatch(r'\x1b\[[0-9;?]*[a-zA-Z]', line.strip()):
        continue
    # 保留正常行
    cleaned_lines.append(line)

# 拼接为清理后的 ANSI 内容
cleaned_content = "\n".join(cleaned_lines)

# 使用 pygments 渲染为 HTML
html = highlight(cleaned_content, AnsiColorLexer(), HtmlFormatter(full=True, style="monokai"))

# 保存到文件
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved cleaned HTML to output.html")
