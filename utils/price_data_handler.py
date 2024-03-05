import talib

import pyEX as P
import pandas as pd
import numpy as np
from settings import settings

client = P.Client(api_token=settings.IEX_API_KEY)

def price_prompting(row, columns, exclude_col=['target']):
    res = ""
    exclude_col = ['target']
    for col in columns:
        if col not in exclude_col:
            res += f"{col} is {row[col]} "
    return res

def get_price_data(ticker):
    price = client.chartDF(ticker, '1m')
    # print(price)
    if price.empty:
        return price
    else:
        return price.sort_values(by='date')

def process_pipeline(df):
    new_df = pd.DataFrame()
    inputs = {}
    # df2['target'] = df.Close.pct_change().shift(-1).apply(lambda x: 1 if x>0 else 0)

    window_size = 5
    price_features = ['open', 'high', 'low', 'close']
    for col in price_features:
        inputs[col] = df[col].values.astype(np.double)

    new_df['Open'] = df.open
    new_df['High'] = df.high
    new_df['Low'] = df.low
    new_df['Close'] = df.close
    new_df['Adj Close'] = df.close

    # EMA
    # new_df['7ema'] = talib.EMA(inputs['close'], timeperiod=7)
    # new_df['14ema'] = talib.EMA(inputs['close'], timeperiod=14)
    # new_df['21ema'] = talib.EMA(inputs['close'], timeperiod=21)

    # macd
    # 3 7 11 // 7 21 14
    # new_df['7macd'], new_df['7macd_sig'], _ = talib.MACD(inputs['close'], 3, 7, 11)
    # new_df['14macd'], new_df['14macd_sig'], _ = talib.MACD(inputs['close'], 7, 21, 14)


    # atr 변동폭 -> natr - normalized atr
    new_df['7natr'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=7)
    new_df['14natr'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=14)
    new_df['21natr'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=21)


    # bollinger band
    new_df['7upper'], new_df['7middle'], new_df['7lower'] = talib.BBANDS(inputs['close'], timeperiod=7)
    new_df['14upper'], new_df['14middle'], new_df['14lower'] = talib.BBANDS(inputs['close'], timeperiod=14)
    new_df['21upper'], new_df['21middle'], new_df['21lower'] = talib.BBANDS(inputs['close'], timeperiod=21)

    # rsv raw stochastic value
    new_df['slow_k'], new_df['slow_d'] = talib.STOCH(inputs['high'], inputs['low'], inputs['close'])
    
    new_df['prev_close'] = df.close.shift(1)
    new_df['price_change'] = df.close.diff()
    new_df['pct_change'] = df.close.pct_change(1)

    return new_df

def processing_data(price):
    processed_price = process_pipeline(price)
    latest_price = processed_price.iloc[-1]
    
    final_price = normalize_price(latest_price)
    prompt = price_prompting(final_price, all_features)
    
    return prompt

norm_price_features = ['Open', 'High', 'Low', 'Close', 'Adj Close', '7upper', '7middle',
       '7lower', '14upper', '14middle', '14lower', '21upper', '21middle', '21lower', 'prev_close']
norm_percent_features = ['slow_k', 'slow_d']
normed_features = ['7natr', '14natr', '21natr']

all_features = norm_price_features + norm_percent_features + normed_features

def normalize_price(df):
    norm_data = pd.Series()
    for col in all_features:
        if col in norm_price_features:
            norm_data[col] = df[col] / df['Adj Close']
        elif col in norm_percent_features:
            norm_data[col] = df[col] / 100
        elif col in normed_features:
            norm_data[col] = df[col]

    return norm_data
