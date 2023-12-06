import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quotes"                                                                             # The name of the spider, which each instance of the spider will share the name of

    # URL's to scrape 
    start_urls = ["https://quotes.toscrape.com/page/1/", 
                  "https://quotes.toscrape.com/page/2/"]
    
    def parse(self, response):                                                                  # Funcion called every crawled web page. The response parameter will contain the web site response.



        for quote in response.xpath("//div[@class='quote']"):                                           # For each quote element in the current page...



            text = quote.xpath(".//span[@class='text']/text()").get()                                   # Extract the quote text as a string.

            author = quote.xpath(".//small[@class='author']/text()").get()	                            # Extract the author name as a string.

            tags = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()                 # Extract the quote tags as a list of strings.



            yield {'text': text, 'author': author, 'tags': tags}                                        # Return extracted data as a Python dict.



        next_page = response.xpath("//li[@class='next']/a/@href").get()                                 # Extract next page link as a string.



        if next_page:	                                                                                # If next page is not None, that is, if we have a next page to visit...

            yield response.follow(next_page, callback=self.parse)                                       # Follow the next page link. Return the next page response object.