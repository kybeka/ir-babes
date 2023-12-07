import scrapy

class LinksVidhyaSpider(scrapy.Spider):
    # Spider name, used to run the spider in the terminal
    name = 'vidhya_links'
    
    # Starting URL for the spider
    start_urls = ['https://www.analyticsvidhya.com/blog-archive/']

    def parse(self, response):
        # Extract information from the main page
        articles = response.xpath('.//div[@class="list-card-content"]')

        # Loop through each article and extract the link
        for article in articles:
            article_link = article.xpath('.//a/@href').extract_first()
            yield {"link": article_link}

        # Extract the link for the next page
        next_page = response.xpath('.//a[@class="next page-numbers"]/@href').extract_first()

        # Check if there is a next page
        if next_page:
            # Make a scrapy request for the next page and specify the callback function
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            # Print a message when there are no more pages
            print("NO MORE PAGES")

# To run this spider, use the following command in the terminal:
# PYTHONDONTWRITEBYTECODE=1 scrapy crawl vidhya_links -o ../crawled/links/links_vidhya.jsonl
