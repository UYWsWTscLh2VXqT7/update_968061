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

# 处理汇总估值数据
total_weight = f"{summary['total_weight']:.2f}%"
total_percent = summary['total_percent']
today_weight = f"{summary['today_weight']:.2f}%"
today_percent = summary['today_percent']

def colorize(val):
    val = float(val)
    css_class = "text-danger" if val > 0 else "text-success" if val < 0 else "text-muted"
    return f'<span class="{css_class}">{val:.2f}%</span>'

# HTML头部
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title class="text-center">摩根太平洋科技基金（968061）估值</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ padding: 2rem; 
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji",
                 "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    }}
    table{{
      font-size: 0.8rem;
    }}
    /* 去掉表格边框 */
    .custom-table {{
      border: none !important;    /* 去掉表格外边框 */
    }}
    .custom-table th,
    .custom-table td {{
      border: none !important;
    }}
    
    /* 表头去除背景 */
    .custom-table thead th {{
      background-color: white !important;
      font-weight: 600;
    }}
    
    /* 外层容器圆角和阴影 */
    .table-wrapper {{
      background: white;
      box-shadow: 0 8px 16px rgba(0,0,0,0.12);
      border-radius: 8px;
      padding: 1rem;
      overflow-x: auto;  /* 防止横向溢出 */
    }}
  </style>
  
</head>
<body>
  <div class="container">
    <h4 class="mb-3">摩根太平洋科技（968061）估值</h4>
    <div class="table-wrapper shadow rounded p-3">
    <table class="table custom-table">
      <thead class="table-light">
        <tr>
          <th>名称</th>
          <th>仓位</th>
          <th>涨跌幅</th>
        </tr>
      </thead>
      <tbody>
"""

for eq in equities:
    name = eq['name']
    weight = f"{Decimal(eq['weight']):.2f}%"
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
          <td>{name}</td>
          <td class="text-end">{weight}</td>
          <td class="text-end {color}">{percent_str}</td>
        </tr>
        <tr class="fw-bold">
    """
    
html += f"""
        <td>总仓位</td>
        <td class="text-end">{total_weight}</td>
        <td class="text-end {color}">{colorize(total_percent)}</td>
        </tr>
        <tr>
        <td>今日开市</td>
        <td class="text-end">{today_weight}</td>
        <td class="text-end {color}">{colorize(today_percent)}</td>
        </tr>
    """

html += """
      </tbody>
    </table>
    </div>
    <div class="footer text-muted mt-5 text-center" style="font-size: 0.7rem;">
      <p>估值更新于 {update_time}<br>持仓截至 2025-05-31（摩根仅公开前 10 仓位）</p>
      <p><a href="https://github.com/UYWsWTscLh2VXqT7/update_968061" target="_blank">开源地址</a>，powered by <a href="https://github.com/xiaopc/qdii-value" target="_blank">qdii-value</a></p>
    </div>
  </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 已保存 index.html")
