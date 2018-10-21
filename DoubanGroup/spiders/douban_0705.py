#coding=utf-8

'''
1. 添加了cookies 和 headers 已登录的，解决访问url 403 问题；
2. 通过nextpage 实现翻页并提取href问题；
3. 判断nextpage is none 时的报错问题；

'''

from pandas import DataFrame,Series
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request




import scrapy

cookies = {'bid':'WBo17bCfi68',
'gr_user_id':'3c0bba1c-fa2e-45b5-b0b0-24b74c4194e1',
'viewed':'"26274202_1477390"',
'll':'"108296"',
'_vwo_uuid_v2':'5D02956A2C919E57699E167ECB7A3CCB|97442f40ee765dfb21691f1d149b2d93',
'ps':'y',
'_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1499306992%2C%22https%3A%2F%2Fwww.google.co.jp%2F%22%5D',
'ap':'1',
'__ads_session':'iQxwuyvE7wi94uUUQwA=',
'ue':'"asuna12@163.com"',
'dbcl2':'"152282565:JibncIl3RrA"',
'ck':'IzLW',
'__utmt':'1',
'_pk_id.100001.8cb4':'4d0686b07eb464a7.1498015140.10.1499311420.1499304324.',
'_pk_ses.100001.8cb4':'*',
'push_noty_num':'0',
'push_doumail_num':'0',
'__utma':'30149280.131723740.1498015141.1499303298.1499306992.13',
'__utmb':'30149280.35.7.1499311420199',
'__utmc':'30149280',}
headers = {'Connection':'keep-alive',
'Cache-Control':'max-age=0',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'https://www.douban.com/accounts/login?source=group',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
'Cookie':'bid=WBo17bCfi68; gr_user_id=3c0bba1c-fa2e-45b5-b0b0-24b74c4194e1; viewed="26274202_1477390"; ll="108296"; _vwo_uuid_v2=5D02956A2C919E57699E167ECB7A3CCB|97442f40ee765dfb21691f1d149b2d93; ps=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1499306992%2C%22https%3A%2F%2Fwww.google.co.jp%2F%22%5D; ap=1; __ads_session=iQxwuyvE7wi94uUUQwA=; ue="asuna12@163.com"; dbcl2="152282565:JibncIl3RrA"; ck=IzLW; __utmt=1; _pk_id.100001.8cb4=4d0686b07eb464a7.1498015140.10.1499311426.1499304324.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.131723740.1498015141.1499303298.1499306992.13; __utmb=30149280.40.7.1499311426201; __utmc=30149280; __utmz=30149280.1499303298.12.12.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.15228',}
class DoubanSpider(scrapy.Spider):
    name = 'douban0705'

    def start_requests(self):
        urls =['https://www.douban.com/group/antitag/discussion?start=0']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,cookies= cookies,headers=headers)

    def parse(self, response):
        s = response.css('table.olt')
        for detail in s.css('td.title'):
            theme_link = detail.css('td.title a::attr(href)').extract_first()
            print(theme_link)

        # 通过next_page 来翻页
        for next in response.css('div.paginator'):
            next_page = next.css('span.next a::attr(href)').extract_first()
            print(next_page)
            if next_page is not None:
                yield scrapy.Request(url=next_page,callback=self.parse,cookies=cookies,headers=headers)


    def parse_detail(self,response):
        pass


