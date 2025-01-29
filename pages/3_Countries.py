import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as ut
from modules import countryvizualizations as cviz
from app import df




# Page Header
st.markdown("<h1 style='text-align: center; color : red;'>Country Based Analyses &#127759;</h1>", unsafe_allow_html=True)
st.divider()

# Main Introduction
st.markdown(
    """
    <h2 style="font-size:28px; text-align:left;">🌍 Welcome to the <strong style="color:red;">Country Analysis Page</strong>! 🌍</h2>
    <p style="font-size:20px; text-align:justify;">
        This page offers powerful tools to explore and analyze fish production data across multiple countries, regions, and production methods. Here's what you can do:
    </p>
    """, unsafe_allow_html=True)
st.divider()

# Content Layout with Columns
c1, c2 = st.columns(2)

with c1:
    st.markdown(""" <h2 style="font-size:28px; text-align:left; color : red;"> Here's What You Can Do: </h2> """, unsafe_allow_html=True)

    st.markdown(
        """
        <h3 style="font-size:22px; color:darkgreen;">🔍 Explore Data for a Single Country:</h3>
        <ul style="font-size:18px; list-style-type:square; margin-left:20px;">
            <li>Analyze total production amounts for specific species or multiple species.</li>
            <li>Observe production trends over time, broken down by regions or production methods.</li>
            <li> You can also see the frequencies and distributions.</li>
            <li>Focus on production in specific regions or across multiple regions.</li>
        </ul>
        <h3 style="font-size:22px; color:darkgreen;">📊 Compare Data Across Multiple Countries:</h3>
        <ul style="font-size:18px; list-style-type:square; margin-left:20px;">
            <li>Compare total production distributions and frequencies for selected countries.</li>
            <li>Compare total production amounts for selected countries.</li>
            <li>Analyze production changes over time for selected countries.</li>
            <li>Examine production in shared regions or based on specific production methods.</li>
            <li>Focus on common fish species or specific species across countries.</li>
        </ul>
        """, 
        unsafe_allow_html=True
    )

with c2:
    st.markdown(""" 
        <h3 style="font-size:22px; color:darkgreen;">⚙️ Customize Your Analysis:</h3>
        <p style="font-size:18px; text-align:justify;">
            Use the sidebar to customize your analysis by selecting:
            <ul style="font-size:18px; list-style-type:circle; margin-left:40px;">
                <li>Countries and regions of interest.</li>
                <li>Specific fish species or multiple species.</li>
                <li>Production methods or combinations of methods.</li>
                <li>The range of years for your analysis.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

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

st.header("Frequencies and Distributions")
st.write("--------------------")
choose = st.selectbox("Choose graph",options = ["Poduction Distributions In Single Year","Annualy Total Prod Box","Total Participation Frequency","Total Participation and Total Porduction Corelation"])

if choose == "Annualy Total Prod Box":
    if len(locations) == 0:
        if len(methods) == 0:
            st.plotly_chart(cviz.plot_proddist_boxplot(df,countries,years))
        else:
            st.plotly_chart(cviz.plot_proddist_boxplot(df,countries,years,methods=methods))
    else:
        if len(methods) == 0:
            st.plotly_chart(cviz.plot_proddist_boxplot(df,countries,years,locations=locations))
        else:
            st.plotly_chart(cviz.plot_proddist_boxplot(df,countries,years,methods=methods,locations=locations))
elif choose == "Poduction Distributions In Single Year":
    years1 = st.multiselect("Select Year:",options=[str(year) for year in range(years[0],years[1]+1)])
    if len(locations) == 0:
        if len(methods) == 0:
            st.plotly_chart(cviz. plot_proddist_yearly(df,countries,years1))
        else:
            st.plotly_chart(cviz. plot_proddist_yearly(df,countries,years1,methods=methods))
    else:
        if len(methods) == 0:
            st.plotly_chart(cviz. plot_proddist_yearly(df,countries,years1,locations=locations))
        else:
            st.plotly_chart(cviz. plot_proddist_yearly(df,countries,years1,methods=methods,locations=locations))                
elif choose == "Total Participation Frequency":
    if len(locations) == 0:
        if len(methods) == 0:
            st.plotly_chart(cviz. plot_participation_by_country(df,countries,years))
        else:
            st.plotly_chart(cviz. plot_participation_by_country(df,countries,years,methods=methods))
    else:
        if len(methods) == 0:
            st.plotly_chart(cviz.plot_participation_by_country(df,countries,years,locations=locations))
        else:
            st.plotly_chart(cviz.plot_participation_by_country(df,countries,years,methods=methods,locations=locations))
elif choose == "Total Participation and Total Porduction Corelation":
    if len(locations) == 0:
        if len(methods) == 0:
            st.plotly_chart(cviz. plot_partvsprod_by_country(df,countries,years))
        else:
            st.plotly_chart(cviz. plot_partvsprod_by_country(df,countries,years,methods=methods))
    else:
        if len(methods) == 0:
            st.plotly_chart(cviz.plot_partvsprod_by_country(df,countries,years,locations=locations))
        else:
            st.plotly_chart(cviz.plot_partvsprod_by_country(df,countries,years,methods=methods,locations=locations))

            
    




column1 , column2 = st.columns([1,1])
with column1:
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countries_prod_map(df,countries,years,locations),key="production_map_2")
    else:
        st.plotly_chart(cviz.plot_countries_prod_map(df,countries,years,locations,methods=methods))


#st.divider()
#st.markdown("<h3>Total Production Amount By Countries</h3>", unsafe_allow_html=True)
#if len(methods) == 0:
#    st.plotly_chart(cviz.plot_countries_by_production(df,countries,years,locations))
#else:
#    st.plotly_chart(cviz.plot_countries_by_production(df,countries,years,locations,methods=methods))

with column2:
    if len(methods) == 0:
        st.plotly_chart(cviz.plot_countryprod_by_time(df,countries,years,locations))
    else:
        st.plotly_chart(cviz.plot_countryprod_by_time(df,countries,years,locations,methods=methods))



st.write("-------------")

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


if len(locations) == 0:
    st.plotly_chart(cviz.plot_country_productiondetail(df,countries,years))
else:
    st.plotly_chart(cviz.plot_country_productiondetail(df,countries,years,locations))






