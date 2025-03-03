
import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Microsoft Stock Price')

# get the data on a specific stock
tickerSymbol = st.text_input('Enter ticker symbol', value='MSFT')

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# validate the ticker symbol
if tickerData.info is None:
    st.error('Error: Ticker symbol not found.')
    st.stop()


# Define the date range for the slider
min_date = pd.to_datetime('2021-01-01').date()
max_date = pd.to_datetime('2023-12-31').date()


# Add a slider to the sidebar. We also ensure to give it a default value.
# Returns a tuple with the selected start and end dates
start_date, end_date = st.sidebar.slider(
    'Select a date range',
    min_value=min_date, 
    max_value=max_date, 
    value=(min_date, max_date),
    format='YYYY-MM-DD'
)

# Convert the selected dates back to pandas timestamps
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)


# Lets also show some information about the company
st.write("""
## Company information
""")
st.write(tickerData.info)

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)

# show daily closing price as table

st.write("""
## Stock information
""")
st.write(tickerDf)
