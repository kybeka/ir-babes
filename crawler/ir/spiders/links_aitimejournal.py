import scrapy

class LinksAITimeJournalSpider(scrapy.Spider):
    # Spider name, used to run the spider in the terminal
    name = 'aitime_links'
    
    # Starting URL for the spider
    start_urls = ['https://www.aitimejournal.com/journal/']

    def parse(self, response):
        # Extract information from the main page
        articles = response.xpath('.//div[@class="ast-post-format- blog-layout-1 ast-no-date-box"]')

        # Loop through each article and extract the link
        for article in articles:
            article_link = article.xpath('.//div[@class="post-thumb-img-content post-thumb"]/a/@href').get()
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
# PYTHONDONTWRITEBYTECODE=1 scrapy crawl aitime_links -o ../crawled/links/links_aitime.jsonl
