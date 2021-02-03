import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from pashabank.items import Article
from itemloaders.processors import TakeFirst


class PashaSpider(scrapy.Spider):
    name = 'pasha'
    allowed_domains = ['pashabank.com.tr']
    start_urls = ['https://www.pashabank.com.tr/tr/haberler/haber-liste/Haberler/91/0/0']

    def parse(self, response):
        articles = response.xpath('//ul[@class="haberlerIconList"]/li')
        for article in articles:
            link = article.xpath('.//a/@href').get()
            date = article.xpath('.//i//text()').get()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

        next_pages = response.xpath('//span[@class="pagerNumbersContainer"]/a/@href').getall()
        yield from response.follow_all(next_pages, self.parse)

    def parse_article(self, response, date):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="contentArea"]//h1//text()').get()
        content = " ".join(response.xpath('//div[@class="contentPageContentText"]//text()').getall()).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()

