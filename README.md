<h3>简介</h3>
自动获取最新 QDII 基金实时估值、历史估值、历史净值、估值平均误差以及估值涨跌预测正确率，并推送到网页中。

QDII 基金估值程序由 https://github.com/xiaopc/qdii-value 提供，非常感谢原作者的付出。

暂时只提供 968061 的实时和历史估值，需要其他 QDII 基金数据的，可以 fork 或 download 项目后修改 json 配置文件以及对应的 python 脚本，详见[项目架构](#项目架构)和[使用](#使用)章节。若无网页需求，亦可直接使用原作者的项目，在本地查看数据。

<h3>Demo</h3>

<a>https://q.599254.xyz</a>

<h3>ToDo</h3>

- [x] 增加历史估值
- [x] 增加历史净值
- [x] 增加估值准确度统计
- [x] 完善 json 获取文档
- [x] 完善其他文档

<h3>项目架构</h3>

```
.
├── .github
│   └── workflows
│       ├── history.yml
│       ├── nav.yml
│       └── update.yml
├── data
│   ├── history.json
│   └── index.html
└── scripts
    ├── 968061.json
    ├── record_history.py
    ├── render_html.py
    └── update_nav.py
```

- history.yml：Actions 脚本，调用 record_history.py
- nav.yml：Actions 脚本，调用 update_nav.py
- update.yml：核心 Actions 脚本，调用 qdii-value 读取实时估值，并调用 render_html.py 写入 index.html
- history.json：存储历史估值涨跌幅、历史净值涨跌幅
- index.html：核心网页，由 render_html.py 生成
- 968061.json：基金配置文件，供 qdii-value 读取，主要存储持仓代码、占比、数据源
- record_history.py：记录基金里所有投资股票闭市后的最终估值。对于 968061，是北京时间 04:00 全部闭市
- render_html.py：核心脚本，读取和展示实时估值涨跌幅、历史净值涨跌幅，计算估值平均误差、估值涨跌预测正确率
- update_nav.py：更新基金公布的净值，968061 大约是北京时间 11~13 点更新

<h3>使用</h3>

- 本项目面向 GitHub Actions，若你计划本地部署，请自行调整 yml 为本地脚本和 cron 语法
- 需首先通过 qdii-value 获取基金 json 配置文件，详见 https://github.com/xiaopc/qdii-value
- 修改 update_nav.py 中的数据源
- 根据你希望查看的基金的闭市时间，修改 record_history.py 的定时时间

<h3>维护说明</h3>

本项目的核心功能并非本人开发。附加功能由本人开发，已完成本人的需求，因此在本 README 完成后将进入维护期，不再更新功能。后须将视脚本运行情况修复 bug。

核心功能：获取实时估值，是直接使用 https://github.com/xiaopc/qdii-value 提供的 python 程序获取。本人未对 qdii-value 项目源代码进行任何修改，亦未做出任何贡献。若本项目对您有帮助，请您赞助和支持 qdii-value 原作者。

附加功能，包括：估值实时更新和展示的网页、历史估值、历史净值、估值误差、涨跌正确率等。

可用性评估：<a>https://q.599254.xyz</a> 可持续更新和使用，依赖于以下条件：

- 域名在有效期内
- Clouflare 提供的免费 Pages 托管服务
- GitHub Actions 提供的免费脚本定时运行服务
- 汇丰银行、Google Finance 提供的数据源接口。你也可以在配置基金 json 文件时修改数据源

除以上条件不满足或不可抗力外，<a>https://q.599254.xyz</a> 应当持续可用。