import pandas as pd
import numpy as np
import plotly.express as plt

df = pd.read_excel("Copy of Ametek Material Usage last 2 years.xlsx")
Headers = df.loc[[0]].values.tolist()
df = df.iloc[1:]
Headers = Headers[0]
Headers[31] = "Sales Qty"
Headers[32] = "Sales Avg Cost"
Headers[34] = "WO Qty"
Headers[35] = "WO Avg Cost"
df.columns = Headers


SalesCost = df["Sales Avg Cost"].values.tolist()
SalesQty = df["Sales Qty"].values.tolist()
SalesTotal = []
for i in range(len(SalesCost)):
    try:
        SalesTotal.append(SalesCost[i]*SalesQty[i])
    except:
        pass
print(df.head())
WOCost = df["WO Avg Cost"].values.tolist()
WOQty = df["WO Qty"].values.tolist()
WOTotal = []
for i in range(len(WOCost)):
    try:
        WOTotal.append(WOCost[i]*WOQty[i])
    except:
        pass
Total = []
for i in range(len(SalesTotal)):
    Total.append(SalesTotal[i]+WOTotal[i])
df["TotalCost"] = Total
df = df.sort_values(by=["TotalCost"], ascending=False)

ABCcatagorization = []
for i in range(228):
    ABCcatagorization.append("A")
for i in range(452):
    ABCcatagorization.append("B")
for i in range(len(Total)-len(ABCcatagorization)):
    ABCcatagorization.append("C")
df["ABC"] = ABCcatagorization

df = df.dropna()
for index,row in df.iterrows():
    if row["Safety Stk"] == 0 or row["ABC"] == "C":
        df = df.drop(index)
#at this point the df is just a df with A and B categories and no 0 stock required

#now normalize each list of the monthly data
listOfLists = df.values.tolist()
finalDataDistribution = []
for l in listOfLists:
    data = np.array(l[7:31])
    normalizedData = (data-min(data))/(max(data)-min(data)) #note that min max scaling results in oversaturation in this case
    for i in normalizedData:
        finalDataDistribution.append(round(i,3))

fig = plt.histogram(x=finalDataDistribution, nbins=75)
fig.show()


#conclusion
#Next step, see which items have majority 0 per month and have still have non-zero safety despite low lead times.
#Also calculate the safety:avg demand ratio and look at highest


#So now that second step (cuz it's easier than the first)
df.reset_index(drop=True,inplace=True)
listOfLists = df.values.tolist()
listOfRatios = []
for l in listOfLists:
    data = l[7:31]
    avg = sum(data)/len(data)
    safetyTot = l[2]
    listOfRatios.append(safetyTot/avg)
df["SafetyTot/MonthlyAvg"] = listOfRatios#plot this as a rising distribution as well as against the lead time
#plotted in asending order
indexList = [n for n in range(len(listOfLists))]
fig = plt.scatter(df.sort_values(by="SafetyTot/MonthlyAvg"), x=indexList, y="SafetyTot/MonthlyAvg", hover_data=["Part #","Description", "ABC"])
fig.show()


#now I'll find the lead times. Bruh, this should really be in one file
print(df.head())
temp = df["Part #"].values.tolist()
temp2 = []
for i in temp:
    temp2.append(str(i))
df["Part #"] = temp2
#df = df.sort_values(by="Part #")
#df = df.sort_values(by="Description")

LTdf = pd.read_excel("MASS - ABC Analysis (version 2).xlsb.xlsx", sheet_name="Active ABC Items")
Headers = LTdf.loc[[0]].values.tolist()
LTdf = LTdf.iloc[1:]
LTdf.columns = Headers[0]
LTpart = LTdf["PART"].values
LTlist = LTdf["LEAD TIME"].values

LTdf2 = pd.read_excel("MASS - ABC Analysis (version 2).xlsb.xlsx", sheet_name="Manufactured Items")
Headers = LTdf2.loc[[0]].values.tolist()
LTdf2 = LTdf2.iloc[1:]
LTdf2.columns = Headers[0]
LTpart2 = LTdf2["PART"].values
LTlist2 = LTdf2["LEAD TIME"].values

result = []
for index,row in df.iterrows():
    goal = row["Part #"]
    found = False
    for i in range(len(LTpart)):
        if LTpart[i] == goal:
            try:
                int(LTlist[i])
                result.append(LTlist[i])
            except:
                result.append("NaN")
            found = True
    for i in range(len(LTpart2)):
        if LTpart2[i] == goal:
            try:
                int(LTlist2[i])
                result.append(LTlist2[i])
            except:
                result.append("NaN")
            found = True
    if found == False:
        result.append(None)
df["Lead Time"] = result
df = df.dropna()#this will end up dropping a few columns
#at this point the df has all the lead times. Now plot it against the saftey:montly avg ratio
fig = plt.scatter(df.sort_values(by="SafetyTot/MonthlyAvg"), x="Lead Time", y="SafetyTot/MonthlyAvg", hover_data=["Part #","Description", "ABC"])
fig.show()
df.to_csv("24MonthsPlusLeadTime.csv")


#this next section is finding which have majority zero demand on a monthly basis and then comparing that to lead time
minNumZeroMonths = 20 #out of 24
listOfLists = df.values.tolist()
listOfQualifyingIndexes = []
for l in range(len(listOfLists)):
    data = listOfLists[l][7:31]
    numZero = 0
    for datum in data:
        if datum == 0:
            numZero = numZero + 1
    if numZero >= minNumZeroMonths:
        listOfQualifyingIndexes.append(l)
new_df = pd.DataFrame(columns=df.columns)
for i in listOfQualifyingIndexes:
    row = df.loc[[i]].values.tolist()[0]
    new_df.loc[i] = row
new_df.to_csv("AAAAA.csv")


#lead time and m/p