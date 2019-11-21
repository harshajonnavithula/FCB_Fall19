#from urllib.request import urlopen
#from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re
import datetime
import urllib
#from goose3 import Goose

''' Author: Matt Krivansky
    Date: 10/07/2019

    This python 3.7 script will be used to scrape the NYTimes news website. 
    First we will scrape NYTimes Travel, then we will scrape NYTimes Food.
    
    First search will be by 'food'.

    Reference: https://dlab.berkeley.edu/blog/scraping-new-york-times-articles-python-tutorial
'''
''' Uses article search API to search articles that are in the Food news desk, since Jan 1 2016, from The New York Times,
    searches for the keyword italian. Loops through 0-10 to get 100 articles, ie. offset = 0 yields top 10 articles, 
    offset = 1 yields top 11-20 articles.
 '''

# STEP 2. DOWNLOAD ARTICLES
# If, at some point, Step 2 is interrupted due to unforeseen
# circumstances (power outage, loss of internet connection), replace the number
# (value of the variable url_num) below with the one you will find in the logfile.log

file = open('NYTimes_urls.txt', 'r')
urls = file.readlines()

data_list = [[]]
for i in range(len(urls)):
    urls[i] = urls[i][:len(urls[i]) - 1]

url_food = ''
def main():    
    data_list.append([url_food, date]) #should change, gets date of article from url
    #find_keywords('article_text.txt', url_food[24:]) #should change, gets the date and title of article from url

def count_articles():
    url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=c0e876f5cc0d4412b6cd37a9b445168a')
    response = requests.get(url)
    print(response.json())

def make_text_files():
    for i in range(len(urls)):
        if (urls[i][24:35] == 'interactive'):
            text_file_name = str(urls[i][36:len(urls[i]) - 5])
            print(text_file_name)
            text_file_name = text_file_name[:4] + text_file_name[5:7] + text_file_name[8:10] + '-' + text_file_name[11:17] + '-' + text_file_name[18:]
            print(text_file_name)
            try:
                f = open(text_file_name + '.txt', 'w+')
            except:
                continue

