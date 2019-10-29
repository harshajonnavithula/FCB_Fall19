#from urllib.request import urlopen
#from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import json
import csv
import pandas as pd
import time
''' Author: Matt Krivansky
    Date: 10/07/2019

    This python 2.7 script will be used to scrape the NYTimes news website. 
    First we will scrape NYTimes Travel, then we will scrape NYTimes Food.
    
    First search will be by 'food'.

    Reference: https://dlab.berkeley.edu/blog/scraping-new-york-times-articles-python-tutorial
'''
''' Uses article search API to search articles that are in the Food news desk, since Jan 1 2016, from The New York Times,
    searches for the keyword italian. Loops through 0-50 to get 500 articles, ie. offset = 0 yields top 10 articles, 
    offset = 1 yields top 11-20 articles.
 '''


keywords = open('keywords.txt', 'r')
urls = []
for keyword in keywords:
    keyword = keyword.strip('\n')
    api = articleAPI('pvZFLevJFdexuI4lFdJ6K5tfPVAUTJbM')
    articles = api.search( q = keyword, begin_date = 20160101, offset = 0,
        fq = {'source':['Reuters','AP', 'The New York Times'], 'news_desk': 'Food'})
    with open('output.json', 'w') as raw_data:
        json.dump(articles, raw_data)
    articles = articles['response']['docs']
    for article in articles:
        print(article['web_url'])
        urls.append(str(article['web_url']))
    time.sleep(6)
new_urls = []
for i in range(len(urls)):
    new_urls.append(urls[i])
    new_urls.append('\n')

with open('NYTimes_urls.txt', 'w') as NYTimes_urls:
    NYTimes_urls.writelines(new_urls)