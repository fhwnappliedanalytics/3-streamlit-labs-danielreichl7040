import streamlit as st
import pandas as pd
from pymongo import MongoClient

import credentials as cr

@st.cache_data
def load_data():
    client = MongoClient(f'mongodb+srv://{cr.user}:{cr.password}@{cr.host}')
    db = client.get_database('sample_training')
    return pd.DataFrame(db.citibike.trips.find())

def render_info():
    st.title('Citibike data')
    st.header('Displaying the citibike dataset')
    st.markdown('Using streamlit to filter and display data fetched from a mongodb database.')

def filter_by_usertype(data):
    user_type = st.sidebar.selectbox('Filter by different user types:', [''] + list(data['usertype'].drop_duplicates()))
    if user_type:
        return data[data['usertype']==user_type]
    return data

def filter_by_tripduration(data):
    # adding a range slider, allowing to choose values in range
    range = st.sidebar.slider('Trip duration', min(data['tripduration']//3600), max(data['tripduration']//3600), (20,40))
    return data[( (data['tripduration']//3600).between(*range))]

def render_map(data):
    df_map = pd.DataFrame([pd.Series(point['coordinates'],index=['lon','lat']) for point in data['start station location']], columns=['lon','lat'])
    st.map(df_map)

render_info()

data = load_data()

data = filter_by_usertype(data)
data = filter_by_tripduration(data)
render_map(data)
