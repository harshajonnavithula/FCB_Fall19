import spoonacular as sp
import json
from pandas.io.json import json_normalize
import pandas as pd
import pathlib

#API Key
api = sp.API('a3dc0c4c374149b29dfba84a54dec14c')
#zomato api key: 760e6dfad78b661b5a418129adbdb04c

#Output path setup
parent = pathlib.Path.cwd() / 'RecipeScraping' / 'Spoonacular'
outputpath = parent / 'spoonacular_output.json'
csvpath = parent / 'spoondata_mediterranean.csv'

#API Query Settings
query = ''
number = 10
sort = 'popularity'
offset = 10
cuisine = 'mediterranean'

#Calling the API, sending results to JSON file and interpreting into dataframe
response = api.search_recipes_complex(query, sort = sort,\
 sortDirection = 'desc', number = number, addRecipeInformation = True,\
 fillIngredients = True, cuisine = cuisine, offset = offset)
data = response.json()
outputfile = open(outputpath, 'w')
json.dump(data,outputfile, indent=4)
outputfile.close()
spoondata = json_normalize(data['results'])

#Reading existing data already loaded into csv
with open(csvpath, 'r') as datafile:
    read = pd.read_csv(datafile, index_col=0)
    datafile.close()

#Appending new data to existing data, duplicates dropped
combineddata = read.append(spoondata, sort=False)
combineddata = combineddata.drop_duplicates('id').reset_index(drop=True)

#Output to csv
combineddata.to_csv(csvpath)
