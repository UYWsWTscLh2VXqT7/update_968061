# record_history.py
import json
from datetime import datetime, timedelta
from qdii_value.confs import Config
from qdii_value import processing
from decimal import Decimal

with open("968061.json", encoding="utf-8") as f:
    conf = json.load(f)

cfg = Config(conf)
_, summary = processing.fetch(cfg.data['equities'])

today = datetime.now().strftime("%Y-%m-%d")
new_record = {
    "date": today,
    "total_percent": float(round(summary["total_percent"], 2))
}


# 追加到历史记录
history_file = "history.json"
try:
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

# 覆盖今天已有的记录（如果重复）
history = [entry for entry in history if entry["date"] != today]
history.append(new_record)

with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

print("✅ 已写入历史估值")
