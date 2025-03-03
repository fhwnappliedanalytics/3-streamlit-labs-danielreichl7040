
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

st.title('Microsoft Stock Price')

# get the data on a specific stock
tickerSymbol = 'MSFT'
# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2021-01-01', end='2021-12-31')

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)
