import pandas as pd
import polars as pl
import seaborn as sns
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt

cryptocurrency = ["ETH-USD"]

df = yf.download(cryptocurrency, period = '5y')
df = df.reset_index()
df = pl.from_pandas(df)



# find volume over time
df = df.with_columns(
    pl.col("Date").dt.year(),
    pl.col("Open").round(decimals = 2),
    pl.col("High").round(decimals = 2),
    pl.col("Low").round(decimals = 2),
    pl.col("Close").round(decimals = 2),
    pl.col("Adj Close").round(decimals = 2)
    )   


avg_df = df.group_by("Date").agg(
        pl.col("Open").mean(),
        pl.col("High").mean(),
        pl.col("Low").mean(),
        pl.col("Close").mean(),
        pl.col("Adj Close").mean(),
        pl.col("Volume").mean()
    )


avg_df = avg_df.sort("Date", descending = False)

pl.Config(set_fmt_float = "full")

    
avg_df = avg_df.with_columns(
    pl.col("Open").round(decimals = 2),
    pl.col("High").round(decimals = 2),
    pl.col("Low").round(decimals = 2),
    pl.col("Close").round(decimals = 2),    
    pl.col("Adj Close").round(decimals = 2),
    pl.col("Volume").round(decimals = 2)
    
    )


# Volume was still increasing between 2019 to 2021 but there is a diminishing rate of growth
# Pct increase is still postivie but decreasing
# From 2022-2023 pct change is negative - indicating a decrease in volume
# 2019 Had the greatest increase in volume, 2023 had the greatest decrease in volume  
volume_change_over_time_df = avg_df.select(
    pl.col("Date"),
    pl.col("Volume"),
    (pl.col("Volume").pct_change() * 100).alias("pct change volume")
    )

    

# price trends over time
price_over_time = sns.lineplot(x = "Date", y = "Close", data = avg_df)
price_over_time.set(title = "Price over time", ylabel = "Closing price")

# Annotated the price on the lineplot
# Price has steadily increased from 2018 to 2020
# From 2020-2021 there was a sharp increase in price
# Price gradually decreasing from 2021-2023
def plot_price_over_time(df):
    for year in df["Date"].unique().to_list():
        point_coordinates = df.filter(pl.col("Date") == year)
        for row in point_coordinates.to_pandas().itertuples(index = False):
            plt.text(row.Date, row.Close, f"{row.Close}", ha = "left", va = "bottom")

            
#plot_price_over_time(avg_df)     
    
# 2021 had the greatest pct change in price 
# In 2022 and 2023 price has been decreasing
pct_change_price_df = avg_df.select(
    pl.col("Date"),
    pl.col("Close"),
    (pl.col("Close").pct_change() * 100).alias("pct_change")
    
    )      


        
# Measuring volatility based on standard deviation and mean
volatility_df = df.with_columns(
        pl.col("Open").round(decimals = 2),
        pl.col("High").round(decimals = 2),
        pl.col("Low").round(decimals = 2),
        pl.col("Close").round(decimals = 2),
        pl.col("Adj Close").round(decimals = 2)
    
    )

volatility_df

close_std = volatility_df.groupby("Date").agg(
        pl.col("Close").std().alias("Close std")
    
    )

close_std = close_std.sort("Date", descending = False)

avg_price = volatility_df.groupby("Date").agg(
        pl.col("Close").mean().round(decimals = 2).alias("avg close")
    )


avg_price = avg_price.sort("Date", descending = False)
avg_price


# merge avg price and std df
merged_avg_std_df = avg_price.join(close_std, on = "Date", how = "outer")
merged_avg_std_df = merged_avg_std_df.with_columns(
        pl.col("Close std").round(decimals = 2),
        (pl.col("Close std") / pl.col("avg close")).alias("Coefficient variation")
    
)

# 2020 Coefficient variation was the highest - was the most volatile year in terms of closing prices
# 2020 Coefficient variation not close to 0 = indicates closing prices did deviate quite a bit from average. 
# This indicates there were quite a number of fluctuations in closing prices in this year
# 2023 the least volatile year - Coefficient variation was the lowest in this year
# Indicates that closing prices were more stable - closing prices were not far off from the mean

merged_avg_std_df = merged_avg_std_df.with_columns(pl.col("Coefficient variation").round(decimals = 2))
merged_avg_std_df = merged_avg_std_df.sort("Coefficient variation", descending = True) 
merged_avg_std_df
             

# Calculating 200 day MA to determine volatility
# MA consistently below closing price = shows upward trend - recent closing prices = higher than historical average
# MA above closing price from later half of 2021 = shows bearish trend - recent closing prices = lower than historical average price
df = df.with_columns(
    pl.col("Close").rolling_mean(window_size = 200).alias("200 day MA")
        
    )

sns.lineplot(x = "Date", y = "Close", label = "closing price", data = df)
sns.lineplot(x = "Date", y = "200 day MA", label = "200 day MA", data = df)
