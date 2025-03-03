import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Function to connect to your PostgreSQL database
@st.cache_resource(hash_funcs={create_engine: id})
def get_connection():
    return create_engine('postgresql://student@mds-dsi-db-23:reRZ2pjg1WxqlwjU@mds-dsi-db-23.postgres.database.azure.com:5432/music_store')


@st.cache_data()
def get_artist_names():
    query = "SELECT name FROM artists;"
    return run_query(query, None)

# Function to run a query and return a DataFrame
def run_query(query, params):
    engine = get_connection()
    return pd.read_sql_query(query, engine, params=params)

# Streamlit UI
st.title('Music Store Data Analysis')

# User input for artist name
artist_names = get_artist_names()
artist_name = st.selectbox('Select an artist:', artist_names['name'])


if artist_name:
    # Query 1: Count of tracks
    query1 = """
    SELECT count(*) 
    FROM tracks
    JOIN public.albums a ON a.id = tracks.album_id
    JOIN public.artists a2 ON a2.id = a.artist_id
    WHERE a2.name = %s;
    """
    count_result = run_query(query1, (artist_name,))
    st.write('### Total Number of Tracks')
    st.write(count_result)

    # Query 2: Tracks count by album
    query2 = """
    SELECT a.title, count(album_id) as tracks_count 
    FROM tracks
    LEFT JOIN albums AS a ON a.id = tracks.album_id
    LEFT JOIN public.artists a2 ON a2.id = a.artist_id
    WHERE a2.name = %s
    GROUP BY title;
    """
    tracks_count_result = run_query(query2, (artist_name,))
    st.write('### Tracks Count by Album')
    st.table(tracks_count_result)

    # Query 3: Total price of albums
    query3 = """
    SELECT al.title, sum(t.unit_price) AS album_price 
    FROM albums AS al
    LEFT JOIN tracks AS t ON t.album_id = al.id
    LEFT JOIN artists AS ar ON ar.id = al.artist_id
    WHERE ar.name = %s
    GROUP BY title;
    """
    album_prices_result = run_query(query3, (artist_name,))
    st.write('### Album Prices')
    st.table(album_prices_result)

    #Query 4: Time series of sales
    time_series_query = """
        SELECT invoice_date, sum(t.unit_price) as total_sales
        FROM invoice_lines
        JOIN public.tracks t ON t.id = invoice_lines.track_id
        JOIN public.albums a ON t.album_id = a.id
        JOIN public.artists a2 ON a2.id = a.artist_id
        JOIN invoices ON invoice_lines.invoice_id = invoices.id
        WHERE a2.name = %s
        GROUP BY invoice_date;
        """
    time_series_result = run_query(time_series_query, (artist_name,))
    if not time_series_result.empty:
        # Convert the invoice_date to datetime for plotting
        time_series_result['invoice_date'] = pd.to_datetime(time_series_result['invoice_date'])
        time_series_result.set_index('invoice_date', inplace=True)

        # Use Streamlit's line_chart to plot the data
        st.write('### Sales Over Time')
        st.line_chart(time_series_result['total_sales'])
