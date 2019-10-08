from urllib.request import urlopen
from bs4 import BeautifulSoup
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

def main():
    url_travel = "http://www.bbc.com/travel/story/20190818-whats-it-like-to-live-in-an-over-touristed-city"
    page_travel = urlopen(url_travel)
    soup_travel = BeautifulSoup(page_travel, 'html.parser')
    content_travel = soup_travel.find('div', {'class': 'body-content'})
    article_travel = ''
    for i in content_travel.findAll('p'):
        article_travel = article_travel + ' ' +  i.text
    with open('BBC_Overtouristed_City.txt', 'w') as file:
        file.write(article_travel)
    
    url_food = "http://www.bbc.com/travel/story/20191007-brazil-the-last-frontier-of-gastronomy"
    page_food = urlopen(url_food)
    soup_food = BeautifulSoup(page_food, 'html.parser')
    content_food = soup_food.find('div', {'class': 'body-content'})
    article_food = ''
    for i in content_food.findAll('p'):
        article_food = article_food + ' ' +  i.text
    with open('BBC_Gastronomy.txt', 'w') as file:
        file.write(article_food)

main()