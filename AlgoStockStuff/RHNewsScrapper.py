import Robinhood as Robinhood

def listOfTickers(folderOfOwnerData):#Way to get definitive list of tickers traded on RH
    filenames = listdir(folderOfOwnerData)
    return sorted([filename.split(".")[0] for filename in filenames])
LIST_OF_TICKERS = listOfTickers("BackTesting/RHStockPopularities(2020-06-16)")
for ticker in LIST_OF_TICKERS:
    try:
        stock_instrument = robinhood_client.instruments(ticker)[0]
    except:
        print(ticker)
