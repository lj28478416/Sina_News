# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaSpiderPipeline(object):
    def process_item(self, item, spider):
        if item['news_detil']:
            with open(item["path"] + "/" +item['news_name'] + ".txt",'w') as f:
                f.write(item["news_detil"])
        return item
