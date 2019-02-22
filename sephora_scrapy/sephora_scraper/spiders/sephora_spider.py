from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sephora_scraper.items import SephoraScraperItem
import re

class SephoraCrawlSpider(CrawlSpider):
    name = 'sephoraspider'
    allowed_domains = ['www.sephora.com']
    start_urls = ['https://www.sephora.com/beauty/best-selling-skin-care']
    rules = (
    Rule(LinkExtractor(allow=r'^https?://www.sephora.com/product/.*', restrict_xpaths='//div[@class="css-1s223mm"]/a'),
         callback='parse_item_page',
        ),
    )

def parse_item_page(self, response):
    print("================parse_item_page works!==================")
    item = SephoraScraperItem()
    item['name'] = response.xpath('//span[@class="css-vbpn3b"]/text()').extract()
    item['brand'] = response.xpath('//span[@class="css-a2osvj"]/text()').extract()
    item['price'] = response.xpath('//div[@class="css-14hdny6"]/text()').extract()
    item['ingredients'] = response.xpath('//*[@id="tabpanel2"]/div/text()').extract()
    yield item
