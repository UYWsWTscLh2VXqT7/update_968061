import sys
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_ansi_color import AnsiColorLexer

# 读取 output.txt
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 清洗逻辑改进
lines = content.splitlines()
cleaned_lines = []

for line in lines:
    # 跳过常见杂项行
    if line.strip() in ["^C", ""]:
        continue
    if line.startswith("spawn qdii-value"):
        continue
    if re.match(r'^\x1b\[[0-9;]*[a-zA-Z]', line):
        continue
    # 不直接去除带 \x1b 的整行，以防止误删有用内容
    cleaned_lines.append(line)

# 合并回 ANSI 内容
cleaned_content = "\n".join(cleaned_lines)

# ANSI 高亮渲染
html = highlight(cleaned_content, AnsiColorLexer(), HtmlFormatter(full=True, style="monokai"))

# 保存 HTML
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved output.html")
