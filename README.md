# Tech-Investment-Analyzer (硬科技赛道自动化投研工具)

本项目是一个为“硬科技”（AI/半导体）赛道打造的自动化投研分析工具。


## 核心功能

* **自动化数据抓取**: 稳定抓取36氪"人工智能"板块的最新文章（一次60篇）。
* **自动化热点分析**: 利用 `jieba` 自定义词典，对文章标题和摘要进行中文分词，并自动化统计关键公司（如"英伟达", "OpenAI", "Kimi"）的提及频率，量化市场热度。
* **自动化报告输出**: 一键生成两个核心文件：
    1.  `report.csv`: 市场热点关键词频率报告。
    2.  `detailed_articles.csv`: 包含标题、摘要、链接的原始文章明细。

## 成果展示 (report.csv)

本项目成功抓取并分析了60篇文章，热点分析结果如下：

| Keyword | Frequency |
| :--- | :--- |
| OpenAI | 9 |
| 英伟达 | 3 |
| Anthropic | 1 |
| Sora | 1 |
| NVIDIA | 0 |
| 华为 | 0 |
| 寒武纪 | 0 |
| 中芯国际 | 0 |
| 商汤 | 0 |
| 旷视 | 0 |
| 月之暗面 | 0 |
| Kimi | 0 |

*(注：词频为0代表在抓取的60篇文章中未被提及，但分析器已具备识别能力)*

---

## 核心原理：动态网页API爬取“模板”

本项目解决的核心问题是“JavaScript动态内容加载”的反爬虫机制。`requests` 库拿到的HTML是空壳，内容由JS异步加载。

我们的解决方案是一个可复用的“两步走”API请求模板：

### 1. 侦察：F12网络侦测

* **问题**：直接爬取HTML页面（`.../information/AI/`），返回的源码中不包含文章列表。
* **侦察**：
    1.  打开浏览器“开发者工具”(F12) -> “网络(Network)” -> `Fetch/XHR`。
    2.  滚动页面，发现页面通过 `POST` 请求 `https://gateway.36kr.com/.../flow` 这个API来获取数据。
    3.  直接模拟 `POST` 请求失败，返回 `{"msg": "请求分页回调值不能为空"}`。

### 2. 破局：“硬编码的钥匙”

* **发现“钥匙”**：通过“查看网页源代码”（View Page Source），在原始HTML的一个 `<script>` 标签中，我们找到了 `POST` 请求所必需的“第一把钥匙”—— `pageCallback` 字符串。
* **问题**：这把“钥匙”本身也是服务器动态生成的，`requests` 脚本直接访问会被服务器识破（返回不带钥匙的HTML）。
* **最终方案（稳定模板）**：
    1.  **获取“黄金钥匙”**：我们作为“人”访问一次“查看网页源代码”，将这个初始 `pageCallback` 复制出来，**硬编码**到 `config.py` 文件中。
    2.  **API请求**：脚本启动，加载 `config.py` 中的“黄金钥匙”。
    3.  **数据获取**：使用 `requests.post()` 携带这把“钥匙”访问API，API验证通过，返回了包含30篇文章的**干净JSON数据**。
    4.  **循环获取**：API返回的JSON中，包含了用于请求“下一页”的**新 `pageCallback`**。我们用这把新钥匙，发起第二次请求，获取第2页的30篇文章，实现循环。

### 3. 分析：自定义词典

* **问题**：`jieba` 默认词典不认识“月之暗面”、“Kimi”等AI新词。
* **解决**：创建 `custom_dict.txt` 文件，并通过 `jieba.load_userdict()` 加载，确保分词准确性。

## 技术栈

* **Python 3.10**
* **数据抓取**: `requests` (用于API的POST请求)
* **数据分析**: `pandas` (用于数据清洗和报告生成)
* **中文分词**: `jieba` (并使用了自定义词典 `custom_dict.txt`)
* **数据结构**: `JSON` (用于解析API响应)

## 如何运行

1.  克隆本仓库:
    ```bash
    git clone https://github.com/Tree-pika/Tech-Investment-Analyzer.git
    cd Tech-Investment-Analyzer
    ```
2.  创建并激活Conda环境:
    ```bash
    conda create -n invest-env python=3.10
    conda activate invest-env
    ```
3.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```
4.  运行主程序:
    ```bash
    python main.py
    ```
5.  在文件夹中查看 `report.csv` 和 `detailed_articles.csv` 两个输出文件。