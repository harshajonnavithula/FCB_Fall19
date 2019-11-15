import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pathlib
import numpy as np
from functools import wraps
import datetime as dt

########################################################
TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?'
)
SERV_REGEX_NUMBER = re.compile(
    r'(\D*(?P<items>\d+)?\D*)'
)
SERV_REGEX_ITEMS = re.compile(
    r'\bsandwiches\b |\btacquitos\b | \bmakes\b', flags=re.I | re.X
)
SERV_REGEX_TO = re.compile(
    r'\d+(\s+to\s+|-)\d+', flags=re.I | re.X
)
def get_minutes(element):
    try:
        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()
        if '-' in tstring:
            tstring = tstring.split('-')[1]  # sometimes formats are like this: '12-15 minutes'
        matched = TIME_REGEX.search(tstring)

        minutes = int(matched.groupdict().get('minutes') or 0)
        minutes += 60 * int(matched.groupdict().get('hours') or 0)

        return minutes
    except AttributeError:  # if dom_element not found or no matched
        return 0
def get_yields(element):
    try:

        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()

        if SERV_REGEX_TO.search(tstring):
            tstring = tstring.split(SERV_REGEX_TO.split(tstring)[1])[1]

        matched = SERV_REGEX_NUMBER.search(tstring).groupdict().get('items') or 0
        servings = "{} serving(s)".format(matched)

        if SERV_REGEX_ITEMS.search(tstring) is not None:
            # This assumes if object(s), like sandwiches, it is 1 person.
            # Issue: "Makes one 9-inch pie, (realsimple-testcase, gives "9 items")
            servings = "{} item(s)".format(matched)

        return servings

    except AttributeError as e:  # if dom_element not found or no matched
        print("get_serving_numbers error {}".format(e))
        return ''
def normalize_string(string):
    return re.sub(
        r'\s+', ' ',
        string.replace(
            '\xa0', ' ').replace(  # &nbsp;
            '\n', ' ').replace(
            '\t', ' ').strip()
    )
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
##########################################################

def allrecipesworldcuisines(x,y):
    linklist = []
    for i in range(x,y):
        url = 'https://www.allrecipes.com/recipes/17562/dinner/?page=' + str(i)
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links_html = soup.findAll('a', href=True, class_='fixed-recipe-card__title-link')
        templist = [link.get('href') for link in links_html]
        linklist = list(set(linklist + templist))

    return linklist
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
def allrecipes(linklist):
    df = pd.DataFrame(columns=['RecipeTitle','TotalTime','Yields','Image',
    'Ingredients','Instructions','Ratings','ReviewCount','OldestReview','Host','Url'])

    for link in linklist:
        site = requests.get(link,headers)
        soup = BeautifulSoup(site.content,"html.parser")

        try:
            title = soup.find('h1').get_text()
        except:
            title = ''

        try:
            totaltime = get_minutes(soup.find('span',{'class': 'ready-in-time'}))

            if not totaltime:
                totaltime = get_minutes(soup.findAll('div', {'class': 'recipe-meta-item-body'})[2])
        except:
            totaltime = -1.0

        try:
            yieldtext = soup.find('meta',{'id': 'metaRecipeServings','itemprop': 'recipeYield'})

            if yieldtext:
                yields = get_yields(yieldtext.get("content"))
            else:
                yields = soup.findAll('div', {'class': 'recipe-meta-item-body'})[3].get_text().strip() + ' serving(s)'
        except:
            yields = ''

        try:
            img = soup.find('img',{'class': 'rec-photo', 'src': True})
            image = img['src']
        except:
            try:
                image = soup.find('div',{'class':'keyvals'})['data-content_featured_image']
            except:
                image = None

        try:
            ingr = soup.findAll('li',{'class': "checkList__line"})
            ingredients = [normalize_string(ingredient.get_text()) for ingredient in ingr if ingredient.get_text(strip=True) not in ('Add all ingredients to list','','ADVERTISEMENT')]

            if not ingredients:
                ingr = soup.findAll('span', {'class':'ingredients-item-name'})
                ingredients = [normalize_string(ingredient.get_text()) for ingredient in ingr]
        except:
            ingredients = []

        try:
            instr = soup.findAll('span',{'class': 'recipe-directions__list--item'})
            instructions = '\n'.join([normalize_string(instruction.get_text()) for instruction in instr])

            if not instructions:
                instr = soup.findAll('div',{'class':'section-body'})[0:len(instrlist)-1]
                instructions = '\n'.join([normalize_string(instruction.get_text()) for instruction in instr])
        except:
            instructions = ''

        try:
            rating = soup.find("meta", {"property": "og:rating"})

            if not rating is None:
                rating = round(float(rating['content']), 2)
            else:
                rating = float(soup.find("meta", {"name": "og:rating"})['content'])
        except:
            rating = -1.0

        try:
            review_count = int(soup.find('meta',{'itemprop': 'reviewCount','content': True})['content'])
        except:
            try:
                review_count = int(soup.find('div',{'class':'component recipe-reviews container-full-width template-two-col with-sidebar-right main-reviews'})['data-reviews-count'])
            except:
                review_count = -1.0

        try:
            revd = soup.findAll('div',{'itemprop': 'dateCreated'})
            reviewdates = [normalize_string(review.get_text()) for review in revd]

            if reviewdates:
                oldestreview = pd.to_datetime(reviewdates).min().date()
            else:
                revd = soup.findAll('span',{'class': 'recipe-review-date'})
                reviewdates = [normalize_string(review.get_text()) for review in revd]
                oldestreview = pd.to_datetime(reviewdates).min().date()
        except:
            oldestreview = pd.to_datetime('01/01/1900').date()

        scrapedata = {'RecipeTitle': title,
                        'TotalTime': totaltime,
                        'Yields':yields,
                        'Image':image,
                        'Ingredients':ingredients,
                        'Instructions':instructions,
                        'Ratings':rating,
                        'ReviewCount':review_count,
                        'OldestReview':oldestreview,
                        'Host':'allrecipes.com',
                        'Url':link
                        }
        df = df.append(scrapedata, ignore_index=True)

    df.drop_duplicates(subset='Url', inplace=True)

    return df

'''
#allrecipeslinks = allrecipesworldcuisines(i,i+10)
olddata = pathlib.Path.cwd() / 'RecipeScraping' / 'AllRecipes' / 'sampleworldcuisines.csv'
oldlinks = pd.read_csv(olddata)
oldlinks = list(oldlinks['Url'])
df = allrecipes(oldlinks)
df
datafile = pathlib.Path.cwd() / 'RecipeScraping' / 'AllRecipes' / 'newworldcuisines.csv'
temp = pd.read_csv(datafile)
df = temp.append(df,ignore_index=True).drop_duplicates(subset='Url')
df.to_csv(datafile, index=False)
'''
