from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import requests
''' Author: Matt Krivansky
    Date: 10/07/2019

    This python3 script will be used to scrape the BBC news website. 
    First we will scrape BBC Travel, then we will scrape BBC Food.
    The BBC Travel article can be found at http://www.bbc.com/travel/story/20190818-whats-it-like-to-live-in-an-over-touristed-city
    The BBC Food article can be found at http://www.bbc.com/travel/story/20191007-brazil-the-last-frontier-of-gastronomy

    Parse the text file counting keywords for both Travel and Food. Create .csv file with counters for each
    keyword in keywords.txt.

    Reference: http://jonathansoma.com/lede/foundations-2017/classes/adv-scraping/scraping-bbc/
'''
data_list = [[]]
with open('BBC_urls.txt', 'r') as urls_txt:
    urls = urls_txt.readlines()
    for i in range(len(urls)):
        urls[i] = urls[i][:len(urls[i]) - 1]

url_food = ''
def main():    
    for i in range(len(urls)):
        data_list = [[]]
        url_food = urls[i]
        try:
            page_food = urlopen(str(url_food))
        except:
            continue
        soup_food = BeautifulSoup(page_food, 'html.parser')
        content_food = soup_food.find('div', {'class': 'body-content'})
        article_food = ''
        for i in content_food.findAll('p'):
            article_food = article_food + ' ' +  i.text
        text_file_name = url_food[32:]
        with open(text_file_name + '.txt', 'w') as file:
            file.write(article_food)
        print(url_food)
        #data_list.append([url_food, url_food[32:40]])
        #find_keywords('article_text.txt', url_food[32:])

def find_keywords(filename, webpage):
    keywords = open('keywords.txt', 'r')
    #output = open('BBC_Gastronomy_keywords_output.csv', 'w')
    data_list = [[]]
    webpage = webpage + '.csv'
    output = open(str(webpage), 'w')
    for keyword in keywords:
        keyword = keyword.strip('\n')
        count = 0
        file = open(filename)
        for line in file:
            sentence = line.split()
            for word in sentence:
                word = replace_characters(word)
                if str(keyword) == str(word):
                    count += 1
        file.close()
        data_list.append([keyword, count])
    writer = csv.writer(output)
    writer.writerows(data_list)
    output.close()
            
def replace_characters(text):
    characters = ['.', ',', ':', ':', '\"', '!', '"', "'", "(", ")", '/', '[', ']']
    for i in characters:
        text = text.replace(i, '')
    return text

def count_articles():
    url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=c0e876f5cc0d4412b6cd37a9b445168a')
    response = requests.get(url)
    print(response.json())

#find_keywords('BBC_Gastronomy.txt')
#count_articles()
main()