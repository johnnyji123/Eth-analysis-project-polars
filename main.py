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
    pl.col("Date").dt.year() 
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
volatility_df = avg_df.with_columns(
        pl.col("Open").round(decimals = 2),
        pl.col("High").round(decimals = 2),
        pl.col("Low").round(decimals = 2),
        pl.col("Close").round(decimals = 2),
        pl.col("Adj Close").round(decimals = 2),
        pl.col("Voume").round(decimals = 2)
    
    )

volatility_df
