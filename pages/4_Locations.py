import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules import utilities as ut
from modules import locationvisualizations as locviz
from app import df

st.markdown("<h1 style='text-align: center; color : red;'>Location Based Analyses</h1>",unsafe_allow_html=True)
st.write("-----------------")
st.markdown(
    """
    <h2 style="font-size:28px; text-align:left;"> Welcome to the <strong style="color:red;">Location Based Analyses</strong>!</h2>
    <p style="font-size:20px; text-align:justify;">
        This page offers powerful tools to explore and analyze fish production data across multiple locations, countries, and production methods.
    </p>
    """, unsafe_allow_html=True)
st.write("-----------------")
column1,column2 = st.columns(2)
with column1:
    st.markdown(""" <h2 style="font-size:28px; text-align:left; color : red;"> Here's What You Can Do: </h2> """, unsafe_allow_html=True)

    st.markdown("""
 

    ### 🎛️ Filters  
    - **Location Selection**: Choose the relevant locations.  
    - **Year Range**: Filter data between the years 1950 and 2018.  
    - **Country Filter**: Narrow down the countries based on selected locations.  
    - **Production Method**: Filter based on the production method.  
    - **Species Selection**: Analyze data by selecting specific species.  
    """
    )
with column2:    
    st.markdown("""
    ### 📊 Visualization Options  
    - **Annual Production Distribution (Boxplot)**: Displays the annual total production distribution for selected locations.  
    - **Total Participation Frequency**: Analyzes the participation frequency by location.  
    - **Participation and Production Correlation**: Shows the correlation between participation and production.  
    - **Production Distribution in a Single Year**: Displays the production distribution for selected year(s).  

    ### 🗺️ Map Visualization  
    Explore the production distributions of countries on a world map based on selected locations.  

    📌 **Use the filters on the left to customize your analysis!**  
    """)
   


st.sidebar.title("All Filters")
st.sidebar.divider()
locations = st.sidebar.multiselect("Choose locations : ",ut.get_uniquefeature(df,"Location"))
st.sidebar.divider()
years = st.sidebar.slider("Choose the range to filter",min_value=1950,max_value=2018,step=1,value=(1950,2018))
st.sidebar.divider()
countries = st.sidebar.multiselect("Filter Countries:",ut.get_commoncountr_forlocs(df,locations,years))
st.sidebar.divider()
if len(countries) == 0: 
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandcount(df,locations,years))
else:
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandcount(df,locations,years,countries))
st.sidebar.divider()
if len(countries) == 0:
    if len(methods) == 0:
        species = st.sidebar.multiselect("Select Species",ut. get_species_bycountlocmethd(df,locations,years))
    else:
        species = st.sidebar.multiselect("Select Species",ut. get_species_bycountlocmethd(df,locations,years,methods = methods))
else:
    if len(methods) == 0:
        species = st.sidebar.multiselect("Select Species:",ut.get_species_bycountlocmethd(df,locations,years,countries = countries))
    else: 
        species = st.sidebar.multiselect("Select Species:",ut.get_species_bycountlocmethd(df,locations,years,countries=countries,methods=methods))
st.sidebar.divider()




st.divider()
st.header("Frequencies and Distributions")
st.write("--------------------")
choose = st.selectbox("Choose graph",options = ["Poduction Distributions In Single Year","Annualy Total Prod Heatmap","Total Participation and Total Production Corelation"])

if choose == "Annualy Total Prod Heatmap":
    st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years))


elif choose == "Total Participation and Total Production Corelation":
    st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years))
    st.plotly_chart(locviz.plot_locationmethpd_paralelcat(df,locations,years))


elif choose == "Poduction Distributions In Single Year":
    years3 = st.multiselect("Choose Years",options=[str(year) for year in range(years[0],years[1]+1)])
    st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3))

st.divider()
st.markdown("<h1 style='text-align: center; color: red;'>Time Series </h1>",unsafe_allow_html=True)
st.write("---------------------------------------------------")
if len(locations) == 0:
    st.warning("Please select some locations")
else:    
    if len(countries) == 0:
            if len(methods) == 0:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years))
                else:
                    st.plotly_chart(locviz.plot_region_species_scatter_line(df, locations, years,species))
            else:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_region_methods_scatter_line(df, locations, years, methods))
                else:
                    st.plotly_chart(locviz. plot_region_methodsspecies_scatter_line(df, locations, years, methods,species))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_locat_country_line(df, locations, years,countries))
            else:
                st.plotly_chart(locviz.plot_region_countriesspecies_scatter_line(df, locations, years, countries,species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_region_countriesmethod_scatter_line(df, locations, years, countries,methods))
            else:
                st.plotly_chart(locviz.plot_region_countriesmethod_speciesscatter_line(df, locations, years, countries,methods,species))
                
                
st.divider()
st.markdown("<h1 style='text-align: center; color: red;'>Total Productions</h1>",unsafe_allow_html=True)
st.write("--------------")
if len(locations) == 0:
    st.warning("Please select some locations")
else:
    if len(countries) == 0:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years),key = "prodloc")
            else:
                st.plotly_chart(locviz.plot_specygrouped_bar(df,locations,years,species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz. plot_groupedbarlocandmethod(df,locations,years,methods))
            else:
                st.plotly_chart(locviz.plot_locmethod_specy(df,locations,years,methods,species))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_countrygrouped_bar(df,locations,years,countries))
            else:
                st.plotly_chart(locviz.plot_loccountry_specy(df,locations,years,countries,species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz. plot_loccountry_method(df,locations,years,countries,methods))
            else:
                st.plotly_chart(locviz.plot_locat_countriesmethod_specy_bar(df, locations, years, countries,methods,species))


