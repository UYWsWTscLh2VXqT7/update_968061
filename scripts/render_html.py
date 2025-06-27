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

# 加载历史估值数据
try:
    with open("../data/history.json", encoding="utf-8") as f:
        history_data = json.load(f)
except FileNotFoundError:
    history_data = []


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
  <title>摩根太平洋科技基金（968061）估值</title>
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
      padding: 0.5rem;
      overflow-x: auto;  /* 防止横向溢出 */
    }}
  </style>
  
</head>
<body>
  <div class="container">
    <div class="table-wrapper shadow rounded p-3">
    <p class="text-muted mb-1" style="font-size: 0.7rem;">摩根太平洋科技（968061）估值</p>
    <p class="text-muted mb-1" style="font-size: 0.7rem;">更新于 {update_time}</p>
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
    """
    
html += f"""
        <tr class="fw-bold">
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
# === 净值误差统计 ===
errors = []
for entry in history_data:
    estimate = entry.get("total_percent")
    nav = entry.get("nav_change_pct")
    try:
        est_val = float(estimate)
        nav_val = float(nav)
        if nav_val != 0:
            error_pct = abs(est_val - nav_val) / abs(nav_val) * 100
            errors.append(error_pct)
    except (TypeError, ValueError):
        continue

mean_error_text = f"{round(sum(errors) / len(errors), 2)}%" if errors else "—"

# === 预测成功率统计 ===
success = 0
fail = 0

for entry in history_data:
    est = entry.get("total_percent")
    nav = entry.get("nav_change_pct")
    try:
        est_val = float(est)
        nav_val = float(nav)
        if est_val == 0 or nav_val == 0:
            continue  # 不计入
        if (est_val > 0 and nav_val > 0) or (est_val < 0 and nav_val < 0):
            success += 1
        else:
            fail += 1
    except (TypeError, ValueError):
        continue

total_cases = success + fail
if total_cases > 0:
    accuracy_pct = round(success / total_cases * 100, 2)
    accuracy_text = f"{accuracy_pct:.2f}%"
else:
    accuracy_text = "—"


html += f"""
      </tbody>
    </table>
    <p class="text-muted mb-1 text-end" style="font-size: 0.7rem;">持仓截至 2025-05-31</p>
    </div>
    <div class="table-wrapper shadow rounded p-3 mt-4">
      <p class="text-muted mb-1" style="font-size: 0.7rem;">历史估值</p>
      <p class="text-muted mb-1" style="font-size: 0.7rem;">平均误差 {mean_error_text}，涨跌正确率 {accuracy_text}</p>
      <table class="table custom-table">
        <thead>
          <tr>
            <th>日期</th>
            <th class="text-end">估值</th>
            <th class="text-end">净值</th>
          </tr>
        </thead>
        <tbody>
"""

for record in reversed(history_data[-30:]):  # 显示最近30天
    date = record["date"]
    val = float(record["total_percent"])
    nav_change_raw = record.get("nav_change_pct", 0.0)
    # 判断是否为数字，否则直接展示原文
    try:
        nav_change_pct_val = float(nav_change_raw)
        nav_change_pct = f"{nav_change_pct_val:.2f}%"
        nav_color = "text-danger" if nav_change_pct_val > 0 else "text-success" if nav_change_pct_val < 0 else "text-muted"
    except (ValueError, TypeError):
        nav_change_pct = str(nav_change_raw)
        nav_color = ""  # 文字时不加颜色
    color = "text-danger" if val > 0 else "text-success" if val < 0 else "text-muted"
    html += f"""
          <tr>
            <td>{date}</td>
            <td class="text-end {color}">{val:.2f}%</td>
            <td class="text-end {nav_color}">{nav_change_pct}</td>
          </tr>
    """

html += """
        </tbody>
      </table>
      <p class="text-muted mb-1 text-end" style="font-size: 0.7rem;">净值由美元换算后会有些许出入</p>
  </div>
      <div class="footer text-muted mt-5 text-center" style="font-size: 0.7rem;">
      <p><a href="https://github.com/UYWsWTscLh2VXqT7/update_968061" target="_blank">开源地址</a>，powered by <a href="https://github.com/xiaopc/qdii-value" target="_blank">qdii-value</a></p>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 已保存 index.html")
