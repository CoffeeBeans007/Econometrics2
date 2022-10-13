from numpy import append
import yfinance as yf
import pandas as pd
from datetime import datetime
price_history=yf.Ticker("AMZN").history(period="5d",interval="1m")

df=pd.read_csv("this is good22")
print(df)
print(price_history["Open"])
print(price_history["Close"])

time=datetime.now()

# print(time)
# print(time.strftime("%H:%M:%S"))
# print(time.strftime("%Y,%m,%d"))
print(price_history)
for index, row in df.iterrows():
    print(row["Date"])
    print(row["Time"])

yahoodate=list(price_history["Datetime"])
print(type(yahoodate[1]))
datelist=[]
timelist=[]
x=0
for j in yahoodate:
    datelist.append(j.strftime("%b-%d-%y"))
    timelist.append(j.strftime("%H:%M%p")) 
    x+=1



price_history["Date"]=datelist
price_history["Time"]=timelist

price_history.to_csv("Prices")
df.to_csv("Sentiments")
