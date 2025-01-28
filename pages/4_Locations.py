import streamlit as st
import plotly.express as px
import pandas as pd
from modules import utilities as ut
from modules import locationvisualizations as locviz
from app import df

st.markdown("<h1 style='text-align: left; color : red;'>Location Based Analyses</h1>",unsafe_allow_html=True)
st.markdown(
        """
        <h2 style="font-size:24px;">Welcome to the <strong style="color:red;">Locations Page</strong>!</h2>
        <p style="font-size:20px;">Here you can explore:</p>
        <ul style="font-size:18px;">
            <li>Total productions by Locations and differences between them</li>
            <li>Production change based on a specific species for variety years</li>
            <li>Compare production methods for different species</li>
        </ul>
        <p style="font-size:18px;">Use the sidebar to select locations and methods to customize your analysis and once you choose the locations and the range of years, it will effect all the graphs!</p>
        """, 
        unsafe_allow_html=True
    )

st.sidebar.title("All Filters")
st.sidebar.divider()
locations = st.sidebar.multiselect("Choose locations : ",ut.get_uniquefeature(df,"Location"))
st.sidebar.divider()
years = st.sidebar.slider("Choose the range to filter",min_value=1950,max_value=2018,step=1,value=(1950,2018))
st.sidebar.divider()
countries = st.sidebar.multiselect("Filter Couuntries:",ut.get_commoncountr_forlocs(df,locations,years))
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
choose = st.selectbox("Choose graph",options = ["Poduction Distributions In Single Year","Annualy Total Prod Box","Total Participation Frequency","Total Participation and Total Porduction Corelation"])

if choose == "Annualy Total Prod Box":
    if len(countries) == 0:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years))
            else:
               st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,methods=methods))
            else:
               st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,species=species,methods=methods))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,countries=countries))
            else:
               st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,countries=countries,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,methods=methods,countries=countries))
            else:
               st.plotly_chart(locviz.plot_proddist_boxplotlocations(df,locations,years,countries=countries,methods = methods,species=species))


elif choose == "Total Participation Frequency":
    if len(countries) == 0:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years))
            else:
               st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,methods=methods))
            else:
               st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,species=species,methods=methods))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,countries=countries))
            else:
               st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,countries=countries,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,methods=methods,countries=countries))
            else:
               st.plotly_chart(locviz.plot_participation_by_locations(df,locations,years,countries=countries,methods = methods,species=species))

elif choose == "Total Participation and Total Porduction Corelation":
    if len(countries) == 0:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years))
            else:
               st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,methods=methods))
            else:
               st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,species=species,methods=methods))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,countries=countries))
            else:
               st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,countries=countries,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,methods=methods,countries=countries))
            else:
               st.plotly_chart(locviz.plot_partvsprod_by_locations(df,locations,years,countries=countries,methods = methods,species=species))


elif choose == "Poduction Distributions In Single Year":
    years3 = st.multiselect("Choose Years",options=[str(year) for year in range(years[0],years[1]+1)])
    if len(countries) == 0:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3))
            else:
               st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,methods=methods))
            else:
               st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,species=species,methods=methods))
    else:
        if len(methods) == 0:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,countries=countries))
            else:
               st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,countries=countries,species=species))
        else:
            if len(species) == 0:
                st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,methods=methods,countries=countries))
            else:
               st.plotly_chart(locviz.plot_locationn_grapyearly(df,locations,years3,countries=countries,methods = methods,species=species))


st.write("----------------")

cc1,cc2 = st.columns(2)
with cc1:
    if len(countries) == 0:
            if len(methods) == 0:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years))
                else:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,species=species))
            else:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,methods=methods))
                else:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,species=species,methods=methods))
    else:
            if len(methods) == 0:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,countries=countries))
                else:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,countries=countries,species=species))
            else:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,methods=methods,countries=countries))
                else:
                    st.plotly_chart(locviz.plot_distline_locat(df,locations,years,countries=countries,methods = methods,species=species))
                
                
with cc2:
    if len(countries) == 0:
            if len(methods) == 0:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years))
                else:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,species=species))
            else:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,methods=methods))
                else:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,species=species,methods=methods))
    else:
            if len(methods) == 0:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,countries=countries))
                else:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,countries=countries,species=species))
            else:
                if len(species) == 0:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,methods=methods,countries=countries))
                else:
                    st.plotly_chart(locviz.plot_groupedbarloc(df,locations,years,countries=countries,methods = methods,species=species))
                    



