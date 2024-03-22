from flask import Flask, render_template, request
import yfinance as yf
import pickle
from datetime import datetime    
# print(instruments)

tickers = ('USDT-USD', # Tether [USDT]
           'BTC-USD',  # Bitcoin [BTC]
           'BNB-USD',  # Binance Coin [BNB]
           'BUSD-USD', # Binance USD [BUSD]
           'ETH-USD',  # Ethereum [ETH]
           'DOT-USD',  # Polkadot [DOT]
           'ADA-USD',  # Cardano [ADA]
           'DOGE-USD', # Shiba Inu [SHIB]
           )





app = Flask(__name__)
app.secret_key = 'i dont care'

@app.route('/', methods=['GET','POST'])
def updatepredictions():
    # get live prices
    # price volume predictions
    instruments = {
        'BNB' : ['BNB-USD', 0, 0, 0],
        'BTC' : ['BTC-USD', 0, 0, 0],
        'ETH' : ['ETH-USD', 0, 0, 0],
        'GAL' : ['GAL11877-USD', 0, 0, 0],
        'GMT' : ['GMT18069-USD', 0, 0, 0],
        'USDT' : ['USDT-USD', 0, 0, 0],
        'BUSD' : ['BUSD-USD', 0, 0, 0],
        'DOT' : ['DOT-USD', 0, 0, 0],
        'ADA' : ['ADA-USD', 0, 0, 0],
        'SHIB' : ['SHIB-USD', 0, 0, 0]
    }
    forecast = []
    for ticker in tickers:
        df2 = yf.download(ticker, start="2023-11-02", end=datetime.today().strftime('%Y-%m-%d'))
        df2['HL_PCT'] = (df2['High'] - df2['Close']) / df2['Close'] * 100
        df2['PCT_change'] = (df2['Close'] - df2['Open']) / df2['Open'] * 100
        df2 = df2[['Close','HL_PCT','PCT_change','Volume']]
        df2.fillna(-99999, inplace=True)
        test = df2.copy()
        predictors = ["Close","HL_PCT","PCT_change","Volume"]
        model_name = "./models/" + ticker + ".pickle"
        with open(model_name, 'rb') as pickle_in:
            clf = pickle.load(pickle_in)
        prediction = clf.predict(test[predictors])
        forecast.append(prediction[-1])
        
    for key, value in instruments.items():
        data = yf.download(value[0], period='1d', interval='1h')
        instruments[key][1] = round(data.iloc[-1].Close, 3)
        instruments[key][2] = int(round(data.iloc[-1].Volume, 3))
        
        
    
    return render_template('index.html', instruments = instruments, forecast = forecast)






#print(instruments['BNB'])





if __name__ == "__main__":
    app.run(debug=True)