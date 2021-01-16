from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests

class PageReader():
    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(urlopen(url), "lxml")
        self.page = self.soup.find("ul", {"id": "thumbs2"})
        self.p = re.compile(r'https://static\.zerochan\.net/(?!download\.png)[\s\S]*?\.full\.[\d]*?\.[jp][pn]g')
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
        self.links = []


    def get_url(self):
        return self.url
    
    def get_page(self):
        return self.page

    def collect_links(self):
        self.links = self.p.findall(str(self.page))

    def download(self):
        increment = 0 # stupid
        for link in self.links:
            img = self.session.get(link, headers=self.headers).content
            with open (str(increment) + link[-4:], 'wb') as f:
                f.write(img)
                increment += 1
        

if __name__ == '__main__':
    test = PageReader("https://www.zerochan.net/Fate%2FGrand+Order?s=fav")
    test.collect_links()
    test.download()