import numpy as np
import yfinance as yf
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from sklearn.linear_model import LinearRegression
import sklearn
import matplotlib.pyplot as plt
from scipy import correlate
import statsmodels.api as sm
from mpl_toolkits.mplot3d import Axes3D
prices=pd.read_csv("Prices")
sentiments=pd.read_csv("Sentiments")

final=pd.DataFrame(columns=["Comment","Date","Time","Price","Vol","Neut","Pos","Neg","Growth15Min"])
x=0
y=0
car=":AMP"
for index, row in sentiments.iterrows():
    
    
    
    Date=row["Date"]
    Time=row['Time']
    
    stringtime=Time
    newstring=Time
    
    for character in car:
        stringtime = stringtime.replace(character, "")
    intstring=int(stringtime)
    rightpm=0
    
    if newstring[-2]=="P":
        
        newstring=newstring.replace("PM","")
        newstring=newstring.replace(":","")
        
        intwa=int(newstring)
        if intwa>=1200:
            rightpm=1
        elif 0-intwa>=-400:
            rightpm=1
    
    if intstring>=930 or rightpm==1:
        
        firstflux=prices[prices['Date'] == Date]
        
        secondflux=firstflux[firstflux["Time"]==Time]
        
       

        if len(secondflux)!=0:
            value=secondflux.index.values[0]
            
            price5later=(prices.iloc[[value+15]]["Close"].tolist()[0])-secondflux["Close"].tolist()[0]
            # price5later=prices.iloc[value+10]["Close"]
            
            final.loc[x] = row["Text"],Date,Time,secondflux["Close"].tolist()[0],secondflux["Volume"].tolist()[0],row["neutRate"],row["posRate"]*100,row["negRate"],price5later
        
        y+=1
    x+=1
    

    
print(tabulate(final, headers='keys', tablefmt='psql'))
final.to_csv("FinalCSV")

x = final[["Vol","Pos"]]

y = np.array(final["Growth15Min"])



#Calculates regression line based on the sklearn library
lr = LinearRegression()
lr.fit(x, y)
predict_y = lr.predict(x)

r_sq = lr.score(x, y)
b0 = lr.intercept_
b1 = lr.coef_

#Creates an array of data based on b1 and b0
plotx=np.array(final["Vol"])
ploty=np.array(final["Pos"])
plotz=np.array(final["Growth15Min"])
fig=plt.figure()
ax=fig.add_subplot(projection="3d")
ax.scatter(plotx,ploty,plotz)
fig.show()
plt.show()

#Fits ai model on x(GDP) and y(Life expectancy) to find relevant statistics
model=sm.OLS(y,x.astype(float)).fit()

predictions=model.predict(x)

#Gives summary statistics on the correlation dataset
print_model=model.summary()
print(print_model)
print ("Intercept : ",lr.intercept_)
print("params",model.params)


#Average error calculation
leasterror=0
for index, row in final.iterrows():
    volume=model.params[0]
    pos=model.params[0]
    intercept=lr.intercept_
    error=row["Growth15Min"]-(volume*row["Vol"])-pos*row["Pos"]-intercept
    leasterror+=error**2

print(leasterror/25)
