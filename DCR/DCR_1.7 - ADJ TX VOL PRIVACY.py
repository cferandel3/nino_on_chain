# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient

dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR CM DATA

asset = "dcr"
date_1 = "2016-02-08"
date_2 = "2020-06-10"

rawtxflow = cm.get_asset_data_for_time_range(asset, "TxTfrValNtv", date_1, date_2)
txflow = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjNtv", date_1, date_2)

# FORMAT CM DATA 

rawtxflow = cmdc.combo_convert(rawtxflow)
txflow = cmdc.combo_convert(txflow)

cmdf = rawtxflow.merge(txflow, on='date', how='left')
print(cmdf)
cmdf['date'] = cmdf['date'].dt.strftime('%Y-%m-%d')

# PULL PRIVACY DATA FROM DCRDATA

Privacy = dcrdata.chart("privacy-participation")
df = pd.DataFrame(Privacy)

ticketPrice = dcrdata.chart("ticket-price")
df1 = pd.DataFrame(ticketPrice)

stkpart = dcrdata.chart("stake-participation")
df11 = pd.DataFrame(stkpart)

# FORMAT PRIVACY DATA FROM DCRDATA 

df['t'] = pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
df.rename(columns={'t': 'date'}, inplace=True)

df['anonymitySet'] = df['anonymitySet'] / 100000000

df = df.drop(columns=['axis', 'bin'])

# FORMAT TICKET DATA FROM DCRDATA 

df1['price'] = df1['price'] / 100000000
df1['dcrtixvol'] = df1['price'] * df1['count'] 
df1['t'] = pd.to_datetime(df1['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

df1.rename(columns={'t': 'date'}, inplace=True)

df2 = df1.groupby('date')['dcrtixvol'].sum()

# FORMAT STAKE PARTICIPATION

df11['t'] = pd.to_datetime(df11['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

df11.rename(columns={'t': 'date'}, inplace=True)
df11 = df11.drop(columns=['axis', 'bin'])

df11['circulation'] = df11['circulation'] / 100000000
df11['poolval'] = df11['poolval'] / 100000000
df11['stakepart'] = df11['poolval'] / df11['circulation']

# MERGE DCRDATA DATAFRAMES

df = df.merge(df2, on='date', how='left').merge(df11, on='date', how='left')

# Merge CM and DCRDATA

findf = cmdf.merge(df, on='date', how='left')

findf.columns = ['date', 'Raw Flows', 'Adj Flows', 'anonymitySet', 'dcrtixvol', 'circulation', 'poolval', 'stakepart']

# CALC NEW METRICS

findf['rawminusprivacy'] = findf['Raw Flows'] - findf['anonymitySet']
findf['142tixvolsum'] = findf['dcrtixvol'].rolling(142).sum()
findf['142dcrvolsum'] = findf['rawminusprivacy'].rolling(142).sum()
findf['raw142hodl'] = findf['142tixvolsum'] / findf['142dcrvolsum']
findf['142hodlreal'] = findf['raw142hodl'] - findf['stakepart']

findf['date'] = pd.to_datetime(findf['date'])

print(findf)

findf.to_excel('hodlconvert.xlsx')

plt.bar(findf['date'], findf['Raw Flows'])
plt.bar(findf['date'], findf['dcrtixvol'])
plt.bar(findf['date'], findf['anonymitySet'])
plt.legend()
plt.show()