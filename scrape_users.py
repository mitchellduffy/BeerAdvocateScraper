from Scraper import UserScraper
import json

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
total_views = 3
print total_reviews

users = []
for i in range(0, total_views):
    start_number = i * 25
    scrap = UserScraper(start_number=start_number)
    users.extend(scrap.get_ref_beer_users())
print users


sss = scrap.get_ratings(users, list(style_set))



