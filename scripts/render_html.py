import json
from decimal import Decimal
from qdii_value.confs import Config
from qdii_value import processing
from datetime import datetime

# 加载配置（json 文件名需与基金代码一致）
with open("968061.json", encoding="utf-8") as f:
    conf = json.load(f)

cfg = Config(conf)
equities, summary = processing.fetch(cfg.data['equities'])

# 获取估值时间
update_time = summary['last_update'].strftime("%Y-%m-%d %H:%M:%S")

# HTML头部
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>摩根太平洋科技基金（968061）估值</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ padding: 2rem; }}
    table {{ font-size: 0.9rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h2 class="mb-3">摩根太平洋科技基金（968061）估值</h2>
    <p class="text-muted">更新于 {update_time}</p>
    <table class="table table-striped table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>代码</th>
          <th>名称</th>
          <th>仓位</th>
          <th>当前价</th>
          <th>涨跌额</th>
          <th>涨跌幅</th>
        </tr>
      </thead>
      <tbody>
"""

for eq in equities:
    code = eq['code']
    name = eq['name']
    weight = f"{Decimal(eq['weight']):.2f}%"
    price = f"{Decimal(eq['last']):.2f}"
    change = f"{Decimal(eq['change']):.2f}"
    percent = float(eq['change_percent'])
    percent_str = f"{percent:.2f}%"

    # 颜色设定
    if percent > 0:
        color = "text-danger"
    elif percent < 0:
        color = "text-success"
    else:
        color = "text-muted"

    html += f"""
        <tr>
          <td>{code}</td>
          <td>{name}</td>
          <td>{weight}</td>
          <td>{price}</td>
          <td>{change}</td>
          <td class="{color}">{percent_str}</td>
        </tr>
    """

html += """
      </tbody>
    </table>
  </div>
</body>
</html>
"""

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 已保存 output.html")
