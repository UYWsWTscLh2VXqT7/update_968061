import sys
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_ansi_color import AnsiColorLexer

with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()
    
# 清理掉开头 spawn 和控制字符等杂项
cleaned_lines = []
for line in content.splitlines():
    if line.startswith("spawn ") or line.strip() == "^C":
        continue
    if any(x in line for x in ["25h", "25?", "\x1b"]):  # 控制码或转义字符
        continue
    cleaned_lines.append(line)

content = "\n".join(cleaned_lines)


# 高亮 ANSI 彩色内容
html = highlight(content, AnsiColorLexer(), HtmlFormatter(full=True, style="monokai"))

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved output.html")
