# -*- coding: utf-8 -*-
import logging
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class WsmCrawlerPipeline(object):
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger()

    @classmethod
    def from_settings(cls, settings):
        db = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=False,
        )
        return cls(db)

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        sql = ''.join([
            "insert into fictions(",
            "   title, author, content, publish_year,",
            "   category, size, finished, cover_url",
            ") values {}".format((
                self.db.escape(item['title']),
                self.db.escape(item['author']),
                self.db.escape(item['content']),
                item['publish_year'],
                ','.join(map(
                    self.db.escape,
                    item['category']
                )),
                item['size'],
                1 if item['finished'] else 0,
                self.db.escape(item['cover_url']),
            ))
        ])

        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.logger.debug(e)
            self.db.rollback()

        return item
