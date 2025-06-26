import json
from datetime import datetime
from qdii_value.confs import Config
from qdii_value import processing

# 读取 JSON 配置
with open("968061.json", "r", encoding="utf-8") as f:
    conf = json.load(f)

c = Config(conf)
equities, summary = processing.fetch(c.data['equities'])

title = f"{conf.get('_name', '摩根太平洋科技估值')}（{conf.get('_id', '')}）"
last_update = summary["last_update"].strftime("%Y-%m-%d %H:%M:%S")
total_percent = summary["total_percent"]
total_color = "red" if total_percent > 0 else "green"

# 生成 HTML
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ padding: 2em; font-family: sans-serif; }}
    .red {{ color: red; }}
    .green {{ color: green; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 0.5em; border-bottom: 1px solid #ccc; }}
  </style>
</head>
<body>
  <h2>{title}</h2>
  <p>更新时间：{last_update}</p>
  <p>估值涨跌幅：<span class="{total_color}">{total_percent:.2%}</span></p>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>股票代码</th>
        <th>名称</th>
        <th>最新价格</th>
        <th>涨跌幅</th>
      </tr>
    </thead>
    <tbody>
"""

for eq in equities:
    pct = eq["change_percent"]
    color = "red" if pct > 0 else "green"
    html += f"""<tr>
      <td>{eq['code']}</td>
      <td>{eq['name']}</td>
      <td>{eq['last']}</td>
      <td class="{color}">{pct:.2%}</td>
    </tr>"""

html += """
    </tbody>
  </table>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Saved index.html")
