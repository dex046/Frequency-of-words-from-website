# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="dwx"
__mtime__ = '2016/10/12  11:39'
"""
import scrapy
from scrapy.selector import Selector

class FotoroomSpider(scrapy.Spider):
    name = "Fotoroomarticle"
    allowed_domains = ["fotoroom.co"]
    start_urls = (
        'http://fotoroom.co',
    )

    def parse(self, response):
        sel = Selector(response)
        link = 'http://fotoroom.co/page/'
        #print sel
        for index in xrange(20):
            yield scrapy.Request(link+str(index+1), callback=self.parseSubclass)

    def parseSubclass(self, response):
        sel = Selector(response)
        # = sel.xpath('//article/h2/a')
        subClass2 = sel.xpath('//article/header/h1/a')
        # for sub in subClass1:
        #     name = sub.xpath('text()').extract()[0]
        #     link = sub.xpath('@href').extract()[0]
        #     print name, link
        #     yield scrapy.Request(link, callback=self.parseContent, meta={'name': name})

        for sub in subClass2:
            name = sub.xpath('text()').extract()[0]
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
        detai = sel.xpath('//article/p//text()').extract()
        for con in detai:
            content += con + '\n'
        fileClass.write(content)
        fileClass.flush()
        fileClass.close()




