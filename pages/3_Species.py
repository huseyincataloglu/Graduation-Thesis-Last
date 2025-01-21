import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as ut
from modules import speciesvizualition as speciesviz
from app import df

#Sidebar configurations -- ---- -- -
species = st.sidebar.multiselect("Choose species : ",ut.get_unique_features(df,"Species"))
st.sidebar.divider()
years = st.sidebar.slider("Choose the range of years :",min_value=1950,max_value=2018,value=(1950,2018),step=1)
st.sidebar.divider()
detail =st.sidebar.multiselect("Choose the production methods : ",ut.get_production_detailsby_species(df,species,years)) 
#Sidebar configurations -- ---- -- -


st.markdown("<h1 style='text-align: left;color:red;'>Specy Based Analyses 🐟</h1>",unsafe_allow_html=True)
st.markdown(
    """
    <h2 style="font-size:24px;">Welcome to the <strong style="color:red;">Specy Page</strong>!</h2>
    <p style="font-size:20px;">Here you can explore:</p>
    <ul style="font-size:18px;">
        <li>Total productions by species and differences between them</li>
        <li>Production change based on a specific species for variety years</li>
        <li>Compare production methods for different species</li>
    </ul>
    <p style="font-size:18px;">Use the sidebar to select species and methods to customize your analysis and once you choose the species and the range of years, it will effect all the graphs!</p>
    """, 
    unsafe_allow_html=True
)




st.divider()

col1,col2 = st.columns(2)
with col1:
    st.markdown("<h3>Total Production Amount By Species</h3>", unsafe_allow_html=True)
    st.plotly_chart(speciesviz.plot_species_totalprodamount(df,species,years))
with col2:
    st.markdown("<h3>Distributions of Production Amount By Species Over Years</h3>", unsafe_allow_html=True)
    st.plotly_chart(speciesviz.plot_species_overyears(df,species,years))

st.divider()

st.markdown("<h3>Overview of Total Production by Species and Methods</h3>", unsafe_allow_html=True)
st.plotly_chart(speciesviz.plot_speciesprdouction_by_detail(df,species,years,detail))

st.divider()
st.markdown("<h3>Distributions Of Production by Species and Methods Over Years</h3>", unsafe_allow_html=True)
st.plotly_chart(speciesviz.plot_speciesondetails_overyears(df,species,years,detail))














