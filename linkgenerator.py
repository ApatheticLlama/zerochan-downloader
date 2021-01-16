class LinkGenerator():
    def __init__(self, keywords, count, sort):
        self.keywords = keywords
        self.count = count
        self.sort = sort
    
    def generate_link(self):
        switcher = {"recent": "id", "popular": "fav", "random": "random"}
        sort_for_link = switcher[self.sort]
        return "https://zerochan.net/" + ', '.join(self.keywords) + "?s=" + sort_for_link


#test_link = LinkGenerator("Kemonomimi", "popular")
#print(test_link.generate_link())