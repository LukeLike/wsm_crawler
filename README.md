## 工作流
- `pip install -r requirements.txt` 安装依赖包
- 在 items.py 中定义 `item` 的字段（基本不用改现有的内容）
- 在 pipelines.py 中完成将爬取的 `item` 存入数据库的逻辑（基本不用改现有的内容）
- 为了爬取某个网站，在 spiders 文件夹下新建一个 *_spider.py 的文件，完成将网页解析为 `item` 的逻辑
- 在项目目录下用命令行跑 `scrapy shell 想要解析的url`，可以交互式地尝试解析网页的方法，参照 [scrapy 的官方文档](https://doc.scrapy.org/en/latest/topics/shell.html)