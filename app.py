
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

cc1,cc2 = st.columns([1,2])
with cc1:
    choose = st.selectbox("Choose fishery area :",options=list(df.Location.unique()))
    if choose == "Africa - Inland waters":
        st.image("assets/africa_inland waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Asia - Inland waters":
        st.image("assets/Asia_inland_waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Mediterranean and Black Sea":
        st.image("assets/Mediterrian_and_black_sea.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Europe - Inland waters":
        st.image("assets/euroe_inlandwaters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Eastern Central":
        st.image("assets/pacific_eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Oceania - Inland waters":
        st.image("assets/ocenia_inland_waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Southeast":
        st.image("assets/atlantic_southeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Eastern Central":
        st.image("assets/atlantic_eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Western Central":
        st.image("assets/atlantic_western.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "America, North - Inland waters":
        st.image("assets/america_north_inland.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "America, South - Inland waters":
        st.image("assets/america_southinland.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Antarctic":
        st.image("assets/atlantic_antartic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Southwest":
        st.image("assets/Atlantic_ Southwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Antarctic":
        st.image("assets/pacific_antartic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Indian Ocean, Antarctic":
        st.image("assets/Indian Ocean_Antarctic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Indian Ocean, Eastern":
        st.image("assets/Indian Ocean_Eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Southwest":
        st.image("assets/Pacific_Southwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Western Central":
        st.image("assets/Pacific_Western Central.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Indian Ocean, Western":
        st.image("assets/Indian Ocean_Western.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Northeast":
        st.image("assets/Atlantic_Northeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Southeast":
        st.image("assets/Pacific_Southeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Atlantic, Northwest":
        st.image("assets/Atlantlic_northwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Northeast":
        st.image("assets/Pacific_Northeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Pacific, Northwest":
        st.image("assets/Pacific_Northwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
    elif choose == "Arctic Sea":
        st.image("assets/Arctic Sea.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=500)
  


# Genel Grafikler








