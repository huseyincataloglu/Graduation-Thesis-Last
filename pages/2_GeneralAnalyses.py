import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as util
from modules import visualization as viz
from app import df



choose = st.sidebar.selectbox("Choose type of analyses:",["Fishery Area","Countries","Species","Production methods"])
st.sidebar.write("----------")
years = st.sidebar.slider("Filter the years",min_value=1950,max_value=2018,value=(1950,2018),step=1)


st.title("General Analysis")
st.divider()

if choose == "Fishery Area":
    locations = ["All Areas"] + list(util.get_uniquefeature(df,"Location"))
    location = st.selectbox("Choose Area :",locations)

    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("""<h2 style = 'text-align : center;'> Statistics</h3> """,unsafe_allow_html=True)
        st.write("-------")
        a,b = st.columns([1.5, 2.5])
        with a:
            st.write(f"**General Statistics**")
            st.dataframe(util.get_summary_df(df,"Location",location,years))
        with b:
            st.write(f"**Yearly Statistics**")
            st.dataframe(util.get_yearls_stats(df,"Location",location,years))
    with c2:
        st.markdown("""<h2 style = 'text-align : center;'> Production Distributions</h3> """,unsafe_allow_html=True)
        st.write("-------")
        st.plotly_chart(viz.plot_locationbox_allyears(df,location,years))

    cc1,_,cc2 = st.columns([1,0.2,1],vertical_alignment="top")
    if location == "All Areas":
        with cc1:
            st.plotly_chart(viz.plot_production_increase(df,years))
            st.divider()
            st.plotly_chart(viz.plot_top_species_by_production(df,years))
        with cc2:
            st.plotly_chart(viz.plot_locations_by_prodution(df,years))
            st.divider()
            st.plotly_chart(viz.plot_top_countries_by_production(df,years))
            st.plotly_chart(viz.plot_top_production_methods(df,years))
    else:
        with cc1:
            st.plotly_chart(viz.plot_production_increase(df,years,location))
            st.divider()
            st.plotly_chart(viz.plot_top_species_by_production(df,years,location))
        with cc2:
            st.plotly_chart(viz.plot_top_production_methods(df,years,location))
            st.divider()
            st.plotly_chart(viz.plot_top_countries_by_production(df,years,location))
elif choose == "Countries":
    country = st.selectbox("Select Country:",util.get_uniquefeature(df,"Country"))
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("""<h2 style = 'text-align : center;'> Statistics</h3> """,unsafe_allow_html=True)
        st.write("-------")
        a,b = st.columns([1.5, 2.5])
        with a:
            st.write(f"**General Statistics**")
            st.dataframe(util.get_summary_df(df,"Country",country,years))
        with b:
            st.write(f"**Yearly Statistics**")
            st.dataframe(util.get_yearls_stats(df,"Country",country,years))
    with c2:
        st.markdown("""<h2 style = 'text-align : center;'> Production Distributions</h3> """,unsafe_allow_html=True)
        st.write("-------")
        st.plotly_chart(viz.plot_countrybox_allyears(df,country,years))

    
    columnleft,_,columnright = st.columns([1,0.2,1])
    with columnleft:
        st.plotly_chart(viz.plot_prodcountry_incr(df,country,years))
        st.write("------")
        st.plotly_chart(viz.plot_countryspeciy_prod(df,country,years))
    with columnright:
        st.plotly_chart(viz.plot_countries_region(df,country,years))
        st.write("--------")
        st.plotly_chart(viz.plot_countryprod_methods(df,country,years))    


    



    


    





