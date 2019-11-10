import pandas as pd
import pathlib
import re
from string import digits
import collections

folder = pathlib.Path.cwd() / 'RecipeScraping' / 'AllRecipes'
df = pd.read_csv(pathlib.Path(folder / 'newworldcuisines.csv'))

remove_digits = str.maketrans('', '', digits)

stopwords = ['teaspoons','teaspoon','tablespoon','tablespoons','cup','cups','containers','packets','bags',
        'quarts','pounds','cans','bottles','pints','packages','ounces','jars','heads','gallons','drops','envelopes',
        'bars','boxes','pinches','dashes','bunches','recipes','layers','slices','links','bulbs','stalks','squares',
        'sprigs','fillets','pieces','legs','thighs','cubes','granules','strips','trays','leaves','loaves','halves',
        'baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'ground', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied',
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped', 'unbaked', 'warmed','well',
        'very', 'super','diagonally', 'lengthwise', 'overnight','as', 'such', 'for', 'with', 'without', 'if', 'about',
        'e.g.', 'in', 'into', 'at', 'until','removed', 'discarded', 'reserved', 'included', 'inch', 'inches',
        'temperature', 'up','chunks', 'pieces', 'rings', 'spears','taste','and','ounce','package','cloves','finely',
        'to','circles','thinly','can','pound','inch','bunch','degrees','as','needed','container','or','quart','lightly',
        'garnish','frenched','canned','freshly','stalk','pint','-inch','milliliter','bottle','drain','reserve','tsp',
        'tbsp','g','tin','glb','oz','goz','see','above','on','an','angle','lengthways','ideally','pinch','mlfl','from',
        'room','topped','roughly','jar','clove','undrained','the','diagonal','free-range','more','if','you','want','it',
        'hot','this','makes','quite','a','according','only','jointed','packet','instructions','kglb','cmin','handful','any',
        'tough','mmin','x','plus','extra','ml','greasing','dusting','heaped','cob','alternatively','scraped','out','serve',
        'unavailable','tub','steamed','wedges','but','stoned','dice','ready-prepared','bite-size','hulled','distilled','square',
        'whole','shell-on','-ml-fl','sharp','knife','approximately','xcmxin','available','supermarkets','asian','de-seeded',
        'bite-sized','piece','new','waxy','litre','drizzling','ready-rolled','also','known','ready-made','-g-oz','use','made',
        'coating','loaf','intoinch','F','C','dredging','tops','prefer','preferably','coarsely','deep','frying','necessary',
        'stiffly','wash','florets','head','other','flanken','across','topping','whites','yolks','yolk','block','boneless',
        'breast','block','no salt added','half','unripe','picked','slicedinch','day-old','thick-cut','leg',
        'leg of','drumsticks','wings','slice','stale','pulp','edge','of','dash','massaged','segments','leftover',
        'plain','buy','inside','spoon','get','-g','unsmoked','bone-in','thoroughly','moons']


df['Ingredients'] = df['Ingredients'].str.strip('][').str.split('\', ')

for i in df['Ingredients'].index:
    for j, val in enumerate(df['Ingredients'][i]):
        query = val.translate(remove_digits).replace('\'','').replace('/','').replace('(','').replace(')','').replace('– ','')
        query = query.replace(',','').replace('.','').replace(' -','').replace(';','').replace('¾','').replace('½','').replace(':','').replace('¼','').replace('- ','').replace('\"','')
        querywords = query.split()
        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        result = ' '.join(resultwords)
        df['Ingredients'][i][j] = result

df = df.reset_index().rename(columns={'index':'id'})
output = df[['id','Ingredients']].rename(columns={'Ingredients':'ingredients'})
output.to_json(pathlib.Path(folder / 'ingredients.json'),orient='records')

df.describe()

classification = pd.read_csv(folder/ 'out.csv')
df = df.merge(classification, how='left', on='id')

df = df.loc[~(df.RecipeTitle == '504 Gateway Time-out')]
df2 = df.Ingredients.apply(pd.Series).merge(df, right_index = True, left_index = True).drop(["Ingredients"], axis = 1\
    ).melt(id_vars = ['RecipeTitle','TotalTime','Yields','Image','Instructions','Ratings','ReviewCount','OldestReview','Host','Url','cuisine'], value_name = "Ingredient").drop("variable", axis = 1).dropna(subset=['Ingredient']).sort_values(by=['RecipeTitle'])

df.to_csv(folder / 'worldcuisines_final.csv')
df2.to_csv(folder / 'alt_worldcuisines_final.csv')
