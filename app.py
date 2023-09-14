import streamlit as st
from main import *
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Airbnb Analysis")
st.markdown("---")

option = st.selectbox("Choose option", options=["None", "Pull Data", "Show Data"])

if option == 'Pull Data':
    request()

if option == 'Show Data':
    if os.path.exists("airbnb_data.csv"):
        df = pd.read_csv("airbnb_data.csv", index_col=None)
        analysis(df)
        st.markdown("---")
        pie_visualization(df)
        st.markdown("---")
        barplot_visualization(df)
    else:
        st.warning("Please pull the data first using the 'Pull Data' checkbox.", icon="⚠️")


