from bs4 import BeautifulSoup
import re
import requests

from linkgenerator import LinkGenerator

class PageReader():
    def __init__(self, url, image_cnt=10):
        self.url = url
        self.image_cnt = image_cnt

        self.p = re.compile(r'https://static\.zerochan\.net/(?!download\.png)[\s\S]*?\.full\.[\d]*?\.[jp][pn]g')
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"} # something interesting i noticed is that requests is actually slower with a user agent. just a note for later
        self.links = []


    def get_url(self):
        return self.url
    
    def collect_links(self):
        for i in range(1, 101):
            soup = BeautifulSoup(requests.get(self.url + str(i)).text, "lxml")
            page = soup.find("ul", {"id": "thumbs2"})

            self.links.extend(self.p.findall(str(page)))

            if len(self.links) >= self.image_cnt or page is None:
                self.links = self.links[0:self.image_cnt]
                break

    def download(self, dir):
        increment = 0 # stupid
        for link in self.links:
            img = self.session.get(link, headers=self.headers).content
            with open (dir.get() + '/' + str(increment) + link[-4:], 'wb') as f:
                f.write(img)
                increment += 1
        

if __name__ == '__main__':
    #test = PageReader("https://www.zerochan.net/Fate%2FGrand+Order?s=fav")
    #test.collect_links()
    #test.download()
    pass
