# Import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# NLTK VADER for sentiment analysis
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
tickers = ['AMZN', 'TSLA', 'GOOG']
for ticker in tickers:
    url = finwiz_url + ticker
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)    
    # Read the contents of the file into 'html'
    html = BeautifulSoup(response)
    # Find 'news-table' in the Soup and load it into 'news_table'
    news_table = html.find(id='news-table')
    
    # Add the table to our dictionary
    news_tables[ticker] = news_table
amzn = news_tables["AMZN"]
# Get all the table rows tagged in HTML with <tr> into ‘amzn_tr’
amzn_tr = amzn.findAll("tr")
for i, table_row in enumerate(amzn_tr):

     # Read the text of the element ‘a’ into ‘link_text’
 a_text = table_row.a.text
 # Read the text of the element ‘td’ into ‘data_text’
#  print(table_row)
 td_text = table_row.td.text
 if i == 5:
    break
 # Print the contents of ‘link_text’ and ‘data_text’ 

# print(news_table.type())
 # Exit after printing 4 rows of data



parsed_news=[["Ticker","Date","Time","Text"]]

for file_name, news_table in news_tables.items():
    for x in news_table.findAll("tr"):
        text=x.a.get_text()
        date_scrape = x.td.text.split()
        if len(date_scrape)==1:
            time=date_scrape[0]

        else:
            date=date_scrape[0]
            time=date_scrape[1]
        ticker=file_name.split("_")[0]
        parsed_news.append([ticker,date,time,text])



df=pd.DataFrame(parsed_news[0:100][1:],columns=parsed_news[0])
scorelist=[]
neulist=[]
poslist=[]
neglist=[]
print(len(df["Text"]))
for i in df["Text"]:
    score = analyser.polarity_scores(i)
    
    neulist.append(score["neu"])
    poslist.append(score["pos"])
    neglist.append(score["neg"])

df["neutRate"]=neulist
df["posRate"]=poslist
df["negRate"]=neglist

print(tabulate(df, headers='keys', tablefmt='psql'))
df.to_csv("this is good22")