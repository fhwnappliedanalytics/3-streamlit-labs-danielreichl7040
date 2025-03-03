
import yfinance as yf
import streamlit as st
import pandas as pd
import datetime

st.write('# Financials')
st.write('This app is a demo version of Streamlit')

st.sidebar.subheader('Stock selection in sidebar')
st.sidebar.write('Select your stock')
stocks = st.sidebar.multiselect('Stock option?', ['AAPL', 'AMZN', 'MSFT', 'GOOGL'])

min_date = datetime.date(2020, 1, 1)
max_date = datetime.date(2023, 1, 1)
min_selected, max_selected = st.sidebar.date_input('Pick date', (min_date, max_date))
"This is the selected dates", min_selected, max_selected

# Checking if any stock is selected
if stocks:
    combined_closing = pd.DataFrame()
    combined_volume = pd.DataFrame()

    for stock in stocks:
        # Get historical data for each stock
        ticker_data = yf.Ticker(stock)
        ticker_df = ticker_data.history(period='1d', start=min_selected, end=max_selected)

        # Append closing prices and volumes to the combined dataframes
        combined_closing[stock] = ticker_df['Close']
        combined_volume[stock] = ticker_df['Volume']

    # Plotting the combined closing prices
    st.write('## Combined Closing Price')
    st.line_chart(combined_closing)

    # Plotting the combined volumes
    st.write('## Combined Volume')
    st.line_chart(combined_volume)

else:
    st.write('Please select at least one stock to display data.')

