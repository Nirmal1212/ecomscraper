# -*- coding: utf-8 -*-
import scrapy
site = "http://www.amazon.in"

class AmazonSpider(scrapy.Spider):
	name = "amazon"
	allowed_domains = ["www.amazon.in"]
	start_urls = [
			# 'http://www.amazon.in/gp/site-directory/',
			# 'http://www.amazon.in/gp/search/other/ref=lp_1968120031_sa_p_89?rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968120031&bbn=1968120031&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1499164967'
			'http://www.amazon.in/s/ref=sr_in_-2_p_89_2?fst=as%3Aoff&rh=n%3A976392031%2Cn%3A%21976393031%2Cn%3A1375424031%2Cp_89%3AApple&bbn=1375424031&ie=UTF8&qid=1499165997&rnid=3837712031'			
			]

	# def parse(self,response):
	def parse1(self, response):
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


	# def parse(self,response):
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
		

	def parse(self,response):
	# def parseProducts(self,response):
		q = '//li[contains(@id,"result_")]'
		for i in response.xpath(q):
			title = ''.join(i.xpath('.//h2/text()').extract())
			sp = ''.join(i.xpath('.//span[contains(@class,"s-price")]/text()').extract())
			mp = ''.join(i.xpath('.//span[contains(@class,"a-text-strike")]/text()').extract())
			purl = ''.join(i.xpath('.//span[contains(@class,"s-price")]/../@href').extract())
			imgurl = ''.join(i.xpath('.//img[contains(@class,"s-access-image")]/@src').extract())
			yield { "title" : title, "sp" : sp, "mrp" : mp, "pdp": purl, "img":imgurl}
		paginate_next = response.xpath('//span[@class="pagnLink"]/a/@href').extract()
		paginate_max = response.xpath('//span[@class="pagnDisabled"]/text()').extract()


	# def parse(self,response):
	def parseBrandsPages(self,response):
		global site
		q = '//span[@class="pagnLink"]/a/@href'
		brands = response.xpath(q).extract()
		self.logger.debug('parsed the brands pages ')
		# self.logger.debug(brands)
		brand_pages = [ site+i for i in list(set(brands))]
		yield {"brand_pages" : brand_pages}


	# def parse(self,response):
	def parseBrands(self,response):
		global site
		q = '//span[@class="refinementLink"]'
		self.logger.debug('parsing the brands in the page')
		for i in response.xpath(q):
			url = site+''.join(i.xpath('../@href').extract())
			name = ''.join(i.xpath('./text()').extract())
			cnt = ''.join(i.xpath('./following-sibling::span/text()').extract())[2:-1]
			# print url,name,cnt
			yield { "url":url, "brand":name, "count":cnt}