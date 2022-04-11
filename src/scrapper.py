import ssl
from urllib import response
import urllib.request
from bs4 import BeautifulSoup

class FilmDataScrapper():
    
    def __init__(self):
        self.url = "https://www.imdb.com"
        self.subdomain = "/search/title/?title_type=tv_movie,tv_series&release_date=2000-01-01,2022-12-31&countries=es&count=250"
        self.start = ""
        self.data = []
    
    def __download_html(self, subdomain):
        ssl._create_default_https_context = ssl._create_unverified_context
        print("Fetching: ", self.url+subdomain+self.start)
        response = urllib.request.urlopen(self.url+subdomain+self.start)
        return response.read()
    
    def __process_page(self):
        html = self.__download_html(self.subdomain)
        bs = BeautifulSoup(html, 'html.parser')
        list = bs.find('div', {'class':'lister-list'})
        rows = list.find_all('div', {'class':'lister-item'})
        for row in rows:
            itemContent = row.find('div', {'class': 'lister-item-content'})
            votes = itemContent.find('p', {'class': 'sort-num_votes-visible'})
            newEntry = {
                'name': itemContent.find('a').text,
                'url': itemContent.find('a', href=True)['href'],
                'year/s': itemContent.find('span', {'class': 'lister-item-year'}).text,
                'certificate': itemContent.find('span', {'class': 'certificate'}).text if itemContent.find('span', {'class': 'certificate'}) != None else '',
                'duration': itemContent.find('span', {'class': 'runtime'}).text if itemContent.find('span', {'class': 'runtime'}) else '',
                'rating': itemContent.find('strong').text if itemContent.find('strong') else '',
                'votes': votes.find('span', {'name': 'nv'}).text if votes and votes.find('span', {'name': 'nv'}) else ''
            }
            self.data.append(newEntry)
        
    
    def scrape(self):
        print(f'Scrapping data from {self.url}')
        self.__process_page()
        for x in range(1,19):
            self.start = '&start=' + str(x * 250 + 1)
            self.__process_page()
        self.__expand_films_info()
        
    def __expand_films_info(self):
        self.start = ''
        for entry in self.data:
            if (entry['url'] != None):
                bs = BeautifulSoup(self.__download_html(entry['url']),'html.parser')
                entry['popularity'] = bs.find('div', {'class': 'hero-rating-bar__popularity__score'}).text if bs.find('div', {'class': 'hero-rating-bar__popularity__score'}) != None else ''
                entry['country'] = bs.find(text='País de origen').parent.find('div', {'class': 'ipc-metadata-list-item__list-content-item'}).text if bs.find(text='País de origen') != None else ''
                entry['creator'] = bs.find(text='Creación').parent.find('div', {'class': 'ipc-metadata-list-item__list-content-item'}).text if bs.find(text='Creación') != None else ''
            
    def dataToCsv(self, filename):
        file=open("../csv" + filename, "w+")
        for key in self.data[0]:
            file.write(key.capitalize() + ";")
        for entry in self.data:
            for key in entry:
                file.write(entry[key] + ";")
                print(entry[key] + ";")
            file.write("\n")
            
            