# TODO: REDO AND NOT SCRAPE FROM IMAGE (articles from 2003 don't have an image)

import scrapy

class LinksMITSpider(scrapy.Spider):
    # Spider name, used to run the spider in the terminal
    name = 'mit_links'
    
    # Starting URL for the spider
    start_urls = ['https://news.mit.edu/topic/artificial-intelligence2']

    def parse(self, response):
        # Extract information from the main page
        articles = response.xpath('.//div[@class="page-term--views--list"]/div[@class="page-term--views--list-item"]/article[@class="term-page--news-article--item"]')

        # Loop through each article and extract the link
        for article in articles:
            link = response.urljoin(article.xpath('.//div/a/@href').extract_first())

            # Yield the link in a dictionary format
            yield {"link": link}

        # Extract the link for the next page
        next_page = response.urljoin(response.xpath('.//a[@rel="next"]/@href').extract_first())

        # Check if there is a next page
        if next_page:
            # Make a scrapy request for the next page and specify the callback function
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            # Print a message when there are no more pages
            print("NO MORE PAGES")
            

# To run this spider, use the following command in the terminal:
# PYTHONDONTWRITEBYTECODE=1 scrapy crawl mit_links -o ../crawled/links/links_mit.jsonl
