import json
import re
import requests
from datetime import datetime
import ast

HISTORY_FILE = "../data/history.json"
JS_URL = "https://www.stockq.org/funds/fund/jpmorgan/js/J015_nav.js"

# 在线获取JS文件内容
resp = requests.get(JS_URL)
resp.encoding = "utf-8"
js_code = resp.text

# 正则提取 data1M 数组的内容
pattern = re.compile(r"var\s+data1M\s*=\s*google\.visualization\.arrayToDataTable\(\s*(\[[\s\S]*?\])\s*\);")

match = pattern.search(js_code)
if not match:
    print("❌ 没找到 data1M 数组")
    exit(1)

array_text = match.group(1)

# 替换 new Date('May 29, 2025') 为 '2025-05-29'
def replace_date(m):
    date_str = m.group(1)
    dt = datetime.strptime(date_str, "%b %d, %Y")
    return f"'{dt.strftime('%Y-%m-%d')}'"

array_text = re.sub(r"new Date\('([^']+)'\)", replace_date, array_text)

# 解析成python列表
try:
    data_list = ast.literal_eval(array_text)
except Exception as e:
    print("❌ 解析JS数组失败:", e)
    exit(1)

# 去除表头
header = data_list.pop(0)

# 构造日期->净值映射
nav_map = {}
for row in data_list:
    if len(row) < 2:
        continue
    date_str = row[0]
    price = row[1]
    if isinstance(date_str, str) and (isinstance(price, float) or isinstance(price, int)):
        nav_map[date_str] = float(price)

print(f"✅ 成功解析data1M，共{len(nav_map)}条净值数据")

# 读取历史文件
with open(HISTORY_FILE, encoding="utf-8") as f:
    history = json.load(f)

# 计算涨跌幅
sorted_dates = sorted(nav_map.keys())
prev_nav = None
nav_change_map = {}
for date in sorted_dates:
    nav = nav_map[date]
    if prev_nav is None:
        nav_change_map[date] = 0.0
    else:
        nav_change_map[date] = round((nav - prev_nav) / prev_nav * 100, 4)
    prev_nav = nav

# 更新历史数据
updated = False
for entry in history:
    date = entry.get("date")
    if not date:
        continue

    if date in nav_map:
        new_nav = str(nav_map[date])
        new_change = nav_change_map.get(date, 0.0)

        old_nav = entry.get("nav")
        old_change = entry.get("nav_change_pct")

        if old_nav in (None, "", "尚未公布") or old_change is None:
            entry["nav"] = new_nav
            entry["nav_change_pct"] = new_change
            updated = True
            print(f"🟢 更新 {date}: 净值 {old_nav} → {new_nav}, 涨跌幅 → {new_change}%")
        else:
            print(f"🔵 跳过 {date}: 已有净值 {old_nav} 和涨跌幅 {old_change}")
    else:
        if "nav" not in entry or entry["nav"] == "":
            entry["nav"] = "尚未公布"
            updated = True
            print(f"⚪ 未找到 {date} 的净值，设为 尚未公布")
        if "nav_change_pct" not in entry or entry["nav_change_pct"] is None:
            entry["nav_change_pct"] = "暂未公布"
            updated = True

if updated:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print("✅ 已写入更新后的 history.json")
else:
    print("ℹ️ 无需更新，所有历史净值和涨跌幅已存在或未公布")
