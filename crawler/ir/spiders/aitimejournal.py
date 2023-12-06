import scrapy

class AITimeJournalSpider(scrapy.Spider):
    name = 'aitimejournal'
    start_urls = ['https://www.aitimejournal.com/journal/']

    

    def parse(self, response):
        # Extract information from the main page
        categories = response.xpath('.//div[@class="ast-post-format- blog-layout-1 ast-no-date-box"]')

        for category in categories:
            category_link = category.xpath('.//div[@class="post-thumb-img-content post-thumb"]/a/@href').get()
            print("YAAAAAAAAAAAAAAAAAAAAAAAAAAS")
            print(category_link)
            yield {"link" : category_link}

        
        
        next_page = response.xpath('.//a[@class="next page-numbers"]/@href').extract_first()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            print("NO MORE PAGES")



