import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as util
from modules import visualization as viz
from app import df



choose = st.sidebar.selectbox("Choose type of analyses:",["Fishery Area","Countries","Species","Production methods"])


st.title("General Analysis")
st.divider()

if choose == "Fishery Area":
    locations = ["All Areas"] + list(util.get_uniquefeature(df,"Location"))
    location = st.selectbox("Choose Area :",locations)
    cc1,_,cc2 = st.columns([1,0.2,1],vertical_alignment="top")
    if location == "All Areas":
        with cc1:
            st.plotly_chart(viz.plot_production_increase(df))
            st.divider()
            st.plotly_chart(viz.plot_top_species_by_production(df))
        with cc2:
            st.plotly_chart(viz.plot_locations_by_prodution(df))
            st.divider()
            st.plotly_chart(viz.plot_top_countries_by_production(df))
            st.plotly_chart(viz.plot_top_production_methods(df))
    else:
        with cc1:
            st.plotly_chart(viz.plot_production_increase(df,location))
            st.divider()
            st.plotly_chart(viz.plot_top_species_by_production(df,location))
        with cc2:
            st.plotly_chart(viz.plot_top_production_methods(df,location))
            st.divider()
            st.plotly_chart(viz.plot_top_countries_by_production(df,location))
elif choose == "Countries":
    country = st.selectbox("Select Country:",util.get_uniquefeature(df,"Country"))
    columnleft,_,columnright = st.columns([1,0.2,1])
    with columnleft:
        st.plotly_chart(viz.plot_prodcountry_incr(df,country))
        st.write("------")
        st.plotly_chart(viz.plot_countryspeciy_prod(df,country))
    with columnright:
        st.plotly_chart(viz.plot_countries_region(df,country))
        st.write("--------")
        st.plotly_chart(viz.plot_countryprod_methods(df,country))    


    



    


    





