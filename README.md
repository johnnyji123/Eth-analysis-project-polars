### Ethereum (ETH) Price Analysis Project
### Overview: This project utilizes Python along with the libraries Polars, Seaborn, Matplotlib, and Yfinance to analyze and visualize the historical performance of Ethereum (ETH) cryptocurrency. The project covers various aspects, including price trends, volatility, correlation between price and volume. The project starts by fetching historical data for Ethereum using the Yahoo Finance API (yfinance library). The data is then converted into a Polars DataFrame for efficient manipulation.
### Technologies used:
* Python
* Polars
* Seaborn
* Matplotlib
* Yfinance API
  
### Volume Analysis
* The project analyzes the volume trends over time, calculating the percentage change in volume.
* Visualizations are created to illustrate volume trends and changes.

### Price Change Analysis
* Percentage changes in closing prices are calculated and analyzed.
* The project identifies periods of significant price changes and volatility.

### Volatility:
* Volatility is measured using standard deviation and mean of closing prices.
* Coefficient of variation is calculated to determine the stability of closing prices.
* 
### Moving Average and Trend Analysis
* A 200-day Moving Average (MA) is calculated to determine trends.
* The project visualizes closing prices alongside the 200-day MA to identify trends.
  
### Correlation Analysis
* The correlation coefficient between closing prices and volume is calculated.
* The project explores the relationship between price and volume.


 ### Conclusion from my analysis

 ### Volume Analysis
 * Overall, the volume of Ethereum increased from 2019 to 2021 but at a diminishing rate.
 * The percentage increase in volume remained positive but decreased.
 * From 2022 to 2023, there was a negative percentage change in volume, indicating a decrease.
 * 2019 had the greatest increase in volume, while 2023 had the greatest decrease.

### Price Trends
* Price trends over time show a steady increase from 2018 to 2020.
* A sharp increase in price occurred from 2020 to 2021.
* Prices have gradually decreased from 2021 to 2023.

### Price Change Analysis:
* In 2021, there was the greatest percentage change in price.
* In 2022 and 2023, prices have been decreasing.
* Percentage changes in price indicate significant volatility, with the potential for both gains and losses.

### Volatility Measurement
* Volatility was measured based on the standard deviation and mean of closing prices
* The coefficient of variation (ratio of standard deviation to mean) was used to assess stability.
* 2020 was the most volatile year, with the highest coefficient of variation.
* 2023 was the least volatile year, indicating more stable closing prices.

### Moving Average and Trend Analysis
* The 200-day Moving Average (MA) was used to determine trends.
* When the MA was consistently below the closing price, it showed an upward trend. This was the case between 2018-2021.
* From the later half of 2021, the MA was above the closing price, indicating a bearish trend.

### Correlation Analysis
* The correlation coefficient between closing prices and volume was 0.75, indicating a strong positive correlation.
* Price and volume are likely to be strongly related; as one variable increases, so does the other.























