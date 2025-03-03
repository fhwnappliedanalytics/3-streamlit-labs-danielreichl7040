
import streamlit as st
import pandas as pd
import numpy as np

# Title of the app
st.title('My Streamlit App')

# Adding a slider
slider_val = st.slider('Slide me', min_value=0, max_value=100)

# Display the value
st.write(f'You selected: {slider_val}')

# Display a dataframe
df = pd.DataFrame(np.random.randn(10, 5), columns=('col %d' % i for i in range(5)))
st.dataframe(df)
