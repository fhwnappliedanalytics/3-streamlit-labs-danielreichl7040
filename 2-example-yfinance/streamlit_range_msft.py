
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

# add a slider to the sidebar. We also ensure to give it a default value.
# We will add a validation ensure that the start date is always before the end date.
start_date = st.sidebar.date_input('Start date', value=pd.to_datetime('2021-01-01'))
end_date = st.sidebar.date_input('End date', value=pd.to_datetime('2021-12-31'))
if start_date > end_date:
    st.sidebar.error('Error: End date must fall after start date.')


# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)
