import requests
from BeautifulSoup import BeautifulSoup

class Scraper:
    def __init__(self):
        self.url_beer_temp = "https://www.beeradvocate.com/search/?start=%d&q=ipa&qt=beer&retired=N"

    def get_beer_soup(self, start_number=0):
        self.start_number_ = start_number
        url_beer = self.url_beer_temp % self.start_number_
        return BeautifulSoup(requests.get(url_beer).content) 

    def get_beer_dict(self, beer_soup, min_total_ratings=100):
        results = beer_soup.findAll('ul')
        beer_links = results[20].findAll('li')

        links = []
        for link in beer_links:
            links.append("http://beeradvocate.com%s" % (link.find('a')['href']))
            
        beer_dict = {}
        for count, beer in enumerate(links):
            print str(self.start_number_ + count + 1) + " of " + str(self.start_number_ + 25)

            soup = BeautifulSoup(requests.get(beer).content)

            ratings = soup.find('span', attrs={'class':'ba-ratings'}).getText()
            if ratings >= min_total_ratings:
                avg = soup.find('span', attrs={'class':'ba-ravg'}).getText()
                heading = soup.find('h1').getText()
                heading = heading.split('|')
                name = heading[0]
                brewery = heading[1]
                beer_dict[name] = {}
                beer_dict[name]['brewery'] = brewery
                beer_dict[name]['link'] = beer
                beer_dict[name]['ratings'] = ratings
                beer_dict[name]['average'] = avg

        return beer_dict



scrap = Scraper()

soup = scrap.get_beer_soup(0)
beer_dict = scrap.get_beer_dict(soup)

print beer_dict
           
