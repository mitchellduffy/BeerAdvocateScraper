from Scraper import BeerScraper
import json



scrap = BeerScraper()

total_beers, total_views, total_rest = scrap.get_beer_number_found()
#total_views = 2
print total_views

beer_dict = {}
for i in range(0, total_views):
    start_number = i * 25
    beer_dict_old = beer_dict
    scrap = BeerScraper(start_number=start_number)
    beer_dict_new = scrap.get_beer_dict()
    beer_dict = beer_dict_old.copy()
    beer_dict.update(beer_dict_new)
print beer_dict


with open("beer_dict.json", "w") as writeJSON:
    json.dump(beer_dict, writeJSON)

