import pandas as pd
import plotly.express as plt

df = pd.read_excel("MASS - ABC Analysis (version 2).xlsb.xlsx", sheet_name="Active ABC Items")
Headers = df.loc[[0]].values.tolist()
df = df.iloc[1:]
df.columns = Headers[0]
#at this point the df has all proper headers. Index of parts starts at 1 btw
#specify which columns to use
usingColumns = ["PART","DESCRIPTION","ABC","SAFETY_TOT","LEAD TIME","Buy Qty","AVG_UNIT_COST","Extended 12 Month Usage Cost","Extended Value","Months On Hand","Volitility"]
dictOfStuff = {}
for i in usingColumns:
    dictOfStuff.update({i:df[i].values.tolist()})
for i in dictOfStuff:
    df = pd.DataFrame(dictOfStuff)
#it is now a fresh df with only the designated columns. Next remove non-entries
for i in usingColumns:
    L = []
    if i != "PART" and i != "DESCRIPTION" and i != "ABC":
        for j in df[i].values.tolist():
            try:
                int(j)
                L.append(j)
            except:
                L.append(0)
        df[i] = L
#And any negative volitility numbers that dont make sense
L=[]
for i in df["Volitility"].values.tolist():
    if i<0:
        L.append(0)
    else:
        L.append(i)
df["Volitility"]=L
#now all the formerly blank values are zero and theres no numbers that dont make sense

#user input stuff
def userInput():
    min = input("Enter username:")




def plotStuff():
    indexList = [n for n in range(len(df["PART"]))]
    indexList = [float(j)/len(indexList)*100 for j in indexList]
    for i in usingColumns[3:]:
        fig = plt.scatter(df.sort_values(by=[i]), x=indexList, y=i, hover_data=["PART","DESCRIPTION"], color="ABC", color_discrete_map={"A":"purple","B":"goldenrod","C":"green"})
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig.show()

plotStuff()
