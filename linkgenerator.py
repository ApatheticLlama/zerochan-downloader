import requests

class LinkGenerator():
    def __init__(self, keywords, sort):
        self.keywords = keywords
        self.sort = sort
    
    def generate_link(self):
        switcher = {"Recent": "id", "Popular": "fav", "Random": "random"}
        sort = switcher[self.sort]
        return requests.get("https://zerochan.net/" + self.keywords).url + "?s=" + sort + "&p="