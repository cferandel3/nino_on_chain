import coinmetrics
import matplotlib.pyplot as plt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"
asset2 = "btc"

#fetch desired data
date_1 = "2016-02-08"
date_2 = "2020-05-05"

bchain = cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)

bchain2 = cm.get_asset_data_for_time_range(asset2, "BlkSizeByte", date_1, date_2) 
price2 = cm.get_asset_data_for_time_range(asset2, "CapMrktCurUSD", date_1, date_2)

price3 = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
# clean CM data
bchain_clean = cm_data_converter.cm_data_convert(bchain)
price_clean = cm_data_converter.cm_data_convert(price)

bchain_clean2 = cm_data_converter.cm_data_convert(bchain2)
price_clean2 = cm_data_converter.cm_data_convert(price2)

price_clean3 = cm_data_converter.cm_data_convert(price3)
# convert to pandas
df = pd.DataFrame(bchain_clean)
df_1 = pd.DataFrame(price_clean)

df_2 = pd.DataFrame(bchain_clean2)
df_3 = pd.DataFrame(price_clean2)

df_4 = pd.DataFrame(price_clean3)
# calculate blockchain size
size = df.cumsum()
size2 = df_2.cumsum()
# calculate market cap / blockchain size
ratio = df_1 / size
ratio2 = df_3 / size2

altbtc_ratio = ratio / ratio2

print(altbtc_ratio)
# send to excel
#ratio.to_excel('value_stored.xlsx')
# plot ratio and market cap
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(altbtc_ratio)
plt.yscale('log')
plt.title("VALUE STORED / BYTE RATIO")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df_4)
plt.title("ALTBTC PRICE")
plt.yscale('log')
plt.show()