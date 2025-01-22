import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as ut
from modules import countryvizualizations as cviz
from app import df




st.markdown("<h1 style='text-align: center; color : red;'>Country Based Analyses &#127759;</h1>",unsafe_allow_html=True)
st.divider()
st.markdown(
        """
        <h2 style="font-size:28px; text-align:left;">🌍 Welcome to the <strong style="color:red;">Country Analysis Page</strong>! 🌍</h2>
        <p style="font-size:20px; text-align:justify;">
            This page offers powerful tools to explore and analyze fish production data across multiple countries, regions, and production methods. Here's what you can do:
        </p>
       """,unsafe_allow_html=True)
st.divider()

c1,c2 = st.columns(2)
with c1:
    st.markdown(""" <h2 style="font-size:28px; text-align:left; color : red;"> Here is what you can do : </h2> """,unsafe_allow_html=True)

    st.markdown(
        """
        <h3 style="font-size:22px; color:darkgreen;">🔍 Explore Data for a Single Country:</h3>
        <ul style="font-size:18px; list-style-type:square; margin-left:20px;">
            <li>Analyze total production amounts for a specific species or multiple species.</li>
            <li>Observe production trends over time, broken down by regions or production methods.</li>
            <li>Focus on production in specific regions or across all regions.</li>
        </ul>
        <h3 style="font-size:22px; color:darkgreen;">📊 Compare Data Across Multiple Countries:</h3>
        <ul style="font-size:18px; list-style-type:square; margin-left:20px;">
            <li>Compare total production amounts for selected countries.</li>
            <li>Analyze production changes over time for selected countries.</li>
            <li>Examine production in shared regions or based on specific production methods.</li>
            <li>Focus on common fish species or specific fish species across countries.</li>
        </ul>
        """, 
        unsafe_allow_html=True
    )
with c2:
    st.markdown("""
        <h3 style="font-size:22px; color:darkgreen;">⚙️ Customization and Insights:</h3>
        <p style="font-size:18px; text-align:justify;">
            Use the sidebar to customize your analysis by selecting:
            <ul style="font-size:18px; list-style-type:circle; margin-left:40px;">
                <li>Countries and regions of interest.</li>
                <li>Specific fish species or all species.</li>
                <li>Production methods or a combination of methods.</li>
                <li>The range of years for your analysis.</li>
            </ul>
        </p>
    """,unsafe_allow_html=True)

# Sidebar extensions -----------------------------

st.sidebar.title("All Filters")
st.sidebar.divider()

countries = st.sidebar.multiselect("Select Countries",ut.get_uniquefeature(df,"Country"))
st.sidebar.divider()
years = st.sidebar.slider("Choose the range to filter",min_value=1950,max_value=2018,step=1,value=(1950,2018))
st.sidebar.divider()
locations = st.sidebar.multiselect("Filter Fishing Areas :",ut.get_commonlocations_forcountries(df,countries,years))
st.sidebar.divider()
if len(locations) == 0: 
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandcountry(df,countries,years))
else:
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandcountry(df,countries,years,locations))

st.sidebar.divider()
if len(locations) == 0:
    if len(methods) == 0:
        species = st.sidebar.multiselect("Select Species",ut. get_species_bycountries(df,countries,years))
    else:
        species = st.sidebar.multiselect("Select Species",ut. get_species_bycountries(df,countries,years,methods = methods))
else:
    if len(methods) == 0:
        species = st.sidebar.multiselect("Select Species:",ut.get_species_bycountries(df,countries,years,locations))
    else:
        species = st.sidebar.multiselect("Select Species:",ut.get_species_bycountries(df,countries,years,locations,methods))

#Sidebar extensions -------------------------------

st.divider()
if len(methods) == 0:
    st.plotly_chart(cviz.plot_countries_prod_map(df,countries,years,locations),key="production_map_2")
else:
    st.plotly_chart(cviz.plot_countries_prod_map(df,countries,years,locations,methods=methods))


col1 , col2 = st.columns(2)
with col1:
    st.markdown("<h3>Total Production Amount By Countries</h3>", unsafe_allow_html=True)
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countries_by_production(df,countries,years,locations))
    else:
        st.plotly_chart(cviz.plot_countries_by_production(df,countries,years,locations,methods=methods))    
with col2:
    st.markdown("<h3 style='text-align: left;'>Countries Production Distribution In Years</h3>", unsafe_allow_html=True)
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countryprod_by_time(df,countries,years,locations))
    else:
        st.plotly_chart(cviz.plot_countryprod_by_time(df,countries,years,locations,methods=methods))



st.divider()
st.markdown("<h3 style='text-align:left;'> Total Productions Of Countries By Species</h3>", unsafe_allow_html=True)
if len(locations) == 0:
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countrieswithspecies(df,countries,species,years))      
    else:
        st.plotly_chart(cviz.plot_countrieswithspecies(df,countries,species,years,methods=methods))
else:
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countrieswithspecies(df,countries,species,years,locations))
    else:
        st.plotly_chart(cviz.plot_countrieswithspecies(df,countries,species,years,locations,methods))





st.divider()

st.markdown("<h3 style='text-align: left;'>Species Production Distribution Of Countries In Years</h3>",unsafe_allow_html=True)
if len(locations) == 0:
    if len(methods) == 0:
            st.plotly_chart(cviz.plot_countryspeciesprod_by_time(df,countries,species,years))    
    else:
            st.plotly_chart(cviz.plot_countryspeciesprod_by_time(df,countries,species,years,methods=methods)) 
else:
    if len(methods) == 0:
            st.plotly_chart(cviz.plot_countryspeciesprod_by_time(df,countries,species,years,locations=locations))
    else:
            st.plotly_chart(cviz.plot_countryspeciesprod_by_time(df,countries,species,years,locations=locations,methods=methods)) 

    



st.divider()

st.markdown("<h3 style='text-align: left;'> Production Methods Of Countries By Total Amount </h3>",unsafe_allow_html=True)
if len(locations) == 0:
    st.plotly_chart(cviz.plot_country_productiondetail(df,countries,years))
else:
    st.plotly_chart(cviz.plot_country_productiondetail(df,countries,years,locations))






