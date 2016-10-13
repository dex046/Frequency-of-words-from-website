# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="dwx"
__mtime__ = '2016/10/9  11:39'
"""
import scrapy
from scrapy.selector import Selector

class ArtileSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["netex.nmartproject.net"]
    start_urls = (
        'http://netex.nmartproject.net/',
    )

    def parse(self, response):
        link = 'http://netex.nmartproject.net/page/'
        for index in xrange(1):
            yield scrapy.Request(link+str(index+1), callback=self.parseSubclass)


    def parseSubclass(self, response):
        sel = Selector(response)
        subClass = sel.xpath('//article/header/h2/a')
        for sub in subClass:
            name = sub.xpath('text()').extract()[0]
            link = sub.xpath('@href').extract()[0]
            print name,link
            yield scrapy.Request(link, callback=self.parseContent,meta={'name':name})

    def parseContent(self, response):
        filename = response.meta['name']
        fileClass = open('./content/'+filename+".txt",'w')
        content = ''
        sel = Selector(response)
        detai = sel.xpath('//*[@class="entry-content"]/p//text()').extract()
        for con in detai:
            content += con + '\n'
        fileClass.write(content)
        fileClass.flush()
        fileClass.close()



