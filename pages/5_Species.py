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

with cl2:
    st.markdown("""
      Brieflly explain production methods:         
    - **Capture production** → *Capture*: Refers to fish caught directly from natural water bodies.
    - **Aquaculture production (marine)** → *Marine Aq*: Represents fish farming in seawater.
    - **Aquaculture production (freshwater)** → *Freshwater Aq*: Denotes fish farming in freshwater environments.
    - **Aquaculture production (brackishwater)** → *Brackish Aq*: Refers to fish farming in brackish water (a mix of freshwater and seawater).

    The `dataframe["Detail"]` column is updated using this mapping to provide concise and consistent labels for production types.
    """,unsafe_allow_html=True)



st.divider()
st.header("Frequencies and Distributions")
st.write("--------------------")
choose = st.selectbox("Choose graph",options = ["Poduction Distributions In Single Year","Annualy Total Prod Box","Total Participation Frequency","Total Participation and Total Porduction Corelation"])

if choose == "Annualy Total Prod Box":
    if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years))
            else:
               st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,methods=methods))
            else:
               st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,countries=countries,methods=methods))
    else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,locations=locations))
            else:
               st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,countries=countries,locations=locations))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,methods=methods,locations=locations))
            else:
               st.plotly_chart(speciesviz.plot_proddist_boxplotspecies(df,species,years,countries=countries,methods = methods,locations=locations))

elif choose == "Poduction Distributions In Single Year":
    years1 = st.multiselect("Selecy separate years related to sidebar years:",[str(year) for year in range(years[0],years[1]+1)])
    if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,countries=countries,methods=methods))
    else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,countries=countries,locations=locations))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,locations=locations,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrapyearly(df,species,years1,countries=countries,locations=locations,methods = methods))

elif choose == "Total Participation Frequency":
    if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years))
            else:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,countries=countries,methods=methods))
    else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,countries=countries,locations=locations,methods = methods))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,methods=methods,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_participation_by_species(df,species,years,countries=countries,methods = methods,locations=locations))
elif choose == "Total Participation and Total Porduction Corelation":
    if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years))
            else:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,countries=countries,methods=methods))
    else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,countries=countries,locations=locations,methods = methods))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,methods=methods,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_partvsprod_by_species(df,species,years,countries=countries,methods = methods,locations=locations))
            


st.write("----------------")
if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,countries=countries,methods=methods))
else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,countries=countries,locations=locations,methods = methods))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,methods=methods,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_parallel_corgrap(df,species,years,countries=countries,methods = methods,locations=locations))

st.write("-------------")
if len(locations) == 0:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years))
            else:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,countries=countries))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,methods=methods))
            else:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,countries=countries,methods=methods))
else:
        if len(methods) == 0:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,countries=countries,locations=locations,methods = methods))
        else:
            if len(countries) == 0:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,methods=methods,locations=locations))
            else:
                st.plotly_chart(speciesviz.plot_species_overyears(df,species,years,countries=countries,methods = methods,locations=locations))

st.write("-------------")
if len(locations) == 0:
    st.plotly_chart(speciesviz.plot_speciesprdouction_by_detail(df,species,years))
else:
    st.plotly_chart(speciesviz.plot_speciesprdouction_by_detail(df,species,years,locations))    


st.write("-------------")

if len(countries) == 0:
    st.plotly_chart(speciesviz.plot_speciescountry_parallel(df, species, years))
else:    
    st.plotly_chart(speciesviz.plot_speciescountry_parallel(df, species, years, countries))














