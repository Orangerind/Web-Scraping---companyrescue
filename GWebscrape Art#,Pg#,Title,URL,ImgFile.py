#This web scraper goes to the companyrescue website and scrapes all the articles in their news section to get the url, title, and Image file names, but the file names are not yet cleaned
import requests
from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import os

# Create empty lists to store article titles and URLs
article_titles = []
article_urls = []
article_page= []
image_names=[]
clean_image_names = []

# Loop through pages 1- 60
for page_num in range(0, 60):
    url = f'https://www.companyrescue.co.uk/guides-knowledge/news/{page_num}' if page_num >= 1 else 'https://www.companyrescue.co.uk/guides-knowledge/news'
    
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Convert the response content into a string
    html_str = str(soup)

    # Working code to scrape specific details here
    # Code available upon request

# Remove any articles with 'N/A' titles or URLs
for i in range(len(article_titles)-1, -1, -1):
    if article_titles[i] == 'N/A' or article_urls[i] == 'N/A':
        del article_titles[i]
        del article_urls[i]
        del article_page[i]
        del image_names[i]



df_title = pd.DataFrame(article_titles, columns=['TITLE'])
df_urls = pd.DataFrame(article_urls, columns=['URL'])
df_pages = pd.DataFrame(article_page, columns=['PAGE#'])
df_imgs = pd.DataFrame(image_names, columns=['IMAGE'])


# Merge the four dataframes
df = pd.concat([df_pages, df_title, df_urls, df_imgs], axis=1)

df.to_csv(r'C:\Users\Admin\Documents\Self learn\Data Analytics\Data Analytics Client 3\Clean Clean Clean.csv')
