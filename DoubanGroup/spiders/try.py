# -*- coding: <utf-8> -*-

from scrapy import Selector
from pandas import DataFrame,Series
import scrapy
from scrapy.selector import Selector
from scrapy import selector
import re
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
    name = 'douban'
    topic_replay_end = []
    def start_requests(self):
        urls =['https://www.douban.com/group/topic/84303073/?start=0']

        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse,cookies= cookies,headers=headers)

    def parse(self, response):
        # s = response.css('div#content')
        s1 = Selector(response)
        title = s1.css('h1::text').extract_first()

        # 解决h1 下无text，但h1.a下有text的问题
        title1 = s1.xpath('//*[@id="content"]/div/div[1]/div[1]/h1//text()').extract_first()
        print(title1)
        # 为了解决报错'NoneType' object has no attribute 'strip' ，加入if not
        if title1 is None:
            title1 = title.strip(' \n')
        print(title1)
        author = s1.css('div.topic-doc h3 span.from a::text').extract_first()
        create_time = s1.css('div.topic-doc h3 span.color-green::text').extract_first()
        article= s1.css('div.topic-content p::text').extract()
# 先将文章中的\r 都去掉，有些单独的'\r' 就变成了空的列表元素：''，再用if 来判断下就好了
        artical_end = []
        for x in  article:
            x1 = x.replace('\r','')
            if x1 != '':
                artical_end.append(x1)
# 将artical_end 列表 转为字符串
        ar =''.join(artical_end)



        ddata = {'title': title1, 'author': author, 'create_time': create_time,'artical_end':ar}
        f = open("/Users/vivi/PycharmProjects/DoubanGroup/%s.txt" % title1, "a")
        print(ddata, file=f)
        f.close()

# replay2 是所有回应
        if s1.xpath('//*[@id="comments"]//text()'):
            replay2 = ''.join(s1.xpath('//*[@id="comments"]//text()').extract())
# replay1 是所有最赞回应

        if s1.xpath('//*[@id="content"]/div/div[1]/ul[1]'):
            replay1 = ''.join(s1.xpath('//*[@id="content"]/div/div[1]/ul[1]//text()').extract())

        if s1.css('ul.topic-reply'):
            topic_replay = s1.css('ul.topic-reply li.clearfix div.bg-img-green h4 a::text,ul.topic-reply li.clearfix div.bg-img-green h4::text,ul.topic-reply li.clearfix p::text').extract()
            for x in topic_replay:
    # 去掉在x左右的空白,\t,\n和\r字符.
                x1 = x.strip(' \t\n\r')
                if x1 !='':
                    self.topic_replay_end.append(x1)
            f = open("/Users/vivi/PycharmProjects/DoubanGroup/%s.txt" % title1, "a")
            print(replay1, file=f)
            print(replay2,file=f)
            f.close()


    # 取出回复的翻页 都在div.paginator 下，当前已经在访问start=0了
            rep_page = s1.css('div.paginator a::attr(href)').extract()
            for next in rep_page:
                print(next)
                if next is not None:
                    yield scrapy.Request(url=next,callback=self.replay,cookies=cookies,headers=headers,meta={'title1':title1})

    def replay(self,response):
        title1 = response.meta['title1']
        s1 = Selector(response)
        topic_replay = s1.css(
            'ul.topic-reply li.clearfix div.bg-img-green h4 a::text,ul.topic-reply li.clearfix div.bg-img-green h4::text,ul.topic-reply li.clearfix p::text').extract()
        for x in topic_replay:
            # 去掉在x左右的空白,\t,\n和\r字符.
            x1 = x.strip(' \t\n\r')
            if x1 != '':
                self.topic_replay_end.append(x1)
        replay2 = ''.join(s1.xpath('//*[@id="comments"]//text()').extract())
        f = open("/Users/vivi/PycharmProjects/DoubanGroup/%s.txt" % title1, "a")
        print(replay2, file=f)
        f.close()






