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
    # 去除 spawn 行和 Ctrl+C 标志
    if "spawn qdii-value" in line:
        continue
    if "^C" in line or "\x03" in line:
        continue
    # 去除控制码标题行，如 ?25l ... 中文标题
    if "?25" in line and re.search(r'[\u4e00-\u9fa5]', line):
        continue
    # 去除基金估值更新提示相关行（包含“更新”关键词）
    if "更新" in line:
        continue
    # 过滤纯控制字符行
    if re.fullmatch(r'\x1b\[[0-9;?]*[a-zA-Z]', line.strip()):
        continue
    line = line.rstrip()
    cleaned_lines.append(line)

cleaned_content = "\n".join(cleaned_lines)

# 生成高亮 HTML
html_body = highlight(cleaned_content, AnsiColorLexer(), HtmlFormatter(style="monokai"))

# 加入Bootstrap和自定义标题
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>基金估值 - 摩根太平洋科技基金（968061）</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
<style>
  body {{
    background-color: #111;
    color: white;
    font-family: monospace;
    padding: 1rem;
  }}
  pre {{
    white-space: pre-wrap;
    word-break: break-word;
  }}
</style>
</head>
<body>
<div class="container">
  <h1 class="mb-4 text-center">摩根太平洋科技基金（968061）</h1>
  <div class="bg-dark rounded p-3">
    {html_body}
  </div>
</div>
</body>
</html>
"""

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved responsive bootstrap output.html")
