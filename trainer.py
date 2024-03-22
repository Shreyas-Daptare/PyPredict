import yfinance as yf
import pandas as pd
import numpy as np
import math
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
# Pickling the classifier (Storing)
import pickle

tickers = ('USDT-USD', # Tether [USDT]
           'BTC-USD',  # Bitcoin [BTC]
           'BNB-USD',  # Binance Coin [BNB]
           'BUSD-USD', # Binance USD [BUSD]
           'ETH-USD',  # Ethereum [ETH]
           'DOT-USD',  # Polkadot [DOT]
           'ADA-USD',  # Cardano [ADA]
           'DOGE-USD', # Shiba Inu [SHIB]
           )



for ticker in tickers:
    df = yf.download(ticker, start = "2020-08-21", end = "2023-11-01")

    df['HL_PCT'] = (df['High'] - df['Close']) / df['Close'] * 100
    df['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100

    df = df[['Close','HL_PCT','PCT_change','Volume']]

    forecast_col = 'Close'
    df.loc[:,('Close','HL_PCT','PCT_change','Volume')].fillna(-99999, inplace=True)
    forecast_out = 1 # For 1 day

    df.loc[:, 'label'] = df[forecast_col].shift(-forecast_out)

    df.dropna(inplace=True)
    train = df.copy()

    clf = LinearRegression()
    predictors = ["Close","HL_PCT","PCT_change","Volume"]
    target = ['label']

    clf.fit(train[predictors],train[target])


    model_name = "./models/" + ticker + ".pickle"
    with open(model_name,'wb') as f:
        pickle.dump(clf,f)

    # Loading the file again
    # pickle_in = open('stockspredictor.pickle','rb')
    # clf = pickle.load(pickle_in)