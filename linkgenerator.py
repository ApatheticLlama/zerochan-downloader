class LinkGenerator():
    def __init__(self, keywords, sort):
        self.keywords = keywords
        self.sort = sort
    
    def generate_link(self):
        switcher = {"Recent": "id", "Popular": "fav", "Random": "random"}
        sort = switcher[self.sort]
        return "https://zerochan.net/" + self.keywords + "?s=" + sort + "&p="


#test_link = LinkGenerator("Kemonomimi", "popular")
#print(test_link.generate_link())
