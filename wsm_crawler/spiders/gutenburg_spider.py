import time
import requests

import scrapy

from wsm_crawler.items import WsmCrawlerItem

class GutenburgSpider(scrapy.Spider):
    name = "gutenburg"

    start_urls = [
        'http://www.gutenberg.org/browse/titles/{}'.format(
            chr(97+i)
        ) for i in range(26)
    ]

    time_format = '%b %d, %Y'

    def parse(self, response):
        container_body = response.css('.pgdbbytitle')
        title_list = container_body.css('h2 > a')
        language_list = list(map(
            lambda lang: lang.strip().strip('()'),
            response.css('h2::text').extract()
        ))

        # 获取本页英文小说的内容
        for title, lang in zip(title_list, language_list):
            if lang != 'English':
                continue
            yield response.follow(title, callback=self.parse_book)

        # 到达下一页进行爬取，但这个网站似乎把所有结果在一页内给出

    def __word_count(self, text):
        """Return # words in the `text`
        """
        return len(text.split())

    def parse_book(self, response):
        book_item = WsmCrawlerItem()

        # 下载小说文本
        links = response.css('a.link')
        for link in links:
            if link.css('a::text').extract_first() == 'Plain Text UTF-8':
                book_url = link.css('a::attr(href)').extract_first()
                book_response = requests.get('http:'+book_url)
                if book_response.status_code != 200: # 下载不到书则忽略
                    return
                book_item['content'] = book_response.content
                if book_response.encoding:
                    book_item['content'] = book_item['content'].decode(
                        book_response.encoding
                    )
                book_item['content'] = book_item['content'].strip()
                if book_item['content'][0] == '\ufeff':
                    book_item['content'] = book_item['content'][1:]

        # 数小说的英文单词数
        book_item['size'] = self.__word_count(book_item['content'])

        # 从表格中提取信息
        table = response.css('.bibrec tr')
        category_info = []
        for row in table:
            row_name = row.css('th::text').extract_first()

            if row_name == 'Author': # 提取作者信息
                book_item['author'] = ' '.join(
                    row.css('td a::text')
                       .extract_first()
                       .split(',')[0:2][::-1]
                ).strip()
            elif row_name == 'Title': # 提取标题
                book_item['title'] = row.css('td::text').extract_first().strip()
            elif row_name == 'Release\xa0Date': # 提取发布年份
                book_item['publish_year'] = time.strptime(
                    row.css('td::text').extract_first(),
                    self.time_format
                ).tm_year
            elif row_name == 'Subject': # 提取主题 (可能有多个)
                category_info.append(
                    row.css('td a::text').extract_first().strip()
                )

        book_item['category'] = category_info

        # 提取封面图片的 url
        cover_wrapper = response.css('#cover-social-wrapper')
        if cover_wrapper.css('div > div::attr(id)').extract_first() == 'cover':
            book_item['cover_url'] = cover_wrapper.css('#cover > img::attr(src)') \
                                      .extract_first()
        else:
            book_item['cover_url'] = ''

        book_item['finished'] = True
        yield book_item
