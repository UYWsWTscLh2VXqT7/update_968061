import subprocess
import os
import json
import shutil
from datetime import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# 设置工作目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 复制配置文件
config_dir = "../configs"
for file in os.listdir(config_dir):
    if file.endswith(".json"):
        shutil.copy(os.path.join(config_dir, file), ".")

# 基金代码列表
fund_codes = ["968061"]

# 存储每个基金的原始输出
fund_outputs = {}

for code in fund_codes:
    try:
        # 确保配置文件存在
        if not os.path.exists(f"{code}.json"):
            print(f"警告: {code}.json 配置文件不存在")
            continue
            
        # 运行 qdii-value 并捕获输出
        result = subprocess.run(
            ["qdii-value", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        
        if result.returncode == 0:
            # 保存原始输出
            fund_outputs[code] = result.stdout
            
            # 转换为带样式的HTML
            lexer = get_lexer_by_name("ansi-terminal", stripall=True)
            formatter = HtmlFormatter(
                style="monokai",
                noclasses=True,
                prestyles="font-family: monospace; font-size: 14px; padding: 15px;"
            )
            styled_html = highlight(result.stdout, lexer, formatter)
            
            # 保存HTML文件
            os.makedirs(f"../public/output/{code}", exist_ok=True)
            with open(f"../public/output/{code}/index.html", "w") as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>基金 {code} 估值</title>
                    <style>{formatter.get_style_defs()}</style>
                    <style>
                        body {{ 
                            background-color: #272822; 
                            padding: 20px;
                            margin: 0;
                        }}
                        .container {{
                            max-width: 800px;
                            margin: 0 auto;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <pre>{styled_html}</pre>
                    </div>
                </body>
                </html>
                """)
        else:
            print(f"执行失败: {result.stderr}")
            fund_outputs[code] = f"Error: {result.stderr}"
    except Exception as e:
        print(f"处理 {code} 时出错: {str(e)}")
        fund_outputs[code] = f"Error: {str(e)}"

# 保存原始文本输出（可选）
os.makedirs("../public/output", exist_ok=True)
with open("../public/output/latest.txt", "w") as f:
    for code, output in fund_outputs.items():
        f.write(f"===== 基金 {code} =====\n")
        f.write(output)
        f.write("\n\n")

# 生成主页
update_time = datetime.now().isoformat()
index_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>QDII基金实时估值</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 20px;
        }
        .fund-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .fund-card {
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .fund-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .fund-card h3 {
            margin-top: 0;
            color: #0366d6;
        }
        .last-updated {
            font-size: 0.9em;
            color: #586069;
            text-align: center;
            margin-top: 30px;
        }
        .view-link {
            display: inline-block;
            margin-top: 10px;
            color: #0366d6;
            text-decoration: none;
        }
        .view-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>QDII基金实时估值</h1>
        <p id="update-time">最后更新时间: 加载中...</p>
    </header>
    
    <div class="fund-list">
        <!-- 基金卡片将由JavaScript动态生成 -->
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // 设置更新时间
            document.getElementById('update-time').textContent = 
                `最后更新时间: ${new Date(""" + f'"{update_time}"' + """).toLocaleString()}`;
            
            const fundCodes = """ + json.dumps(fund_codes) + """;
            const container = document.querySelector('.fund-list');
            
            fundCodes.forEach(code => {
                const card = document.createElement('div');
                card.className = 'fund-card';
                card.innerHTML = `
                    <h3>基金 ${code}</h3>
                    <div class="output-preview">
                        <pre style="white-space: pre-wrap; max-height: 200px; overflow: hidden; background: #f6f8fa; padding: 10px; border-radius: 4px;">${""" + f'fund_outputs[code].replace(/</g, "&lt;").replace(/>/g, "&gt;")' + """}</pre>
                    </div>
                    <a href="/output/${code}/" class="view-link">查看完整详情</a>
                `;
                container.appendChild(card);
            });
        });
    </script>
</body>
</html>
"""

with open("../public/index.html", "w") as f:
    f.write(index_html)
