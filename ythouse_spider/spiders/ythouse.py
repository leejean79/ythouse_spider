import scrapy
from lxml import etree
from ythouse_spider.spiders.utils import *


class YthouseSpider(scrapy.Spider):
    name = 'ythouse'
    allowed_domains = ['ytbbs.ythouse.com']
    start_urls = ['https://ytbbs.ythouse.com/resoldhome/esf/list?page=1']

    # 直接解析start_urls返回的response
    def parse(self, response):
       #  首页所有二手房的item列表
       item_li = response.xpath('//li[@class="item clearfix"]')

       # 定义一个字典保存每次爬取的字段信息
       temp_dic = {}

       # 遍历每个item提取相关字段
       for item in item_li:
           fields_li = item.xpath('.//p[@ class ="area"]//a/@title').extract()
           # 二手房小区名
           temp_dic['District'] = fields_li[0]
           # 二手房区域
           temp_dic['Region'] = fields_li[1]
           # 二手房具体位置
           temp_dic['Garden'] = item.xpath('.//p[@class="area"]//span[@class="maps"]/text()').extract()[0]
           # 二手房户型
           temp_dic['Layout'] = item.xpath('.//p[@class="detail"]//span/text()').extract()[0]
           # 楼层
           temp_dic['Floor'] = item.xpath('.//p[@class="detail"]//span/text()').extract()[1]
           temp_dic['Floor'] = extract_floor(temp_dic['Floor'])
           # 总楼层
           temp_dic['Total_Floor'] = extract_total_floor(item.xpath('.//p[@class="detail"]//span/text()').extract()[1])
           # 总价
           temp_dic['Price'] = item.xpath('.//div[@class="about-price"]//em/text()').extract()[0]
           # 均价
           temp_dic['Price_PerAverage'] = item.xpath('.//div[@class="about-price"]//p[@class="tag"]/text()').extract_first()
           if temp_dic['Price_PerAverage'] is not None:
                temp_dic['Price_PerAverage'] = extract_aver_price(temp_dic['Price_PerAverage'])
           # 面积
           temp_dic['Size'] = item.xpath('.//span[@class="area-detail_big"]/text()').extract()[0]
           # 建造年份
           temp_dic['Year'] = item.xpath('.//p[@class="detail"]/text()').extract()[2].replace("  ", "").replace("\n", "")
           temp_dic['Year'] = extract_year(temp_dic['Year'])

           yield temp_dic
           # print(temp_dic)

      # 实现翻页：1.提取末页页码2.提取下一页链接3.判读下一页页码是否为与末页相等，不等的话继续爬取
      # 提取末页地址 /resoldhome/esf/list?page=9
       last_page_href =  response.xpath('//span[contains(text(),"末页")]/../@href').extract_first()
       last_page_num = extract_total_page(last_page_href)
       # 提取下一页
       next_page_href = response.xpath('//span[contains(text(),"下一页")]/../@href').extract_first()
       next_page_num = extract_total_page(next_page_href)
       if next_page_num < last_page_num:
           yield scrapy.Request("https://ytbbs.ythouse.com/resoldhome/esf/list?page=" + str(next_page_num), callback = self.parse)
           next_page_num += 1
