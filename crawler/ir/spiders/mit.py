from datetime import datetime
import jsonlines
import scrapy
from ..articles import strip_first_paragraph, extract_date_from_url
import re

class MITSpider(scrapy.Spider):

    name = "mit_content"    
    start_urls = []
    with jsonlines.open('../crawled/links/links_mit.jsonl') as f:

        for line in f.iter():
            start_urls.append(line["link"])

    # De-bugging
    # start_urls = [
    #     "https://news.mit.edu/1994/robotuna",
    #     "https://news.mit.edu/2017/miniaturizing-brain-smart-drones-0712",
    #     "https://news.mit.edu/2021/media-advisory-mit-researchers-ai-policy-needed-manage-impacts-build-more-equitable-systems",
    #     "https://news.mit.edu/2023/synthetic-imagery-sets-new-bar-ai-training-efficiency-1120"
    # ]

    def parse(self, response):

        ## first_paragraph: 250 characters
        ## article_title 
        ## author
        ## date published: year/month/day
        ## tags

        ## url of article
        ## image

        #Starting point
        page_body = response.xpath('.//div[@class="page--section--inner"]')

        # Aggregate article url
        article_url = response.url

        # Aggregate article title
        article_title = page_body.xpath('.//span[@itemprop="name headline"]/text()').get()

        # Aggregate article author
        author = page_body.xpath('.//span[@class="news-article--author"]/text()').get()

        # Aggregating the first paragraph
        first_paragraph = ""
        for p in page_body.xpath('.//div[@class="news-article--content--body--inner"]/div/p'):
            # Concatenate the text content of the paragraph
            first_paragraph += p.xpath('string()').get()

        first_paragraph = strip_first_paragraph(first_paragraph)

        # Aggregate date published
        datetime_str = page_body.xpath('//time/@datetime').extract_first()
        # Parse the datetime string into a datetime object
        parsed_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        # Extract year and month in the desired format
        date_published = {"year": int(parsed_datetime.year), "month": int(parsed_datetime.month)}

        # Get tags
        tags = []
        tag_body = response.xpath('.//ul[@class="news-article--topics-list"]/li')
        for t in tag_body:
            tag = t.xpath('.//a/text()').getall()
            tags.extend(tag)

        # Get image
        photo_body = page_body.xpath('.//div[@class="news-article--media--image--file"]')

        # Extract the src attribute of the first image if it exists
        image_src = response.urljoin(photo_body.xpath('.//img/@src').extract_first())


        # Set article_image based on the extracted values
        if image_src:
            article_image = image_src
            # print("Article Image:", article_image)
        else:
            article_image = None
            # print("No article image found.")

        yield{"text": first_paragraph, "title": article_title, "author": author, "date": date_published, "tags": tags, "article_url": article_url, "img_url": article_image}


        #PYTHONDONTWRITEBYTECODE=1 scrapy crawl mit_content -o ../crawled/content/content_mit.jsonl
        





