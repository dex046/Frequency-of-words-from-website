# -*- coding: utf-8 -*-

#sovle the encode of chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="dwx"
__mtime__ = '2016/10/12  11:39'
"""
import scrapy
from scrapy.selector import Selector

class lenscultureSpider(scrapy.Spider):
    '''
    to create a Spider, you need extends form scrapy.Spider object, and define following three attributes and methods:
    name: id
    start_urls
    parse()
    '''
    name = "lensculture"
    allowed_domains = ["lensculture.com"]
    start_urls = (
        'https://www.lensculture.com/',
    )

    # visual_stories_link = 0
    # fine_art_link = 1
    # documentary_link = 2
    # b_w_link = 3
    # conceptual_link = 4
    # urban_street_link = 5
    # alternative_link = 6
    # portrait_link = 7
    # landscape_link = 8
    # contemporary_link = 9
    # photojournalism_link = 10
    # architecture_link = 11
    # natrue_link = 12
    # still_life_link = 13
    # festivals_link = 14
    # abstract_link = 15
    # interiors_link = 16
    # staged_link = 17

    def parse(self, response):
        link = 'https://www.lensculture.com/explore'
        raw_link = 'https://www.lensculture.com'
        category_id = [21, 1, 8, 13, 10, 17, 7, 3, 4, 15, 2, 6, 14, 11, 16, 18, 19, 20]
        for index_i in xrange(18):
            for index_j in xrange(10):
                link += "?category" + str(category_id[index_i]) + "&page=" + str(index_j + 1)
                yield scrapy.Request(link, callback=self.parseSubclass, meta={'raw_link': raw_link,  'type': 'explore'})

        link = 'https://www.lensculture.com/explore/award-winners/street-photography-awards-2016'
        yield scrapy.Request(link, callback=self.parseSubclass, meta={'raw_link': raw_link, 'type': 'awards'})

    def parseSubclass(self, response):
        type = response.meta["type"]
        if type == "explore":
            raw_link = response.meta["raw_link"]
            sel = Selector(response)
            subClass = sel.xpath('//ul[@class="grid-list category-projects-list"]/li/a')
            for sub in subClass:
                #name = sub.xpath('text()').extract()[0]
                link = raw_link + sub.xpath('@href').extract()[0]
                print link
                yield scrapy.Request(link, callback=self.parseArtproject, meta={'raw_link': raw_link, 'type': 'explore'})

        if type == "awards":
            raw_link = response.meta["raw_link"]
            sel = Selector(response)
            subClass = sel.xpath('//div[@class="report-item grid-list-item"]/a[@class="name"]')
            for sub in subClass:
                # name = sub.xpath('text()').extract()[0]
                link = raw_link + sub.xpath('@href').extract()[0]
                print link
                yield scrapy.Request(link, callback=self.parseArtproject, meta={'raw_link': raw_link, 'type': 'awards'})

    def parseArtproject(self, response):
        type = response.meta["type"]
        if type == "explore":
            raw_link = response.meta["raw_link"]
            sel = Selector(response)
            subClass = sel.xpath('//ul/li/a[@class="title"]')
            for sub in subClass:
                name = sub.xpath('text()').extract()[0]
                link = raw_link + "project" + sub.xpath('@href').extract()[0]
                print name, link
                yield scrapy.Request(link, callback=self.parseContent, meta={'name': name})

        if type == "awards":
            raw_link = response.meta["raw_link"]
            sel = Selector(response)
            subClass = sel.xpath('//div[@class="featured-project-title"]/a')
            for sub in subClass:
                name = sub.xpath('text()').extract()[0]
                link = raw_link + sub.xpath('@href').extract()[0]
                print link
                yield scrapy.Request(link, callback=self.parseContent, meta={'name': name})


    def parseContent(self, response):
        filename = response.meta['name']
        filename = filename.replace(':', '')
        filename = filename.replace('\\', '')
        filename = filename.replace('/', '')
        filename = filename.replace('*', '')
        filename = filename.replace('?', '')
        filename = filename.replace('"', '')
        filename = filename.replace('<', '')
        filename = filename.replace('>', '')
        filename = filename.replace('|', '')

        #print filename
        fileClass = open(filename + ".txt", 'w')
        content = ''
        sel = Selector(response)
        detail = sel.xpath("//div[@class='description-info outer-form hide ']//p[2]/text()").extract()
        print detail
        for con in detail:
            content += con + '\n'
        fileClass.write(content)
        fileClass.flush()





