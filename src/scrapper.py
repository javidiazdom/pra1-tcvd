import ssl
from urllib import response
import urllib.request
from bs4 import BeautifulSoup

class FilmDataScrapper():
    
    def __init__(self):
        self.url = "https://www.imdb.com"
        self.subdomain = "/search/title/?title_type=tv_movie,tv_series,tv_episode&release_date=2010-01-01,2022-04-06&countries=es&count=250"
        self.start = ""
        self.data = []
        
        # "&start=251
    
    def __download_html(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urllib.request.urlopen(self.url+self.subdomain)
        return response.read()
    
    def scrape(self):
        print(f'Scrapping data from {self.url}')
        html = self.__download_html()
        bs = BeautifulSoup(html, 'html.parser')
        list = bs.find('div', {'class':'lister-list'})
        rows = list.find_all('div', {'class':'lister-item'})
        for row in rows:
            itemContent = row.find('div', {'class': 'lister-item-content'})
            votes = itemContent.find('p', {'class': 'sort-num_votes-visible'})
            newEntry = {
                'name': itemContent.find('a').text,
                'url': itemContent.find('a').href,
                'year/s': itemContent.find('span', {'class': 'lister-item-year'}).text,
                'certificate': itemContent.find('span', {'class': 'certificate'}).text if itemContent.find('span', {'class': 'certificate'}) != None else '',
                'duration': itemContent.find('span', {'class': 'runtime'}).text if itemContent.find('span', {'class': 'runtime'}) else '',
                'rating': itemContent.find('strong').text if itemContent.find('strong') else '',
                'votes': votes.find('span', {'name': 'nv'}).text if votes else ''
            }
            self.data.append(newEntry)
        f = open("raw.html", "w", encoding="utf-8")
        f.write(str(self.data))