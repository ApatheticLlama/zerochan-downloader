from bs4 import BeautifulSoup
import re
import requests
import time
import random

from linkgenerator import LinkGenerator

class PageReader():
    def __init__(self, url, image_cnt=10):
        self.url = url
        self.image_cnt = image_cnt

        self.p = re.compile(r'https://static\.zerochan\.net/(?!download\.png)[\s\S]*?\.full\.[\d]*?\.[jp][pn]g')
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        self.links = []


    def get_url(self):
        return self.url
    
    def collect_links(self):
        for i in range(1, 101):
            print(i)
            soup = BeautifulSoup(self.session.get(self.url + str(i), headers=self.headers).text, "lxml")
            print(i)
            page = soup.find("ul", {"id": "thumbs2"})

            self.links.extend(self.p.findall(str(page)))

            if len(self.links) >= self.image_cnt or page is None:
                self.links = self.links[0:self.image_cnt]
                break

            time.sleep(random.randint(3, 8))

    def download(self, dir):
        increment = 0 # stupid
        for link in self.links:
            print(increment)
            img = self.session.get(link, headers=self.headers).content
            print(increment)
            with open (dir.get() + '/' + str(increment) + link[-4:], 'wb') as f:
                f.write(img)
                increment += 1

            time.sleep(random.randint(3, 8))

        

if __name__ == '__main__':
    #test = PageReader("https://www.zerochan.net/Fate%2FGrand+Order?s=fav")
    #test.collect_links()
    #test.download()
    pass
