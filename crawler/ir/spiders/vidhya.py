import jsonlines
import scrapy
from ..articles import strip_first_paragraph, extract_date_from_url
import re

class VidhyaSpider(scrapy.Spider):

    name = "vidhya_content"    
    start_urls = []
    with jsonlines.open('../crawled/links/links_vidhya.jsonl') as f:

        for line in f.iter():
            start_urls.append(line["link"])

    # De-bugging
    # start_urls = [
    #     # "https://www.analyticsvidhya.com/blog/2023/12/meet-gemini-googles-answer-to-chatgpt/",
    #     # "https://www.analyticsvidhya.com/blog/2023/12/top-books-to-master-sql-concepts/",
    #     # "https://www.analyticsvidhya.com/blog/2023/12/generative-ai-frameworks/",
    #     # "https://www.analyticsvidhya.com/blog/2023/12/pioneering-data-science-in-latin-america-with-favio-vazquez/"
    # ]

    def parse(self, response):
        #Starting point
        page_body = response.xpath('.//main[@class="w-100 float-left main-row"]')

        # Aggregate article url
        article_url = response.url

        # Aggregate article title
        article_title = page_body.xpath('.//div[@class="col-md-9 pl-0"]/h1/text()').get()

        # Aggregate article author
        author = page_body.xpath('.//div[@class="publish-info w-100"]/a/text()').get()

        # Aggregating the first paragraph
        first_paragraph = ""
        for p in page_body.xpath('.//section[@class="av-details-page target w-100"]/p'):
            # Concatenate the text content of the paragraph
            first_paragraph += p.xpath('string()').get()

            # Check if the paragraph contains an anchor tag
            anchor_text = p.xpath('.//a/text()').get()
            if anchor_text:
                # Concatenate the text content of the anchor tag
                first_paragraph += anchor_text

            # Break the loop if the first paragraph is aggregated
            if first_paragraph:
                break

        first_paragraph = strip_first_paragraph(first_paragraph)

        # Aggregate date published
        date_published = extract_date_from_url(response.url)

        # Get tags
        tags = []
        tags = response.xpath('.//div[@class="blog-tag-row"]/a/text()').getall()

        # Get image
        photo_body = page_body.xpath('.//div[@id="article-start"]')

        # Extract the src attribute of the first image if it exists
        image_src = photo_body.xpath('.//img/@src').extract_first()

        # Extract the background-image URL from the YouTube video thumbnail div if it exists
        youtube_thumbnail_style = photo_body.xpath('.//div[@class = "ytp-cued-thumbnail-overlay-image"]/@style').extract_first()
        youtube_thumbnail_url = None

        if youtube_thumbnail_style:
            match = re.search(r'url\(["\']?([^"\']+)["\']?\);', youtube_thumbnail_style)
            if match:
                youtube_thumbnail_url = match.group(1)

        # Set article_image based on the extracted values
        if image_src:
            article_image = image_src
            # print("Article Image:", article_image)
        elif youtube_thumbnail_url:
            article_image = youtube_thumbnail_url
            # print("YouTube Video Thumbnail Image:", article_image)
        else:
            article_image = None
            # print("No article image found.")

        yield{"text": first_paragraph, "title": article_title, "author": author, "date": date_published, "tags": tags, "article_url": article_url, "img_url": article_image}




        #PYTHONDONTWRITEBYTECODE=1 scrapy crawl vidhya_content -o ../crawled/content/content_vidhya.jsonl
        

        ## first_paragraph: 250 characters
        ## article_title 
        ## author
        ## date published: year/month/day
        ## tags

        ## url of article
        ## image




