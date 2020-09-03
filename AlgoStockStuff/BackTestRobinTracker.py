from Robinhood import Robinhood
import pandas as pd
import numpy as np
from os import listdir

def listOfDays(RHhistorical):
    finalList = []
    for i in RHhistorical:
        finalList.append(i["begins_at"][:10])
    return finalList

def listOfFiles(folderOfOwnerData):
    filenames = listdir(folderOfOwnerData)
    return sorted([filename for filename in filenames])

def getPercentMoveForDay(historicalQuote,day):#note that day must be in form YYYY-MM-DD and quote data must be from RH historicals by day like l = robinhood_client.get_historical_quotes("BCDA", 'day','year')['results'][0]['historicals']
    for i in range(len(historicalQuote)):
        if historicalQuote[i]["begins_at"][:10] == day:
            return round((float(historicalQuote[i]["close_price"])-float(historicalQuote[i-1]["close_price"]))*100/float(historicalQuote[i-1]["close_price"]),2)

def getOwnersAtCloseOfDay(df,day):#Again day must be in form YYYY-MM-DD. Also note that on RobinTrack data, the market closes for the day at 22:00 so this is the time before close
    for row in df.itertuples():
        if str(row.timestamp)[:13] == day + " 21":
           return row.users_holding

def determineImportantCoefficient(x_data, y_data, typeOfRegression): #type is either "exponential" or "linear"
    if typeOfRegression == "exponential":
        return round(np.polyfit(x_data, np.log(y_data), 1, w=np.sqrt(y_data))[0],4)
    if typeOfRegression == "linear":
        return round(np.polyfit(x_data, y_data, 1)[0],4)
    else:
        print("invalid regression type")

def findBestStocksOnDay(files,day,timeFrame,listOfDays,typeOfCurve,numStocks):#day,timeFrame,numStocks,listOfDays): #timeFrame is an int of days back
    positionOfDayInListOfDays = 0
    finalDict = {}
    for i in range(len(listOfDays)):
        if day == listOfDays[i]:
            positionOfDayInListOfDays = i

    for fileName in files:
        df = pd.read_csv(ROBIN_TRACK_FOLDER_NAME + "/" + fileName)
        x_data = []
        y_data = []
        for i in range(timeFrame):#get data for days
            x_data.append(i)
            y_data.append(getOwnersAtCloseOfDay(df, listOfDays[positionOfDayInListOfDays-i]))
        y_data.reverse()
        for i in range(len(y_data)):
            if y_data[i] == None:
                y_data[i] = 0
            if y_data[i] < MIN_OWNERS_LIMIT:
                for j in range(len(y_data)):
                    y_data[j] = 0
        print(fileName)
        print(y_data)
        print(x_data)
        print()
        #add the computed coefficient to the dictionary for the day along with ticker as key value pair
        if typeOfCurve == "exponential":
            try:
                finalDict.update({fileName.split(".")[0]:determineImportantCoefficient(x_data,y_data,"exponential")})
            except:
                finalDict.update({fileName.split(".")[0]:0})
        if typeOfCurve == "linear":
            try:
                finalDict.update({fileName.split(".")[0]:determineImportantCoefficient(x_data,y_data,"linear")})
            except:
                finalDict.update({fileName.split(".")[0]:0})
    #compute best performing companys
    finalTickers = []
    for i in range(numStocks):
        finalTickers.append(max(finalDict,key=finalDict.get))
        del finalDict[max(finalDict,key=finalDict.get)]
    return finalTickers

def backTest(endDay,timePeriod, functionType, numStocks):
    daysToTest = LIST_OF_TRADING_DAYS[timePeriod:LIST_OF_TRADING_DAYS.index(endDay)+1]
    print(daysToTest)
    OverallMoves = []
    for day in daysToTest:
        tickers = findBestStocksOnDay(listOfFiles(ROBIN_TRACK_FOLDER_NAME), day, timePeriod, LIST_OF_TRADING_DAYS, functionType,numStocks)
        percentMove = []
        for ticker in tickers:
            try:
                l = robinhood_client.get_historical_quotes(ticker, 'day','year')['results'][0]['historicals']
                percentMove.append(getPercentMoveForDay(l,LIST_OF_TRADING_DAYS[LIST_OF_TRADING_DAYS.index(day)+1]))#Get the move on the following day
            except:
                pass
        print(percentMove)
        OverallMoves.append(sum(percentMove)/len(percentMove))
    return sum(OverallMoves)/len(OverallMoves)



'''Try a varient where u need more than a certain num of people owning'''
robinhood_client = Robinhood()
robinhood_client.login(username='', password='')
ROBIN_TRACK_FOLDER_NAME = "RHStockPopularities(2020-06-16)"
LIST_OF_TRADING_DAYS = listOfDays(robinhood_client.get_historical_quotes("AAPL", 'day','year')['results'][0]['historicals'])
MIN_OWNERS_LIMIT = 200
STONKS = 5

#edit this as you test
f = open("ResultsWith" + str(MIN_OWNERS_LIMIT) + "MinOwnersLimit," + str(STONKS) + "stocks,BuyDayAfter.txt","w+")
f.write("2Day,Exponential:" + str(backTest("2020-06-16",2, "exponential", STONKS)))
f.write("2Day,Linear:" + str(backTest("2020-06-16",2, "linear", STONKS)))
f.write("3Day,Exponential:" + str(backTest("2020-06-16",3, "exponential", STONKS)))
f.write("3Day,Linear:" + str(backTest("2020-06-16",3, "linear", STONKS)))
f.write("5Day,Exponential:" + str(backTest("2020-06-16",5, "exponential", STONKS)))
f.write("5Day,Linear:" + str(backTest("2020-06-16",5, "linear", STONKS)))
f.write("7Day,Exponential:" + str(backTest("2020-06-16",7, "exponential", STONKS)))
f.write("7Day,Linear:" + str(backTest("2020-06-16",7, "linear", STONKS)))
f.write("12Day,Exponential:" + str(backTest("2019-07-11",12, "exponential", STONKS)))
f.write("12Day,Linear:" + str(backTest("2020-06-16",12, "linear", STONKS)))
f.close()


