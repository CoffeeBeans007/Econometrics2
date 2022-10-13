# Import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from time import strptime
from time import strftime
prices=pd.read_csv("Prices")
print(prices)
newtimelist=[]
for index, row in prices.iterrows():
    
    newtime=row["Time"]
    
    
    if newtime[-2]=="P":
        striptime=newtime
        striptime=striptime.replace("PM","")
        striptime=striptime.replace(":","")
        hours=striptime[:2]
        if hours=="13":
            newtimes="01"
        elif hours=="14":
            newtimes="02"
        elif hours=="15":
            newtimes="03"
        else:
            newtimes="12"
        newtime=newtimes+":"+striptime[2]+striptime[3]+"PM"

    print(newtime)
    newtimelist.append(newtime)

prices["Time"]=newtimelist    
print(prices)
prices.to_csv("Prices")


        
        



            
    



        
        