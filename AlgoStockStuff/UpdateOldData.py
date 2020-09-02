from Robinhood import Robinhood
import pandas as pd
import numpy as np

import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import pytz

#to run this again, just redownload the latest version of the robintrack historicals
robinhood_client = Robinhood()
robinhood_client.login(username='nzemtzov@g.hmc.edu', password='NeoQuantReloaded')

def getPercentMoveNextDay(ticker,day):#note that day must be in form YYYY-MM-DD and quote data must be from RH historicals by day like l = robinhood_client.get_historical_quotes("BCDA", 'day','year')['results'][0]['historicals']
    historicalQuote = robinhood_client.get_historical_quotes(ticker, 'day','year')['results'][0]['historicals']
    for i in range(len(historicalQuote)):
        if historicalQuote[i]["begins_at"][:10] == day:
            return round((float(historicalQuote[i+1]["close_price"])-float(historicalQuote[i]["close_price"]))*100/float(historicalQuote[i]["close_price"]),2)
def getPercentMoveForDay(ticker,day):#note that day must be in form YYYY-MM-DD and quote data must be from RH historicals by day like l = robinhood_client.get_historical_quotes("BCDA", 'day','year')['results'][0]['historicals']
    historicalQuote = robinhood_client.get_historical_quotes(ticker, 'day','year')['results'][0]['historicals']
    for i in range(len(historicalQuote)):
        if historicalQuote[i]["begins_at"][:10] == day:
            return round((float(historicalQuote[i]["close_price"])-float(historicalQuote[i-1]["close_price"]))*100/float(historicalQuote[i-1]["close_price"]),2)
def getNumDaysOnIndex(ticker,dd,index):
    result = 0
    startPoint = listOfDays.index(dd)
    isInList = True
    for i in range(startPoint+1):
        if isInList == True:
            tickers = []
            t = [s.rstrip() for s in open("DailyMoversData/" + listOfDays[startPoint-i] + index + ".txt").readlines()]
            for line in t[:-1]:
                tickers.append(line.split(":")[0])

            isInList = False
            for j in range(len(tickers)):
                if tickers[j] == ticker:
                    result = result + 1
                    isInList = True
    return result
def getRobinHoodOwners(ticker,day):
    df = pd.read_csv("BackTesting/RHStockPopularities(2020-06-26)/" + ticker + ".csv")
    for row in df.itertuples():
        if str(row.timestamp)[:13] == day + " 21":
           return row.users_holding
def getCoefficients(ticker, day):
    x_data = [n for n in range(7)]
    y_data = []

    Days = []
    ind = 0
    data = robinhood_client.get_historical_quotes(ticker, 'day','year')['results'][0]['historicals']
    for i in range(len(data)):
        if data[i]["begins_at"][:10] == day:
            ind = i
    for i in range(7):
        Days.append(data[ind-i]["begins_at"][:10])
    for d in Days:
        y_data.append(getRobinHoodOwners(ticker,d))
    y_data.reverse()
    return round(np.polyfit(x_data, np.log(y_data), 1, w=np.sqrt(y_data))[0],4)*1000
def getVolume(ticker,day):#note that day must be in form YYYY-MM-DD and quote data must be from RH historicals by day like l = robinhood_client.get_historical_quotes("BCDA", 'day','year')['results'][0]['historicals']
    historicalQuote = robinhood_client.get_historical_quotes(ticker, 'day','year')['results'][0]['historicals']
    for i in range(len(historicalQuote)):
        if historicalQuote[i]["begins_at"][:10] == day:
            return int(historicalQuote[i]["volume"])

    
firstDate = date(2020, 4, 27)#change this whenever updating
listOfDays = []
for i in robinhood_client.get_historical_quotes("AAPL", 'day','year')['results'][0]['historicals']:
    listOfDays.append(i["begins_at"][:10])
listOfDays = listOfDays[listOfDays.index(str(firstDate)):]
listOfDays = listOfDays[:-1]#should have all the days that have recorded files


for day in listOfDays[:-1]:
    g = [s.rstrip() for s in open("DailyMoversData/" + day + "Gainers.txt").readlines()]
    l = [s.rstrip() for s in open("DailyMoversData/" + day + "Losers.txt").readlines()]
    gm = [s.rstrip() for s in open("DailyMoversData/" + day + "GainersMinusOverBought.txt").readlines()]
    ob = [s.rstrip() for s in open("DailyMoversData/" + day + "OverBought.txt").readlines()]
    os = [s.rstrip() for s in open("DailyMoversData/" + day + "OverSold.txt").readlines()]
        
    df = pd.DataFrame()

    temp = []
    percentMoveThisDay = []
    index = []
    daysOnIndex = []
    RHOwners = []
    RHOwnersCoefficient = []
    volume = []

    percentMoveNextDay = [] #note this is the target data for the NN

    for line in g[:-1]:
        try:
            robinhood_client.quote_data(line.split(":")[0])["last_trade_price"]
            temp.append(line.split(":")[0])
            index.append("Gainers")
        except:
            pass
    for line in l[:-1]:
        try:
            robinhood_client.quote_data(line.split(":")[0])["last_trade_price"]
            temp.append(line.split(":")[0])
            index.append("Losers")
        except:
            pass
    for line in gm[:-1]:
        try:
            robinhood_client.quote_data(line.split(":")[0])["last_trade_price"]
            temp.append(line.split(":")[0])
            index.append("GainersMinusOverBought")
        except:
            pass
    for line in ob[:-1]:
        try:
            robinhood_client.quote_data(line.split(":")[0])["last_trade_price"]
            temp.append(line.split(":")[0])
            index.append("OverBought")
        except:
            pass
    for line in os[:-1]:
        try:
            robinhood_client.quote_data(line.split(":")[0])["last_trade_price"]
            temp.append(line.split(":")[0])
            index.append("OverSold")
        except:
            pass

    for i in range(len(temp)):
        ticker = temp[i]
        try:
            percentMoveThisDay.append(getPercentMoveForDay(ticker,day))
        except:
            percentMoveThisDay.append("NaN")
        try:
            percentMoveNextDay.append(getPercentMoveNextDay(ticker,day))
        except:
            percentMoveNextDay.append("NaN")
        try:
            daysOnIndex.append(getNumDaysOnIndex(ticker,day,index[i]))
        except:
            daysOnIndex.append("NaN")
        try:
            RHOwners.append(getRobinHoodOwners(ticker, day))
        except:
            RHOwners.append("NaN")
        try:
            RHOwnersCoefficient.append(getCoefficients(ticker,day))
        except:
            RHOwnersCoefficient.append("NaN")
        try:
            volume.append(getVolume(ticker,day))
        except:
            volume.append("NaN")
            
        
    df["Ticker"] = temp
    df["Index"] = index
    df["DaysOnIndex"] = daysOnIndex
    df["Owners"] = RHOwners
    df["OwnersCoefficient"] = RHOwnersCoefficient
    df["PercentMoveToday"] = percentMoveThisDay
    df["Volume"] = volume
    df["target"] = percentMoveNextDay
    df.to_csv(day + ".csv", index=False)
    print("done")
#edit target with change in day on spy?