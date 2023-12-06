import scrapy

class AINewsSpider(scrapy.Spider):
    name = 'link_spider_ai'
    start_urls = ['https://www.artificialintelligence-news.com/#']

    def parse(self, response):
        # Extract information from the main page
        categories = response.xpath('//*[@id="main-nav"]/li[2]/ul/li')
        for category in categories:
            category_link = category.xpath('.//a/@href').get()
            yield {"link" : category_link}
            #For the sub-menus
            # category_kid = category.xpath('.//ul/li')
            # if category_kid:
            #     for category_kid_mini in category_kid:
            #         category_kid_link = category_kid_mini.xpath('.//a/@href').get()
            #         yield {"link" : category_kid_link}

            
