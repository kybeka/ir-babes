import datetime
import re
from datetime import datetime

def convert_date(date_array):
    # Convert month name to its numerical representation
    months = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    month_name, day, year = date_array
    # Convert month name to numerical representation
    month = months.get(month_name)

    # Create a date object
    return {"year": int(year), "month": int(month)}
     

def strip_first_paragraph(first_paragraph):
    # Strip the first paragraph to only the first 250 characters
    stripped_paragraph = first_paragraph[:250].strip()
    return stripped_paragraph

    
def extract_date_from_url(url):
    # Define a regex pattern to extract year and month from the URL
    pattern = r'/(\d{4})/(\d{2})/'

    # Use regex to find the match in the URL
    match = re.search(pattern, url)

    # Check if a match is found
    if match:
        year, month = match.groups()
        return { "year": int(year), "month": int(month) }
    else:
        return None





    # def make(site,  # Domain of scraped site
    #      page_link,  # Page link
    #      artist_name,
    #      artist_image,
    #      bio,
    #      bio_long,
    #      amount_post,
    #      amount_subs,
    #      price_tiers,  # List of price tiers. See function 'make_price_tier'
    #      tags,  # Tags list
    #      socialmedias,  # Social media links list
    #      artist_banner):
    # # print(price_tiers)
    # return {
    #     'site': site,
    #     'page_link': page_link,
    #     'artist_name': stripIfNotNone(artist_name),
    #     'artist_image': stripIfNotNone(artist_image),
    #     'artist_banner': artist_banner,
    #     'bio': stripIfNotNone(bio),
    #     'bio_long': stripIfNotNone(bio_long),
    #     'amount_post': amount_post,
    #     'amount_subs': amount_subs,
    #     'price_tiers_title': list(map(lambda tier: stripIfNotNone(tier['title']), price_tiers or [])),
    #     'price_tiers_monthly': list(map(lambda tier: stripIfNotNone(tier['monthly']), price_tiers or [])),
    #     'price_tiers_monthly_chf': list(map(lambda tier: convertCurrenciesToCHF(tier['monthly']), price_tiers or [])),
    #     'price_tiers_description': list(map(lambda tier: stripIfNotNone(tier['description']), price_tiers or [])),
    #     'tags': tags or [],
    #     'socialmedias': socialmedias or [],
    #     'indexDate': datetime.now().isoformat()
    # }
