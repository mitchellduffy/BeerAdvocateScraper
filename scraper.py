import requests
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(requests.get("http://beeradvocate.com/search?q=ipa&qt=beer").content)

results = soup.findAll('ul')

# manually identified item 20 
beer_links = results[20].findAll('li')
links = []
for link in beer_links:
    links.append("http://beeradvocate.com%s" % (link.find('a')['href']))
    

beer_list = {}
for beer in links:
    soup = BeautifulSoup(requests.get(beer).content)
    heading = soup.find('h1').getText()
    heading = heading.split('|')
    name = heading[0]
    brewery = heading[1]
    beer_list[name] = {}
    beer_list[name]['brewery'] = brewery
    beer_list[name]['link'] = beer


print beer_list
