import csv
from pathlib import Path
from datetime import datetime

# 配置
INPUT_DIR = Path("public/data")
OUTPUT_HTML = Path("public/index.html")
FUND_CODES = [line.strip() for line in open("scripts/fund_codes.txt") if line.strip()]

def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>QDII基金估值</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>QDII基金最新估值</h1>
    <p class="timestamp">最后更新: {{UPDATE_TIME}}</p>
    <table>
        <tr>
            <th>基金代码</th>
            <th>基金名称</th>
            <th>当前净值</th>
            <th>更新时间</th>
        </tr>
        {{TABLE_ROWS}}
    </table>
</body>
</html>"""

    table_rows = []
    latest_data = []
    
    for code in FUND_CODES:
        csv_file = INPUT_DIR / f"{code}.csv"
        if not csv_file.exists():
            continue
            
        with open(csv_file, newline='') as f:
            last_row = list(csv.reader(f))[-1]  # 获取CSV最后一行
            
        # 假设CSV格式：净值,更新时间,基金名称
        value, update_time, name = last_row
        table_rows.append(f"""
        <tr>
            <td>{code}</td>
            <td>{name}</td>
            <td>{value}</td>
            <td>{update_time}</td>
        </tr>""")
        
        latest_data.append({
            "code": code,
            "name": name,
            "value": value,
            "time": update_time
        })

    # 保存为JSON（供JS动态加载）
    with open(INPUT_DIR / "latest.json", "w") as f:
        json.dump(latest_data, f)

    # 生成HTML
    html = html.replace("{{TABLE_ROWS}}", "\n".join(table_rows))
    html = html.replace("{{UPDATE_TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    OUTPUT_HTML.write_text(html)

if __name__ == "__main__":
    generate_html()
