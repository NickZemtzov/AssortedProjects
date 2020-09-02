import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from Robinhood import Robinhood

def getOpenAndClosePriceForDay(Day):
    temp = Day.split(",")
    openPrice = float(temp[3][2:])#this must be 1 when using the NASDAQ or QTEC otherwise it's 2 so [3][2:]
    closePrice = float(temp[1][2:])
    return openPrice,closePrice

def basicAlgo(StartingAmount,stock): #backchecking an algorithm
    money = StartingAmount
    shares = 0
    finalPrice = getOpenAndClosePriceForDay(stock[1])[1]
    initialPrice = getOpenAndClosePriceForDay(stock[-1])[1]
    equityOverTime = []
    stockPerformanceOverTime = []
    correspondingDay = []
    for i in range(len(stock)-1):
        NVDAday = stock[len(stock)-i-1] #gets the first day
        NVDAopenPrice, NVDAclosePrice = getOpenAndClosePriceForDay(NVDAday) #finds the opening and closing prices
        #we now have the open and close price in a day for each stock. Now for the algorithm
        if NVDAclosePrice<NVDAopenPrice and money != 0:#if NVDA went down and you have the money to buy, do so
            shares = money/NVDAclosePrice
            money = 0
        if shares>0 and NVDAclosePrice>NVDAopenPrice:#sell a share if it went up that day
            money = NVDAclosePrice*shares
            shares = 0
        equityOverTime.append(money + shares*NVDAclosePrice)
        stockPerformanceOverTime.append((StartingAmount/initialPrice)*NVDAclosePrice)
        correspondingDay = correspondingDay + [i]

    money = money + shares*finalPrice #sell all remaining shares
    stockIncreaseOver5Years = finalPrice/(getOpenAndClosePriceForDay(stock[-1])[1])
    print(stockIncreaseOver5Years)
    print(money/StartingAmount)
    plt.plot(correspondingDay, equityOverTime, 'r--', correspondingDay, stockPerformanceOverTime, 'b--')
    plt.show()

def movingAvgAlgo(startingAmount,stock): #note the averages are based on close price
    overallData = []
    correspondingMovingAverageLength = []
    for i in range(2,260):#will calculate how well algo does for moving averages of 2 days up to 260 days
        money = startingAmount
        sharesOfAAPL = (startingAmount/2)/(getOpenAndClosePriceForDay(stock[len(stock) - 259])[1]) #starts half invested
        money = money/2

        closePrices = []#calculates the list of closing prices before start of trading date
        for j in range(i):
            AAPLday = stock[len(stock)+j-260]
            closePrices.append(getOpenAndClosePriceForDay(AAPLday)[1])
        for j in range(1000):#uses 1000 as the start to avoid startup bias on the moving averages
            AAPLday = stock[len(stock)-j-261]#starts 1000 days ago. gets data for day
            AAPLclosePrice = getOpenAndClosePriceForDay(AAPLday)[1]
            #trading algo
            if AAPLclosePrice > np.mean(closePrices) + np.std(closePrices) and sharesOfAAPL != 0:#if the price is a standard dev above the moving average, sell all
                money = sharesOfAAPL*AAPLclosePrice#sell all
                sharesOfAAPL=0
            if AAPLclosePrice < np.mean(closePrices) and sharesOfAAPL == 0:#if the close price drops below the moving average, put half of money in
                sharesOfAAPL = (money/2)/(AAPLclosePrice)#buy half
                money = money/2
            if AAPLclosePrice < np.mean(closePrices) + np.std(closePrices):
                sharesOfAAPL = sharesOfAAPL + money/AAPLclosePrice #buy all
                money = 0
            #updates moving average
            closePrices.append(AAPLclosePrice)
            closePrices = closePrices[1:]
        #Sell shares at end and calculate how well it did
        money = money + sharesOfAAPL*AAPLclosePrice
        AAPLPercentIncreaseLast1000Days = AAPLclosePrice/(getOpenAndClosePriceForDay(stock[len(stock) - 260])[1])
        overallData = overallData + [(money/startingAmount)]
        correspondingMovingAverageLength = correspondingMovingAverageLength + [i]
    print(AAPLPercentIncreaseLast1000Days)
    plt.plot(correspondingMovingAverageLength,overallData)
    plt.show()


NVDA = [s.rstrip() for s in open("HistoricalQuotesNVDA.txt","r").readlines()]
AAPL = [s.rstrip() for s in open("HistoricalQuotesAAPL.txt","r").readlines()]
NIO = [s.rstrip() for s in open("HistoricalQuotesNIO.txt","r").readlines()]
TSLA = [s.rstrip() for s in open("HistoricalQuotesTSLA.txt","r").readlines()]
DOW = [s.rstrip() for s in open("HistoricalQuotes^DOW.txt","r").readlines()]#note needs to be formated
NASDAQ = [s.rstrip() for s in open("HistoricalQuotesNASDAQ.txt","r").readlines()]#also needs formatting
QTEC = [s.rstrip() for s in open("HistoricalQuotesQTEC.txt","r").readlines()]#also needs formatting
ALGN = [s.rstrip() for s in open("HistoricalQuotesALGN.txt","r").readlines()]

startingAmount = 1000
basicAlgo(startingAmount,NIO)
movingAvgAlgo(startingAmount,QTEC)