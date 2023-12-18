import pandas as pd
import polars as pl
import seaborn as sns
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from fbprophet import Prophet
import pystan


cryptocurrency = ["ETH-USD"]

# Connecting to Yfinance API
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

# Calculating the averages of all the columns
avg_df = df.group_by("Date").agg(
        pl.col("Open").mean(),
        pl.col("High").mean(),
        pl.col("Low").mean(),
        pl.col("Close").mean(),
        pl.col("Adj Close").mean(),
        pl.col("Volume").mean()
    )


avg_df = avg_df.sort("Date", descending = False)

# Converting Scientific notation to float
pl.Config(set_fmt_float = "full")

# Rounding decimals to 2    
avg_df = avg_df.with_columns(
    pl.col("Open").round(decimals = 2),
    pl.col("High").round(decimals = 2),
    pl.col("Low").round(decimals = 2),
    pl.col("Close").round(decimals = 2),    
    pl.col("Adj Close").round(decimals = 2),
    pl.col("Volume").round(decimals = 2)
    
    )


# Analysing volume over time
volume_change_over_time_df = avg_df.select(
    pl.col("Date"),
    pl.col("Volume"),
    (pl.col("Volume").pct_change() * 100).alias("pct change volume")
    )
    
    

# price trends over time plotted using sesaborn
price_over_time = sns.lineplot(x = "Date", y = "Close", data = avg_df)
price_over_time.set(title = "Price over time", ylabel = "Closing price")


# Function to Annotate the lineplot with its values
def plot_price_over_time(df):
    for year in df["Date"].unique().to_list():
        point_coordinates = df.filter(pl.col("Date") == year)
        for row in point_coordinates.to_pandas().itertuples(index = False):
            plt.text(row.Date, row.Close, f"{row.Close}", ha = "left", va = "bottom")

            
plot_price_over_time(avg_df)     
    

# Caclulating pct change in price
pct_change_price_df = avg_df.select(
    pl.col("Date"),
    pl.col("Close"),
    (pl.col("Close").pct_change() * 100).alias("pct_change")
    
    )      


        
volatility_df = df.with_columns(
        pl.col("Open").round(decimals = 2),
        pl.col("High").round(decimals = 2),
        pl.col("Low").round(decimals = 2),
        pl.col("Close").round(decimals = 2),
        pl.col("Adj Close").round(decimals = 2)
    
    )

volatility_df


# Measuring volatility based on standard deviation and mean
close_std = volatility_df.groupby("Date").agg(
        pl.col("Close").std().alias("Close std")
    
    )

close_std = close_std.sort("Date", descending = False)


# Finding the average close price
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


# Finding the Coefficient Variation
merged_avg_std_df = merged_avg_std_df.with_columns(pl.col("Coefficient variation").round(decimals = 2))
merged_avg_std_df = merged_avg_std_df.sort("Coefficient variation", descending = True) 
merged_avg_std_df
             

# Finding 200 day Moving average across all years
df = df.with_columns(
    pl.col("Close").rolling_mean(window_size = 200).alias("200 day MA")
            
    )

# Plotting close price and MA on lineplot
sns.lineplot(x = "Date", y = "Close", label = "closing price", data = df)
sns.lineplot(x = "Date", y = "200 day MA", label = "200 day MA", data = df)


# Selecting relevant columns
price_volume_df = avg_df.select(
    pl.col("Date"),
    pl.col("Close"),    
    pl.col("Volume")
    )


# Calculating Correlation coefficient between price and volume
price_volume_df = price_volume_df.with_columns(
        pl.corr("Close", "Volume").alias("Correlation coefficient")
    )

price_volume_df = price_volume_df.with_columns(pl.col("Correlation coefficient").round(decimals = 2))
price_volume_df




