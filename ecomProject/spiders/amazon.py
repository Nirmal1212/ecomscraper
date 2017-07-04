# -*- coding: utf-8 -*-
import scrapy
site = "http://www.amazon.in"

class AmazonSpider(scrapy.Spider):
	name = "amazon"
	allowed_domains = ["www.amazon.in"]
	start_urls = [
			'http://www.amazon.in/gp/site-directory/',
			]

	def parse(self, response):
		q = '//div[contains(@class,"popover-grouping")]//a[contains(@class,"nav_a")]'
		global site

		for i in response.xpath(q):
			d1 = {
			  'url' : site+' '.join(i.xpath('./@href').extract()),
			  'Category': ' '.join(i.xpath('./text()').extract()),
			  'MetaCategory': ' '.join(i.xpath('../../../h2/text()').extract())
			}
			# yield d1
			# url = "http://www.amazon.in/Mens-Tshirts-Polos/b/ref=sd_allcat_sbc_mfashion_tshirts/259-4996162-3224231?ie=UTF8&node=1968120031"
			url = d1['url']
			yield scrapy.Request(url,
                          callback=self.parseCategoryPage,meta={'src':d1})
			# break


	def parseCategoryPage(self, response):
		src = response.meta['src']
		try:
			q = '//span[@class="a-list-item"]/a/span[text() = "See more"]/../@href'
			brand_url = site+response.xpath(q).extract()[1]
			src['brand_url'] = brand_url
			yield src
		except Exception as e:
			# self.logger.debug('Exception occured:: %s',e)
			self.logger.exception(e)
			pass
		

	def parseProducts(self,response):

		pass

	def parseBrandsPaginate(self,response):
		q = '//span[@class="pagnLink"]/a/@href'
		brands = response.xpath(q).extract()
		brands = list(set(brands))
		yield brands