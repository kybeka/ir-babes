import scrapy

class MITSpider(scrapy.Spider):
    name = 'mit'
    start_urls = ['https://news.mit.edu/topic/artificial-intelligence2']

    def parse(self, response):
        # Extract information from the main page
        categories = response.xpath('.//div[@class="page-term--views--list"]/div[@class="page-term--views--list-item"]/article[@class="term-page--news-article--item"]')

        for category in categories:
            link = response.urljoin(category.xpath('.//div/a/@href').extract_first())

            yield {"link" : link}



        next_page = response.urljoin(response.xpath('.//a[@rel="next"]/@href').extract_first())

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            print("NO MORE PAGES")




