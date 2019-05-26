from bs4 import BeautifulSoup
import requests
import re

class Google:
    @classmethod
    def search(self, search):
        path = "https://www.google.com/search?q="+search+"&tbm=nws"
        page = requests.get(path+"&cr=countryCA&lr=lang_us")
        soup = BeautifulSoup(page.content,features="lxml")
        links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        urls = [re.split(":(?=http)",link["href"].replace("/url?q=",""))[0] for link in links]
        
        urls = [re.split("&",link)[0] for link in urls]
        res = list(set([url for url in urls if 'webcache' not in url]))
        return res

