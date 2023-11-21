# Information Retreival USI INF 2023

# Topic:
- Artifical Intelligence News

# Authors:
- Kyla Kaplan
- Elvira Baltasar

# Libraries:
- Scrapy
- Pyterrier

# Websites scraped:
- https://www.artificialintelligence-news.com/
- https://news.mit.edu/topic/artificial-intelligence2
- https://venturebeat.com/category/ai/

# File Breakdown (temporary)
- ir // main folder
    - scrapy.cfg // deployment configuration file
    - middlewares.py // project middlewares file
    - pipelines.py // project pipelines file
    - settings.py // project setting file

    - spiders/ // where the spiders are stored
        - __init_.py // spider initializer
        - example.py // example spider

# Execution
    In order to run the necessary spider:
    - $ scrapy crawl NAMEOFSPIDER -o results.jsonl