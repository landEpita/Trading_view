import requests
import pandas as pd
import arrow
import datetime

def get_quote_data(symbol='SBIN.NS', data_range='1d', data_interval='1m'):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    print(res)
    body = data['chart']['result'][0]
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('Asia/Calcutta').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])    
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)     #removing NaN rows
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
    
    return df

data = get_quote_data('KPIT.NS', '1d', '1m')
print(data)
