import scrapy

class VidhyaSpider(scrapy.Spider):
    name = 'vidhya'
    start_urls = ['https://www.analyticsvidhya.com/blog-archive/']

    def parse(self, response):
        # Extract information from the main page
        categories = response.xpath('.//div[@class="list-card-content"]')

        for category in categories:
            category_link = category.xpath('.//a/@href').extract_first()
            yield {"link" : category_link}


        
        
        next_page = response.xpath('.//a[@class="next page-numbers"]/@href').extract_first()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            print("NO MORE PAGES")




