import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as ut
from modules import speciesvizualition as speciesviz
from app import df

#Sidebar configurations --------------
st.sidebar.title("All Filters")
st.sidebar.divider()
species = st.sidebar.multiselect("Choose species : ",ut.get_uniquefeature(df,"Species"))
st.sidebar.divider()
years = st.sidebar.slider("Choose the range to filter",min_value=1950,max_value=2018,step=1,value=(1950,2018))
st.sidebar.divider()
locations = st.sidebar.multiselect("Filter Fishing Areas :",ut.get_commonlocations_forspecies(df,species,years))
st.sidebar.divider()
if len(locations) == 0: 
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandspecies(df,species,years))
else:
    methods = st.sidebar.multiselect("Filter Production Methods",ut.get_methodsfor_locandspecies(df,species,years,locations))
st.sidebar.divider()
if len(locations) == 0:
    if len(methods) == 0:
        countries = st.sidebar.multiselect("Select Countries",ut. get_countries_byspecies(df,species,years))
    else:
        countries = st.sidebar.multiselect("Select Countries",ut. get_countries_byspecies(df,species,years,methods = methods))
else:
    if len(methods) == 0:
        countries = st.sidebar.multiselect("Select Countries:",ut.get_countries_byspecies(df,species,years,locations))
    else:
        countries = st.sidebar.multiselect("Select Countries:",ut.get_countries_byspecies(df,species,years,locations,methods))
st.sidebar.divider()


#Sidebar configurations -------------

st.markdown("<h1 style='text-align: center;color:red;'>Specy Based Analyses 🐟</h1>",unsafe_allow_html=True)
st.divider()
cl1,cl2 = st.columns(2)
with cl1:
    st.markdown(
        """
        <h2 style="font-size:24px;">Welcome to the <strong style="color:red;">Specy Page</strong>!</h2>
        <p style="font-size:20px;">Here you can explore:</p>
        <ul style="font-size:18px;">
            <li>How the production distributed across multiple species</li>
            <li>Which species produced more for a specific country</li>
            <li>Compare based on Locations</li>
            <li>Total productions by species and differences between them</li>
            <li>Production change based on a specific species for variety years</li>
            <li>Compare production methods for different species</li>
        </ul>
        <p style="font-size:18px;">Use the sidebar to select species,locations,countries, and methods to customize your analysis!</p>
        """, 
        unsafe_allow_html=True
    )



st.divider()
st.header("Frequencies and Distributions")
st.write("--------------------")
choose = st.selectbox("Choose graph",options = ["Poduction Distributions In Single Year","Annualy Total Prod Box","Total Participation Frequency","Total Participation and Total Porduction Corelation"])

if choose == "Annualy Total Prod Box":
    st.plotly_chart(speciesviz.plot_histogram_yearlytotal(df, species, years),use_container_width=True)

elif choose == "Poduction Distributions In Single Year":
    years1 = st.multiselect("Selecy separate years related to sidebar years:",[str(year) for year in range(years[0],years[1]+1)])
    st.plotly_chart(speciesviz.plot_proddistspecies_yearly(df, species, years1),use_container_width=True)


elif choose == "Total Participation and Total Porduction Corelation":
    st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years),use_container_width=True)
    st.plotly_chart(speciesviz.plot_speciesmethpd_paralelcat(df,species,years),use_container_width=True)


st.divider()
st.markdown("<h1 style='text-align: center; color: red;'>Time Series </h1>",unsafe_allow_html=True)
st.write("---------------")
if len(locations) == 0:
    if len(methods) == 0:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_species_overyears(df,species,years),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_speciesountries_overyears(df, species, years,countries),use_container_width=True)
    else:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_speciesmethods_overyears(df, species, years,methods),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_speciesmethod_countoveryears(df, species, years,methods,countries),use_container_width=True)
else:
    if len(methods) == 0:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_specieslocats_overyears(df, species, years,locations),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_specieslocats_countroveryears(df, species, years,locations,countries),use_container_width=True)
    else:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_specieslocats_methodsoveryears(df, species, years,locations,methods),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_specieslocat_methcountroveryears(df, species, years,locations,methods,countries),use_container_width=True)




st.divider()
st.markdown("<h1 style='text-align: center; color: red;'>Total Productions</h1>",unsafe_allow_html=True)
st.write("-------------")
if len(locations) == 0:
    if len(methods) == 0:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_speciespolar(df, species, years),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_speciescountries_polar(df, species, years,countries),use_container_width=True)
    else:
        if len(countries) == 0:
            st.plotly_chart(speciesviz. plot_speciesmethodspolar(df, species, years,methods),use_container_width=True)
        else:
            st.plotly_chart(speciesviz. plot_speciescountr_methodpolar(df, species, years,methods,countries),use_container_width=True)
else:    
    if len(methods) == 0:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_specieslocat_polar(df, species, years,locations),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_speciescountr_locatpolar(df, species, years,locations,countries),use_container_width=True)
    else:
        if len(countries) == 0:
            st.plotly_chart(speciesviz.plot_speciesmethods_locatpolar(df, species, years,locations,methods),use_container_width=True)
        else:
            st.plotly_chart(speciesviz.plot_specylocatmethods_countr_sankey(df,species,years,locations,methods,countries),use_container_width=True)














