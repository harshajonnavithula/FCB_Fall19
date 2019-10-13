from recipe_scrapers import scrape_me
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pathlib
import numpy as np

######################## AllRecipes
#Fetching links from world cuisines page
def allrecipesworldcuisines(x,y):
    linklist = []
    for i in range(x,y):
        url = 'https://www.allrecipes.com/recipes/86/world-cuisine/?page=' + str(i)
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links_html = soup.findAll('a', href=True, class_='fixed-recipe-card__title-link')
        templist = [link.get('href') for link in links_html]
        linklist = list(set(linklist + templist))

    return linklist

######################## BBCFood
#Fetching links from cuisines page
def bbcfoodcuisines():
    linklist = []
    url = 'https://www.bbc.co.uk/food/cuisines'
    headers = requests.utils.default_headers()
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    mainlinks_html = soup.findAll('a', href=True, class_='promo promo__cuisine')
    maintemplist = ['https://www.bbc.co.uk' + link.get('href') for link in mainlinks_html]

    for url in maintemplist:
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links_html = soup.findAll('a', href=True, class_=re.compile('promo promo__[^i]....'))
        templist = ['https://www.bbc.co.uk' + link.get('href') for link in links_html]
        linklist = list(set(linklist + templist))

    return linklist


allrecipeslinks = allrecipesworldcuisines(1,11)
bbcfoodlinks = bbcfoodcuisines()

#Scraping fields from linklist
def scrapingdata(linklist):
    df = pd.DataFrame(columns=['RecipeTitle','TotalTime','Yields','Image',
     'Ingredients','Instructions','Ratings','Host','Url'])
    for link in linklist:
        scraper = scrape_me(link)

        try:
            rating = scraper.ratings()
        except:
            rating = np.nan

        scrapedata = {'RecipeTitle': scraper.title(),
                    'TotalTime':scraper.total_time(),
                    'Yields':scraper.yields(),
                    'Image':scraper.image(),
                    'Ingredients':scraper.ingredients(),
                    'Instructions':scraper.instructions(),
                    'Ratings':rating,
                    'Host':scraper.host(),
                    'Url':link}
        df = df.append(scrapedata, ignore_index=True)
    df.drop_duplicates(subset='Url', inplace=True)

    return df

df = scrapingdata(bbcfoodlinks)
df

#Writing to csv
datafile = pathlib.Path.cwd() / 'RecipeScraping' / 'AllRecipes' / 'sampleworldcuisines.csv'
temp = pd.read_csv(datafile)
df = temp.append(df,ignore_index=True).drop_duplicates(subset='Url')
df.to_csv(datafile, index=False)
