import pandas as pd
import numpy as np
from pandas_datareader import data, wb
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
sns.set_style('whitegrid')
import plotly as py
import plotly.express as px
import cufflinks as cf
cf.go_offline()

# Figure out how to get the stock data from Jan 1st 2006 to Jan 1st 2016 for each of these banks
#  Set each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol

start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)
# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)
# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)
# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)
# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)
# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)
# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

# Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

# Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks.
# Set the keys argument equal to the tickers list. Also pay attention to what axis you concatenate on.**
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)
bank_stocks.head()
# Set the column name levels
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']

# What is the max Close price for each bank's stock throughout the time period?
bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()

# Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock.
returns = pd.DataFrame()

# Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()

#  Create a pairplot using seaborn of the returns dataframe
sns.pairplot(returns[1:])
plt.show()

# Worst Drop
returns.idxmin()

#Best Single Day Gain
returns.idxmax()

# Riskiest stock based on standard deviation
returns.std()

# Riskiest stock in 2015 based on standard deviation
returns.loc['2015-01-01':'2015-12-31'].std()

# Create a distplot using seaborn of the 2015 returns for Morgan Stanley
sns.displot(returns.loc['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=100)
plt.show()

# Create a distplot using seaborn of the 2008 returns for CitiGroup
sns.displot(returns.loc['2008-01-01':'2008-12-31']['C Return'],color='red',bins=100)
plt.show()

# Create a line plot showing Close price for each bank for the entire index of time.
for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()
plt.show()

# bank_stocks['Year'] = bank_stocks['Date'].apply(lambda date: date.year)
# or
# bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()
# or
#fig = px.line(bank_stocks,x='Year', y='Close',title='Closing Prices')
#fig.show()
#fig1 = bank_stocks.xs(key='Close',axis=1,level='Stock Info').iplot(kind='spread', asFigure=True)  <-only comment that works here (ish)
#py.offline.plot(fig1)

# Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008
plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='BAC 30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC Close')
plt.legend()
plt.show()

# Create a heatmap of the correlation between the stocks Close Price
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True,cmap='coolwarm')
plt.show()

# Use seaborn's clustermap to cluster the correlations together
sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True,cmap='coolwarm')
plt.show()
