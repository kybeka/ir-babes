import scrapy
import jsonlines
from ..articles import strip_first_paragraph, convert_date


class AITimesSpider(scrapy.Spider):

    name = "aitimes_content"    
    start_urls = []

    with jsonlines.open('../crawled/links/links_aitimes.jsonl') as f:
        for line in f.iter():
            start_urls.append(line["link"])

    # De-bugging
    # start_urls = [
    #     # "https://www.aitimejournal.com/5-ai-artists-and-their-creative-work/839/",
    #     # "https://www.aitimejournal.com/conversational-ai-in-healthcare/34253/",
    #     # "https://www.aitimejournal.com/top-accounting-companies-for-digital-entrepreneurs-to-watch/44101/",
    #     # "https://www.aitimejournal.com/janne-aas-jakobsen-founder-and-ceo-of-consigli-as-ais-role-in-engineering-and-construction-sustainable-technologies-global-expansion-entrepreneurial-insights-and-technological-in/47249/"
    # ]
    

    def parse(self, response):

        #Starting point
        page_body = response.xpath('.//main[@id="main"]')

        # Aggregate article url
        article_url = response.url

        # Aggregate article title
        article_title = page_body.xpath('.//h1[@class="entry-title"]/text()').get()

        # Aggregate article author
        author = page_body.xpath('.//span[@class="author-name"]/text()').get()


        # Aggregating the first paragraph
        first_paragraph = ""
        for p in page_body.xpath('.//div[@class="entry-content clear"]/p'):
            # Concatenate the text content of the paragraph
            first_paragraph += p.xpath('string()').get()

            # # Check if the paragraph contains an anchor tag
            # anchor_text = p.xpath('.//a/text()').get()

            # if anchor_text:
            #     # Concatenate the text content of the anchor tag
            #     first_paragraph += anchor_text

            # Break the loop if the first paragraph is aggregated
            if first_paragraph:
                break

        first_paragraph = strip_first_paragraph(first_paragraph)

        # Aggregate date published
        date_holder = page_body.xpath('.//div[@class="entry-meta"]/text()').getall()
        if date_holder:
            date_array = date_holder[1].split(" ")[2:]
            date_published = convert_date(date_array)
        else:
            date_published = None


        # Get tags
        tags = []

        # tags
        if (response.xpath('.//span[@class="tags-links"]/a/text()').getall()):
            tags.append(response.xpath('.//span[@class="tags-links"]/a/text()').getall())

        # categories
        if(response.xpath('.//span[@class="cat-links"]/a/text()').getall()):
            categories = []
            categories = response.xpath('.//span[@class="cat-links"]/a/text()').getall()
            tags = tags.extend(categories)
        
        # Flatten the list using list comprehension
        if tags:
            tags = [item for sublist in tags for item in sublist] if isinstance(tags[0], list) else tags

        # Get image
        photo_body = page_body.xpath('.//div[@class="entry-content clear"]')

        # Extract the src attribute of the first image if it exists
        image_src = photo_body.xpath('.//img/@src').extract_first()

        if article_title and author and date_published and first_paragraph:
            yield {"text": first_paragraph, "title": article_title, "author": author, "date": date_published, "tags": tags, "article_url": article_url, "img_url": image_src}


        #PYTHONDONTWRITEBYTECODE=1 scrapy crawl aitimes_content -o ../crawled/content/content_aitimes.jsonl


