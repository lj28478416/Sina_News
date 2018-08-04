# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaSpiderItem
from ..settings import COOKIES
import re


class SinaspiderSpider(scrapy.Spider):
    name = 'SinaSpider'
    allowed_domains = ["sina.com",'sina.com.cn']
    start_urls = ['http://www.sina.com.cn/']

    def parse(self, response):
        first_lev_node_list = response.xpath("//div[@class='main-nav']/div")[0:5]
        for first_lev_node_ul in first_lev_node_list:
            first_lev_node_ul_list = first_lev_node_ul.xpath("./ul")
            for first_lev_node in first_lev_node_ul_list:
                first_lev_node_name = first_lev_node.xpath("./li/a/b/text()").extract_first()
                second_lev_node_list = first_lev_node.xpath("./li")[1:4]
                for second_lev_node in second_lev_node_list:
                    item = SinaSpiderItem()
                    # num += 1
                    second_lev_node_name = second_lev_node.xpath("./a/text()").extract_first()
                    second_lev_node_url = second_lev_node.xpath("./a/@href").extract_first()
                    if not os.path.exists(first_lev_node_name + "/" + second_lev_node_name):
                        os.makedirs(first_lev_node_name + "/" + second_lev_node_name)
                    item['path'] = first_lev_node_name + "/" + second_lev_node_name
                    # print(num)
                    # print(first_lev_node_name + "/" + second_lev_node_name)
                    # print(item)
                    # num_list.append(item)
                    # print(num_list)
                    # print(item['news_url'])
                    yield scrapy.Request(second_lev_node_url, callback=self.parse_detil, meta={'item1': item},
                                         cookies=COOKIES)
                    # print("PARSE_URL----")

    def parse_detil(self, response):
        # print("PARSE_DETIAL", id(response))
        item = response.meta["item1"]
        shtml_url_list = []
        for news_url in response.xpath("//a/@href").extract():
            if news_url.endswith('.shtml'):
                if news_url.startswith('http:'):
                    news_url= news_url
                else:
                    news_url = 'http:' + news_url
                shtml_url_list.append(news_url)
        for shtml_url in shtml_url_list:
            item['news_url'] = shtml_url
            yield scrapy.Request(shtml_url, callback=self.parse_news, meta={'item2': item}, cookies=COOKIES)
            # yield item

    def parse_news(self, response):
        # print("PARSE_NEWS", response.url)
        item = response.meta["item2"]
        if response.url.startswith('http://english.sina.com/'):
            news_name = response.xpath("//div[@id='artibodyTitle']/h1/text()").extract_first()
            if news_name:
                news_name =re.sub(r'<.*?>', '' , news_name)
                item['news_name'] = news_name
                news_detil = response.xpath("//div[@id='artibody']").extract()[0] if len(response.xpath("//div[@id='artibody']").extract()) else ''
                news_detil = re.sub(r'<.*?>', '', news_detil)
                item['news_detil'] = news_detil
            else:
                item['news_name'] = 'error'
                item['news_detil'] = ''
        else:
            news_name = response.xpath("//h1[@class='main-title']").extract_first()
            if news_name:
                news_name =re.sub(r'<.*?>', '' , news_name)
                item['news_name'] = news_name
                news_detil = response.xpath("//div[@id='artibody']").extract()[0] if len(response.xpath("//div[@id='artibody']").extract()) else ''
                news_detil = re.sub(r'<.*?>', '', news_detil)
                item['news_detil'] = news_detil
            else:
                item['news_name'] = 'error'
                item['news_detil']=''
        # print(news_detil)
        # item['news_detil'] = node_test.xpath("/string()").extract_first()
        yield item
