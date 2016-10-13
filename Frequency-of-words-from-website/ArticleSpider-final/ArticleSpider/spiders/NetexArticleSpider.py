# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="dwx"
__mtime__ = '2016/10/11  11:39'
"""
import scrapy
from scrapy.selector import Selector

class Netexarticle(scrapy.Spider):
    name = "netexarticle"
    allowed_domains = ["netex.nmartproject.net"]
    start_urls = (
        'http://netex.nmartproject.net/',
    )

    def parse(self, response):
        sel = Selector(response)
        link = 'http://netex.nmartproject.net/?s=2016'
        #print sel
        for index in xrange(10):
            yield scrapy.Request(link+"&paged="+str(index+1), callback=self.parseSubclass)

    def parseSubclass(self, response):
        sel = Selector(response)
        # = sel.xpath('//article/h2/a')
        subClass2 = sel.xpath('//article/h2/a')
        # for sub in subClass1:
        #     name = sub.xpath('text()').extract()[0]
        #     link = sub.xpath('@href').extract()[0]
        #     print name, link
        #     yield scrapy.Request(link, callback=self.parseContent, meta={'name': name})

        for sub in subClass2:
            name = sub.xpath('@title').extract()[0]
            link = sub.xpath('@href').extract()[0]
            print name, link
            yield scrapy.Request(link, callback=self.parseContent, meta={'name': name})

    def parseContent(self, response):
        tempfilename = response.meta['name']
        filename = tempfilename.replace(':', '')
        filename = filename.replace('\\', '')
        filename = filename.replace('/', '')
        filename = filename.replace('*', '')
        filename = filename.replace('?', '')
        filename = filename.replace('"', '')
        filename = filename.replace('<', '')
        filename = filename.replace('>', '')
        filename = filename.replace('|', '')

        print filename
        fileClass = open(filename+".txt", 'w')
        content = ''
        sel = Selector(response)
        detai = sel.xpath('//*[@class="entry-content"]/p//text()').extract()
        for con in detai:
            content += con + '\n'
        fileClass.write(content)
        fileClass.flush()
        fileClass.close()




