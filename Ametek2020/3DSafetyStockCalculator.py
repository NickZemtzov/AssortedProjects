import plotly as plt
import pandas as pd
from statistics import stdev

#this relies on the file HistoricalDataForSafetyStock.xlsx
df = pd.read_excel("MyAmetekData.xlsx")
print(df.head())

#find standard deviation
for index,row in df.iterrows():
    listOfDemand = []
    print(row["201907"])
    listOfDemand.append(row["201907"])
    listOfDemand.append(row["201908"])
    listOfDemand.append(row["201909"])
    listOfDemand.append(row["201910"])
    listOfDemand.append(row["201911"])
    listOfDemand.append(row["201912"])
    listOfDemand.append(row["202001"])
    listOfDemand.append(row["202002"])
    listOfDemand.append(row["202003"])
    listOfDemand.append(row["202004"])
    listOfDemand.append(row["202005"])
    listOfDemand.append(row["202006"])
    print(stdev(listOfDemand))

