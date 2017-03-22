import requests
import re
import json
from BeautifulSoup import BeautifulSoup

class UserScraper:
    def __init__(self, start_number=0, brewery=199, beer=29619):
        self.url_ref_beer = "https://www.beeradvocate.com/beer/profile/%d/%d/?sort=topr&start=%d"
        self.url_ref_beer = self.url_ref_beer % (brewery, beer, start_number)
        self.soup = BeautifulSoup(requests.get(self.url_ref_beer).content)

    def get_ref_beer_soup(self):
        return self.soup

    def get_ref_beer_numbers(self):
        total_counts = self.soup.find('span', attrs={'class':'ba-reviews'}).getText()
        total_counts = int(total_counts.replace(',', ''))
        return total_counts, total_counts / 25, total_counts % 25

    def get_ref_beer_users(self):
        temp = self.soup.findAll('a', attrs={'class':'username'})
        users = []
        for i in temp:
            if len(i.getText()) > 0:
                users.append(i.getText())
                print i.getText()
        return users 

    def get_ratings(self, users, beer_list):
        for user in [users[0]]:
            print user
            url = "https://www.beeradvocate.com/user/beers/?start=0&ba=%s&order=dateD&view=R" % user
            print url
            soup = BeautifulSoup(requests.get(url).content)               
            total_counts = int(soup.body.findAll(text=re.compile('^.Ratings'))[0].split()[1])
            views = total_counts / 50
            rest = total_counts % 50

            for start_number in range(0,0): #range(0, views):
                start = start_number * 50
                url = "https://www.beeradvocate.com/user/beers/?start=%d&ba=%s&order=dateD&view=R" % (start, user)              
                soup = BeautifulSoup(requests.get(url).content)
                return soup.prettify()
                
          
class BeerScraper:
    def __init__(self, start_number=0, search='ipa'):
        self.url_beer = "https://www.beeradvocate.com/search/?start=%d&q=%s&qt=beer&retired=N"
        self.url_beer = self.url_beer % (start_number, search)
        self.soup = BeautifulSoup(requests.get(self.url_beer).content) 
        self.start_number = start_number

    def get_beer_soup(self):
        return self.soup

    def get_beer_number_found(self):
        total_counts = self.soup.body.findAll(text=re.compile('^Found:'))
        total_counts = int(total_counts[0].split()[1])
        return  total_counts, total_counts / 25, total_counts % 25 

    def get_beer_dict(self,  min_total_ratings=100, total_views=-1):
        results = self.soup.findAll('ul')
        beer_links = results[20].findAll('li')

        links = []
        for link in beer_links:
            links.append("http://beeradvocate.com%s" % (link.find('a')['href']))
            
        beer_dict = {}
        for count, beer in enumerate(links):
            print str(self.start_number + count + 1) + " of " + str(self.start_number + 25)

            soup = BeautifulSoup(requests.get(beer).content)

            ratings = soup.find('span', attrs={'class':'ba-ratings'}).getText()
            ratings = int(ratings.replace(',', ''))
            if ratings >= min_total_ratings:
                avg = soup.find('span', attrs={'class':'ba-ravg'}).getText()
                style = soup.find('a', href=re.compile('/beer/style/[0-9]')).getText()
                heading = soup.find('h1').getText()
                heading = heading.split('|')
                name = heading[0]
                brewery = heading[1]
                beer_dict[name] = {}
                beer_dict[name]['brewery'] = brewery
                beer_dict[name]['link'] = beer
                beer_dict[name]['ratings'] = ratings
                beer_dict[name]['average'] = avg
                beer_dict[name]['style'] = style

        return beer_dict


