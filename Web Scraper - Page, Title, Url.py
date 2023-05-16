#This web scraper goes to the companyrescue website and scrapes all the articles in their news section to get the url, title, page number
import requests
from bs4 import BeautifulSoup
import regex as re
import pandas as pd

# Create empty lists to store article titles and URLs
article_titles = []
article_urls = []
article_page= []

# Loop through pages 1-56
for page_num in range(1, 60):
    url = f'https://www.companyrescue.co.uk/guides-knowledge/news/{page_num}' if page_num > 1 else 'https://www.companyrescue.co.uk/guides-knowledge/news/'
    
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Convert the response content into a string
    html_str = str(soup)

    # Find all occurrences of '<div class="record">' in the HTML string
    record_start_idxs = [m.start() for m in re.finditer('<div class="record">', html_str)]

    # Loop through each record
    for i, start_idx in enumerate(record_start_idxs):
        # Find the end index of the record by finding the next occurrence of '<div class="record">' or the end of the string
        if i < len(record_start_idxs) - 1:
            end_idx = record_start_idxs[i+1]
        else:
            end_idx = len(html_str)

        # Extract the record substring
        record_str = html_str[start_idx:end_idx]

        # Extract the article title and URL from the record substring
        title_match = re.search('<h2><a href="(.*?)">(.*?)</a></h2>', record_str)
        if title_match:
            article_url = url + title_match.group(1).strip()
            article_title = title_match.group(2).strip()
        else:
            article_url = 'N/A'
            article_title = 'N/A'

        # Append the article title and URL to the respective lists
        article_titles.append(article_title)
        article_urls.append(article_url)
        article_page.append(page_num)

# Remove any articles with 'N/A' titles or URLs
for i in range(len(article_titles)-1, -1, -1):
    if article_titles[i] == 'N/A' or article_urls[i] == 'N/A':
        del article_titles[i]
        del article_urls[i]
        del article_page[i]

df_title = pd.DataFrame(article_titles, columns=['title'])
df_urls = pd.DataFrame(article_urls, columns=['url'])
df_pages = pd.DataFrame(article_page, columns=['Page'])

# Merge the two dataframes
df = pd.concat([df_pages,df_title, df_urls], axis=1)

df.to_csv(r'C:\Users\Admin\Documents\Self learn\Data Analytics\Data Analytics Client 2\First 3 Pages Scrape.csv')