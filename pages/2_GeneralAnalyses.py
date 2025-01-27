import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as util
from modules import overviewvizualition as oviz
from modules import visualization as viz
from modules import utilitiesoverview as uo
from app import df



choose = st.sidebar.selectbox("Choose type of analyses:",["Fishery Area","Countries","Species","Production methods"])
st.sidebar.write("----------")
years = st.sidebar.slider("Filter the years",min_value=1950,max_value=2018,value=(1950,2018),step=1)


st.title("General Analysis")
st.divider()


if choose ==  "Fishery Area":
    locations = ["All Areas"] + list(util.get_uniquefeature(df,"Location"))
    location = st.selectbox("Choose Area :",locations)

    if location == "All Areas":
        c1,c2 = st.columns([1,1])
        with c1:
            st.markdown("""<h2 style = 'text-align : center;'> Statistics</h3> """,unsafe_allow_html=True)
            st.write("-------")
            a,b = st.columns([1.5, 2.5])
            with a:
                st.write(f"**General Statistics**")
                st.dataframe(uo.get_summary_dfOverview(df,years))
            with b:
                st.write(f"**Yearly Statistics**")
                st.dataframe(uo.get_yearly_statsOverview(df,years))
        with c2:
            st.markdown("""<h2 style = 'text-align : center;'> Production Distributions</h3> """,unsafe_allow_html=True)
            st.write("-------")
            st.plotly_chart(oviz.plot_locationbox_allyears(df,years))

        cc1,_,cc2 = st.columns([1,0.2,1],vertical_alignment="top")
        with cc1:
            st.plotly_chart(oviz.plot_production_increase(df,years))
            st.divider()
            st.plotly_chart(oviz.plot_top_species_by_production(df,years))
        with cc2:
            st.plotly_chart(oviz.plot_locations_by_prodution(df,years))
            st.divider()
            st.plotly_chart(oviz.plot_top_countries_by_production(df,years))
            st.plotly_chart(oviz.plot_top_production_methods(df,years))
    else:
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
                st.dataframe(util.get_yearly_stats(df,"Location",location,years))
        with c2:
            st.markdown("""<h2 style = 'text-align : center;'> Production Distributions</h3> """,unsafe_allow_html=True)
            st.write("-------")
            st.plotly_chart(viz.plot_locbox_allyears(df,years,location))

        cc1,_,cc2 = st.columns([1,0.2,1],vertical_alignment="top")
        with cc1:
            st.plotly_chart(viz.plot_locationproduction_increase(df,years,location))
            st.divider()
            st.plotly_chart(viz.plot_locatspeciy_prod(df,years,location))
        with cc2:
            st.divider()
            st.plotly_chart(viz.plot_top_count_byloc(df,years,location))
            st.plotly_chart(viz.plot_locyprod_methods(df,years,location))

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
            st.dataframe(util.get_yearly_stats(df,"Country",country,years))
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

elif choose == "Species":
    specy = st.selectbox("Select Specy:",util.get_uniquefeature(df,"Species"))
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("""<h2 style = 'text-align : center;'> Statistics</h3> """,unsafe_allow_html=True)
        st.write("-------")
        a,b = st.columns([1.5, 2.5])
        with a:
            st.write(f"**General Statistics**")
            st.dataframe(util.get_summary_df(df,"Species",specy,years))
        with b:
            st.write(f"**Yearly Statistics**")
            st.dataframe(util.get_yearly_stats(df,"Species",specy,years))
    with c2:
        st.markdown("""<h2 style = 'text-align : center;'> Annualy Total Production Distributions</h3> """,unsafe_allow_html=True)
        st.write("-------")
        st.plotly_chart(viz.plot_specybox_allyears(df,specy,years))

    columnleft,_,columnright = st.columns([1,0.2,1])
    with columnleft:
        st.plotly_chart(viz.plot_prodspecy_incr(df,specy,years))
        st.write("------")
        st.plotly_chart(viz.plot_top_count_species(df,specy,years))
    with columnright:
        st.plotly_chart(viz.plot_species_region(df,specy,years))
        st.write("--------")
        st.plotly_chart(viz.plot_specyprod_methods(df, specy,years))
            





    



    


    





