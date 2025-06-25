import sys
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_ansi_color import AnsiColorLexer

with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 高亮 ANSI 彩色内容
html = highlight(content, AnsiColorLexer(), HtmlFormatter(full=True, style="monokai"))

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved output.html")
