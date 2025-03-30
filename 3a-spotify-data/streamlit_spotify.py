import streamlit as st
import pandas as pd

# Load CSVs
df_tracks = pd.read_csv('./data/csv_files/SpotGenTrack/Data Sources/spotify_tracks.csv')
df_artists = pd.read_csv('./data/csv_files/SpotGenTrack/Data Sources/spotify_artists.csv')

# App Title
st.title('Spotify Track App')

# Explode Artists 
df_tracks['artists_id'] = df_tracks['artists_id'].apply(eval)  # <- wichtig, falls als String gespeichert
track_exploded = df_tracks.explode('artists_id')

# Join mit Artists
df_artists = df_artists.rename(columns={'id': 'artists_id', 'name': 'artist_name'})
merged_df = track_exploded.merge(df_artists[['artists_id', 'artist_name', 'genres']], on='artists_id', how='left')

# Input-Feld für den User
search_term = st.text_input('🎵 Enter a track name:')

# Filtern, falls was eingegeben wurde
if search_term:
    # Case-insensitive using CASE=FALSE
    results = merged_df[merged_df['name'].str.contains(search_term, case=False, na=False)]

    if not results.empty:

        results_to_display = results[['name', 'artist_name', 'genres']].drop_duplicates()

        st.write(f"### Gefundene Ergebnisse für: `{search_term}`")
        for i, row in results_to_display.iterrows():
            st.markdown(f"**🎧 Track:** {row['name']}  \n"
                        f"**👤 Artist:** {row['artist_name']}  \n"
                        f"**🎼 Genre:** {', '.join(eval(row['genres'])) if isinstance(row['genres'], str) else 'Keine Angabe'}")
            st.markdown("---")
    else:
        st.warning("Keine Treffer gefunden.")