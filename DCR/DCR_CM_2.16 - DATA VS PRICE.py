import coinmetrics
import cm_data_converter as cmdc
import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-08-03"

mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
blk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date_1, date_2))
dcrbtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))

df = mcap.merge(blk, on='date', how='left').merge(dcrbtc, on='date', how='left')
df.columns = ['date', 'mcap', 'blkdata', 'PriceBTC']

# Calc Metrics

df['142data'] = df['blkdata'].rolling(142).mean()
df['28data'] = df['blkdata'].rolling(28).mean()
df['cumsumdata'] = df['blkdata'].cumsum()

# Plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
line1 = ax1.plot(df['date'], df['PriceBTC'], color='w')
ax1.set_ylabel("Market Cap", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Market Cap vs Data Added to Chain per Day", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
""" ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

ax11 = ax1.twinx()
""" ax11.bar(df['date'], df['cumsumdata'], color='lime', alpha=0.5) """
ax11.bar(df['date'], df['blkdata'], color='aqua', alpha=0.5)
ax11.plot(df['date'], df['142data'], color='r')
ax11.plot(df['date'], df['28data'], color='lime')
ax11.set_ylabel("Bytes Added Per Day", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax11.legend(loc='upper left')

plt.show()