import scrapy
from reddit.items import RedditItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import datetime
import re
from scrapy.http.request import Request
from reddit.spiders import json_parser


    
class RedditSpider(scrapy.Spider):
    name = "post"
    start_urls = ['https://old.reddit.com/r/space/top']

    def parse(self, response):

        def format_comment(x):
            res = int(re.sub("[^0-9]", "", x))
            return res

        next_selector = response.xpath('//span[@class="next-button"]/a/@href')

        for p in response.xpath('//div[@id="siteTable"]/div[contains(@class, "thing")]'):
            l = ItemLoader(item=RedditItem(), selector=p)
            l.add_xpath('title', ['.//a[@class="title may-blank "]/text()', './/a[@class="title may-blank outbound"]/text()'], MapCompose(str.strip, str.title))
            l.add_xpath('user','.//p[@class="tagline "]/a[1]/text()')
            l.add_xpath('upvotes','.//div[@class="score likes"]/@title', MapCompose(int))
            #l.add_xpath('upvotes','.//div[@class="_23h0-EcaBUorIHC-JZyh6J"]//div[@id="vote-arrows-t3_ybmvbx"]', MapCompose(int))
            
            
            #l.add_xpath('comments','.//a[contains(@data-event-action, "comments")]/text()', MapCompose(lambda x:format_comment(x)))
            l.add_xpath('subreddit', './/p[@class="tagline "]/a[2]/text()')
            l.add_xpath('content_link', './/a[contains(@data-event-action, "title")]/@href')
            l.add_xpath('awards', ['.//a[@class="awarding-link"]/@data-count', './/a[@class="awarding-show-more-link"]/text()'], MapCompose(lambda x: format_comment(x)))
            l.add_xpath('time', './/time/@datetime')
            yield l.load_item()

        for url in next_selector.extract():
            yield Request(url, callback=self.parse)


