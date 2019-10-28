#from urllib.request import urlopen
#from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import json
import csv
import pandas as pd
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
for i in range(0, 10):
    api = articleAPI('pvZFLevJFdexuI4lFdJ6K5tfPVAUTJbM')
    articles = api.search( q = 'italian', begin_date = 20160101, offset = i,
        fq = {'source':['Reuters','AP', 'The New York Times'], 'news_desk': 'Food'})
    with open('output.json', 'w') as raw_data:
        json.dump(articles, raw_data)

data = pd.read_json('output.json')
print(data)