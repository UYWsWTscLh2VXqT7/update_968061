import sys
from pygments import highlight
from pygments.lexers.special import TextLexer
from pygments.formatters import HtmlFormatter
from pygments_ansi_color.lexer import AnsiColorLexer

with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 解析 ANSI 颜色转为 HTML
html = highlight(content, AnsiColorLexer(), HtmlFormatter(full=True, style="monokai"))

# 输出 HTML 文件
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved output.html")
