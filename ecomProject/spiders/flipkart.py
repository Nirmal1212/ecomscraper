# -*- coding: utf-8 -*-
import scrapy


class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["www.flipkart.com"]
    start_urls = (
        'http://www.www.flipkart.com/',
    )

    def parse(self, response):
        pass
