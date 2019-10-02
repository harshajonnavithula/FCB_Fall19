import spoonacular as sp
import json
from pandas.io.json import json_normalize
import pandas as pd
import pathlib

api = sp.API('a3dc0c4c374149b29dfba84a54dec14c')
#zomato api key: 760e6dfad78b661b5a418129adbdb04c

query = 'pasta'
cuisine = 'Italian'
sort = 'popularity'
number = 5

response = api.search_recipes_complex(query, cuisine = cuisine, sort = sort, sortDirection = 'desc', number = number, addRecipeInformation = True)
data = response.json()

outputfile = open('spoonacular_output.json', 'w')
json.dump(data,outputfile, indent=4)
outputfile.close()

spoondata = json_normalize(data['results'])

with open('spoonacular_output.json', 'r') as datafile:
    test = json.load(datafile)
    datafile.close()
df2 = json_normalize(test['results'])

spoondata.to_excel('spoondata.xlsx')
