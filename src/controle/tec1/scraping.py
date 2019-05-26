import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pprint
print("start")

sia = SentimentIntensityAnalyzer()
date_sentiments = {}

for i in range(1,3):
    page = urlopen('https://www.businesstimes.com.sg/search/facebook?page='+str(i)).read()
    soup = BeautifulSoup(page, features="html.parser")
    posts = soup.findAll("div", {"class": "media-body"})
    for post in posts:
        time.sleep(1)
        url = post.a['href']
        date = post.time.text
        #print(date, url)
        #print(date_sentiments)
        try:
            try:
                link_page = urlopen(url).read()
            except:
                url = url[:-2]
                link_page = urlopen(url).read()
            link_soup = BeautifulSoup(link_page)
            sentences = link_soup.findAll("p")
            passage = ""
            for sentence in sentences:
                passage += sentence.text
            sentiment = sia.polarity_scores(passage)['compound']
            print(url, sentiment)
            date_sentiments.setdefault(date, []).append(sentiment)
        except:
            print("error")

date_sentiment = {}

for k,v in date_sentiments.items():
    date_sentiment[datetime.strptime(k, '%d %b %Y').date() + timedelta(days=1)] = round(sum(v)/float(len(v)),3)
    #print(v)
#print("end")

earliest_date = min(date_sentiment.keys())

#print(date_sentiment)
print(date_sentiment)
