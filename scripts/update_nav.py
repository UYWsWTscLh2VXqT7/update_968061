import json
import re
import requests
from datetime import datetime
import ast

HISTORY_FILE = "../data/history.json"
#JS_URL = "https://www.stockq.org/funds/fund/jpmorgan/js/J015_nav.js"
URL = "https://www.moneydj.com/funddj/bcd/BCDNavList.djbcd?a=jfz57"

# 在线获取JS文件内容
resp = requests.get(URL)
resp.encoding = "utf-8"
line = resp.text.strip()

try:
    date_part, nav_part = line.split(' ', 1)
except ValueError:
    raise ValueError("❌ 数据格式异常，无法拆分日期和净值")

date_strs = date_part.split(',')
nav_strs = nav_part.split(',')

# 构造 date → nav 映射
nav_map = {}
for d, v in zip(date_strs, nav_strs):
    try:
        date_fmt = datetime.strptime(d.strip(), "%Y%m%d").strftime("%Y-%m-%d")
        nav_map[date_fmt] = float(v.strip())
    except Exception as e:
        print(f"⚠️ 跳过无法解析的项: {d} -> {v} ({e})")

print(f"✅ 成功解析 {len(nav_map)} 条净值数据")

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
