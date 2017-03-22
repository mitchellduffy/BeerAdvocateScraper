from Scraper import UserScraper
import json
import requests
from BeautifulSoup import BeautifulSoup

# load beer data and get the different styles
# -------------------------------------------
with open('beer_dict.json') as beer_dict:    
    data = json.load(beer_dict)

style_set = set() 
for beer in data:
    style_set.add(data[beer].get("style"))
print style_set



# get all the users who have rated a specific beer
# ------------------------------------------------
scrap = UserScraper()

total_reviews, total_views, total_rest = scrap.get_ref_beer_numbers()
total_views = 1
print total_reviews

users = []
for i in range(0, total_views):
    start_number = i * 25
    scrap = UserScraper(start_number=start_number)
    users.extend(scrap.get_ref_beer_users())
print users


user_dict = scrap.get_ratings(users, list(style_set))
print user_dict


with open("user_dict.json", "w") as writeJSON:
    json.dump(user_dict, writeJSON)













