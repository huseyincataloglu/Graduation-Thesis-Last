
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from modules.datacleaning import clean_data
from modules import visualization as viz
from modules import utilities as util

st.set_page_config(
    page_title="FishStats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
    

# Veri yükleme
df = pd.read_csv('data/FishStats2018.csv')
df = clean_data(df)

# Başlık
st.markdown("<h1 style = 'text-align: left; color : red;'>FishStats Dashboard </h1>",unsafe_allow_html=True)

st.markdown("""
    <h2 style="font-size:26px;">Welcome to the <strong style="color:red;">FishStats Dashboard</strong>!</h2>
    <p style="font-size:20px;">This <strong style="color:red;">Streamlit</strong> dashboard is built to visualize the global fish catch dataset from <a href="https://www.kaggle.com/datasets/thebumpkin/worldwide-fishing-catch-statitstics-1950-2018" target="_blank">Kaggle</a>.</p>        
    <p style="font-size:20px;">In this main page, you can explore the general information and the dataset. For more detailed analysis, you can access other pages via the sidebar!<p>
    """, 
    unsafe_allow_html=True
)

# Genel Bilgiler
col1, col2, col3 ,col4= st.columns(4)
with col1:
    st.subheader("Total Countries :earth_africa:")
    st.subheader(f"{util.get_total_features(df,"Country")}")
    
with col2:
    st.subheader("Total Species :fish:")
    st.subheader(f"{util.get_total_features(df,"Species")}")

with col3:
    st.subheader("Total Locations :round_pushpin:")
    st.subheader(f"{util.get_total_features(df,"Location")}")

with col4:
    st.subheader("Total Production Methods")
    st.subheader(f"{util.get_total_features(df,"Detail")}")


st.dataframe(df)



# Genel Grafikler








