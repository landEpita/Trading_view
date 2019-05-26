from goose3 import Goose
from google_search import *
import sys

from textblob import TextBlob

def article(url):
    g = Goose()
    try:
        article = g.extract(url=url)
        print(article.title)
        #print(article.meta_description)
        return article.cleaned_text[:150]
    except:
        print("not fund")


def positif(text):
    obj = TextBlob(text)
    sentiment = obj.sentiment.polarity
    print(sentiment)



urls = Google.search(sys.argv[1])

for url in urls:
    positif(article(url))



