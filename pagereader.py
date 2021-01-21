from bs4 import BeautifulSoup
import re
import requests
import time
import random

from linkgenerator import LinkGenerator

class PageReader():
    def __init__(self, url, dir, image_cnt):
        self.url = url
        self.dir = dir
        self.image_cnt = image_cnt

        self.p = re.compile(r'https://static\.zerochan\.net/(?!download\.png)[\s\S]*?\.full\.[\d]*?\.[jp][pn]g')
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        self.links = []


    def get_url(self):
        return self.url
    
    def collect_links(self):
        for i in range(1, 101):
            soup = BeautifulSoup(self.session.get(self.url + str(i), headers=self.headers).text, "lxml")
            page = soup.find("ul", {"id": "thumbs2"})
            
            self.links.extend(self.p.findall(str(page)))
            self.links = self.links[0:self.image_cnt]

            yield len(self.links)

            if page is None or len(self.links) == self.image_cnt:
                break

    def download_images(self):
        p=re.compile(r'(?!https:\/\/static\.zerochan\.net\/)[/s/S]*\.full\.[\d]*?\.[jp][pn]g') #nvm missing parentheses
        for iteration, link in enumerate(self.links):
            name = p.search(str(link)).group(0)
            img = self.session.get(link, headers=self.headers).content
            with open (self.dir + '/' + name, 'wb') as f: 
                f.write(img)
            
            yield iteration
    
    def download(self, queue):
        queue.put('c')
        link_gen = self.collect_links()
        while True:
            try:
                link_count = 'c' + str(next(link_gen))
                queue.put(link_count)
            except StopIteration:
                break
        
        queue.put('d')
        download_gen = self.download_images()
        while True:
            try:
                download_count = 'd' + str(next(download_gen))
                queue.put(download_count)
            except StopIteration:
                break
        
        queue.put("end")