class LinkGenerator():
    def __init__(self, keywords, sort = "popular"):
        self.keywords = keywords
        self.sort = sort
    
    def get_keywords(self):
        return self.keywords

    def get_sort(self):
        return self.sort
    
    def generate_base_link(self):
        return "https://zerochan.net/" + ', '.join(self.keywords) + "?s=" 
    
    def generate_useful_link(self, base_link):
        switcher = {"recent": "id", "popular": "fav", "random": "random"}
        sort_for_link = switcher[self.sort]
        return base_link + sort_for_link

#test_link = LinkGenerator("Kemonomimi", "popular")
#print(test_link.generate_useful_link(test_link.generate_base_link()))