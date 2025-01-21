import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as ut
from modules import countryvizualizations as cviz
from app import df




st.markdown("<h1 style='text-align: left; color : red;'>Country Based Analyses &#127759;</h1>",unsafe_allow_html=True)

st.markdown(
    """
    <h2 style="font-size:24px;">Welcome to the <strong style="color:red;">Country Page</strong>!</h2>
    <p style="font-size:20px;">Here you can explore:</p>
    <ul style="font-size:18px;">
        <li>Total productions by countries and compare them</li>
        <li>Production change based on a specific species for variety years</li>
        <li>Compare production methods for different countries</li>
    </ul>
    <p style="font-size:18px;">Use the sidebar to select countries and species to customize your analysis and once you choose the countries and the range of years, it will effect all the graphs!</p>
    <p style ="font-size:18px;"><strong>Remind : If you have chosen common species, dont choose uncommon specy because it wont make any change.</strong> </p> 
    """, 
    unsafe_allow_html=True
)

st.divider()
# Sidebar extensions -----------------------------
countries = st.sidebar.multiselect("Select Countries :",ut.get_unique_features(df,"Country"),default=["Japan","Indonesia"])
st.sidebar.divider()
years = st.sidebar.slider("Choose the range to filter",min_value=1950,max_value=2018,step=1,value=(1950,2018))
st.sidebar.divider()
species_common = st.sidebar.multiselect("Common species for your country chooses",ut.get_commonspecies_forcountries(df,countries,years))
species = st.sidebar.multiselect("Select Species",ut. get_species_bycountries(df,countries,years))
#Sidebar extensions -------------------------------


col1 , col2 = st.columns(2)
with col1:
    st.markdown("<h3>Total Production Amount By Countries</h3>", unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countries_by_production(df,countries,years))

with col2:
    st.markdown("<h3 style='text-align: left;'>Countries Production Distribution In Years</h3>", unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countryprod_by_time(df,countries,years))


st.divider()

if len(species_common) == 0:
    st.markdown("<h3 style='text-align:left;'> Total Productions Of Countries By Species</h3>", unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countrieswithspecies(df,countries,species,years))
else:
    st.markdown("<h3 style='text-align:left;'> Total Productions Of Countries By Species</h3>", unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countrieswithcommonspecies(df,countries,species_common,years))


st.divider()

if len(species_common) == 0:
    st.markdown("<h3 style='text-align: left;'>Species Production Distribution Of Countries In Years</h3>",unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countryspeciesprod_by_time(df,countries,species,years))    
else:
    st.markdown("<h3 style='text-align: left;'>Species Production Distribution Of Countries In Years</h3>",unsafe_allow_html=True)
    st.plotly_chart(cviz.plot_countrycommonspeciesprod_by_time(df,countries,species_common,years))


st.divider()

st.markdown("<h3 style='text-align: left;'> Production Detail Of Countries By Total Amount </h3>",unsafe_allow_html=True)
st.plotly_chart(cviz.plot_country_productiondetail(df,countries,years))






