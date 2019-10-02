from recipe_scrapers import scrape_me

scraper = scrape_me('https://www.allrecipes.com/recipe/8358/apple-cake-iv/')

print(scraper.title())
print(scraper.total_time())
scraper.ingredients()
print(scraper.yields())
print(scraper.instructions())
scraper.image()
scraper.links()
