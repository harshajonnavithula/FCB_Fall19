#from urllib.request import urlopen
#from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import time
import os
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
    
def make_urls_list():
    old_urls_list = []
    old_urls = open('NYTimes_urls.txt', 'r')
    for line in old_urls:
        old_urls_list.append(line)
    api = articleAPI('pvZFLevJFdexuI4lFdJ6K5tfPVAUTJbM')
    keyword = str(input('Enter the keyword to search for: '))
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
    print(new_urls)
    return

    with open('NYTimes_urls.txt', 'w') as NYTimes_urls:
        for i in range(len(new_urls)):
            if new_urls[i] not in old_urls_list:
                NYTimes_urls.writelines(new_urls[i])

list_of_text_file_names = []

def make_text_files_list():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith('.txt') and f.startswith('20'):
            list_of_text_file_names.append(str(f))
    print(list_of_text_file_names)

def find_keywords(text_filename, webpage):
    keywords = open('keywords.txt', 'r')
    data_list = [[]]
    webpage = webpage + '.csv'
    output = open(str(webpage), 'w')
    for keyword in keywords:
        keyword = keyword.strip('\n')
        count = 0
        file = open(text_filename)
        for line in file:
            sentence = line.split()
            for word in sentence:
                word = replace_characters(word)
                if str(keyword) == str(word):
                    count += 1
        file.close()
        data_list.append([keyword, count])
    writer = csv.writer(output)
    print(data_list)
    writer.writerows(data_list)
    output.close()
            
def replace_characters(text):
    characters = ['.', ',', ':', ':', '\"', '!', '"', "'", "(", ")", '/', '[', ']']
    for i in characters:
        text = text.replace(i, '')
    return text

def main():    
    make_text_files_list()
    print(len(list_of_text_file_names))
    for i in range(len(list_of_text_file_names)):
        data_list = [[]]
        print(list_of_text_file_names[i])
        find_keywords(list_of_text_file_names[i], list_of_text_file_names[i][:len(list_of_text_file_names[i]) - 4])

main()