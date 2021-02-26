import scrapy

from scrapy.loader import ItemLoader
from ..items import AdyenItem
from itemloaders.processors import TakeFirst


class AdyenSpider(scrapy.Spider):
	name = 'adyen'
	start_urls = ['https://www.adyen.com/blog']

	def parse(self, response):
		post_links = response.xpath(
			'//article/a/@href|//div[@class="col-12 col-sm-6 col-md-4 press-release__overview"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath(
			'//a[@class="story-pagination__button"]/@href|//ul[@class="story-overview-menu"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[contains(@class, "story-text-block")]//text()[normalize-space()]|//div[@class="press-release__text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="story-author"]//time/text()|//span[@class="press-release__details--date"]/text()').get()

		item = ItemLoader(item=AdyenItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
