import pandas as pd
import plotly.express as px
import streamlit as st
from modules import utilities as util
from modules import overviewvizualition as oviz
from modules import visualization as viz
from modules import utilitiesoverview as uo
from app import df



choose = st.sidebar.selectbox("Choose type of analyses:",["Fishery Area","Countries","Species"])
st.sidebar.write("----------")
years = st.sidebar.slider("Filter the years",min_value=1950,max_value=2018,value=(1950,2018),step=1)


st.markdown("<h1 style='text-align: center; color: red;'>General Analysis</h1>",unsafe_allow_html=True)
st.divider()
st.markdown("""
Welcome to the **General Analysis** section. Here you can explore various analyses of the fishery data. 
You can filter the data by different categories such as **Fishery Area**, **Countries**, **Species**, and **Production Methods**.

Use the sidebar to choose the type of analysis and filter the years according to your preferences. The statistics, production distributions, and trends are displayed interactively to help you understand global fishery patterns and trends over time.

- **Fishery Area**: Explore statistics and production distributions by different fishery areas across the globe.
- **Countries**: View fishery statistics for specific countries and their contributions to global production.
- **Species**: Analyze fishery production by different species and understand trends.

Select any option and dive into detailed visualizations to gain insights into the data!
""",unsafe_allow_html=True)
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
        st.write("-------------------")
        st.markdown("<h1 style='text-align: center; color: red;'>Country Section</h1>",unsafe_allow_html=True)
        lc1,lc2= st.columns([1,1],vertical_alignment="top")
        with lc1:
            st.write("---------------")
            st.plotly_chart(viz.plot_locationproduction_increase(df,years,location))
            st.divider()
            st.plotly_chart(viz.locatcountrprod_inc(df,years,location))
        with lc2:
            st.write("---------------")
            st.plotly_chart(viz.plot_top_count_byloc(df,years,location))
            st.write("---------------")
            st.plotly_chart(viz.locatcountry_meth(df,years,location))


        st.markdown("<h1 style='text-align: center; color: red;'>Specy Section</h1>",unsafe_allow_html=True)
        st.write("-------------------")
        ls1,ls2 = st.columns([1,1],vertical_alignment="top")
        with ls1:
            st.plotly_chart(viz.plot_locaspecy_intime(df,years,location))
        with ls2:
            st.plotly_chart(viz.plot_locatspeciy_prod(df,years,location))
        st.write("-------")
        st.plotly_chart(viz.plot_locatspeciy_country(df,years,location))
        st.plotly_chart(viz.plot_locatspecy_methods(df,years,location))
        
        st.write("--------------------------")
        st.markdown("<h1 style='text-align: center; color: red;'>Method Section</h1>",unsafe_allow_html=True)
        lm1,lm2 = st.columns(2)
        with lm1:
            st.plotly_chart(viz.plot_locamethods_bar(df,years,location))
        with lm2:
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
        #st.write("----------")
       # st.plotly_chart(viz.plot_rainbow_foryears(df,country,years))

    with c2:
        st.markdown("""<h2 style = 'text-align : center;'> Production Distributions</h3> """,unsafe_allow_html=True)
        st.write("-------")
        st.plotly_chart(viz.plot_countrybox_allyears(df,country,years))
 

    st.write("------------------------")
    st.markdown("<h1 style='text-align: center; color: red;'>Location Section</h1>",unsafe_allow_html=True)
    locleft,locrigth = st.columns([1,1])
    with locleft:
        st.plotly_chart(viz.plot_prodcountry_incr(df,country,years))
        st.plotly_chart(viz.plot_countries_region(df,country,years))
    with locrigth:
        st.plotly_chart(viz.plot_countryloc_inc(df,country,years))
        st.plotly_chart(viz.plot_countryloc_method(df,country,years))

    st.write("------------------------")
    st.markdown("<h1 style='text-align: center; color: red;'>Specy Section</h1>",unsafe_allow_html=True)
    specyleft,specyright = st.columns(2)
    with specyleft:
        st.plotly_chart(viz.plot_countryspeciy_pordline(df,country,years))
        st.plotly_chart(viz.plot_countryspecy_methodprod(df,country,years))
    with specyright:
        st.plotly_chart(viz.plot_countryspeciy_prod(df,country,years))
        st.plotly_chart(viz.plot_countryspecy_locatprod(df,country,years))

    st.write("------------------------")
    st.markdown("<h1 style='text-align: center; color: red;'>Method Section</h1>",unsafe_allow_html=True)
    methodleft,methodright = st.columns(2)
    with methodleft:
        st.plotly_chart(viz.plot_prodmethod_incr(df,country,years))
    with methodright:
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

    st.write("-------")
    st.markdown("<h1 style='text-align: center; color: red;'>Location Section</h1>",unsafe_allow_html=True)
    columnleft,_,columnright = st.columns([1,0.2,1])
    with columnleft:
        st.plotly_chart(viz.plot_prodspecy_incr(df,specy,years))
        st.write("------")
        st.plotly_chart(viz.plot_top_locforspecy(df,specy,years))
    with columnright:
        st.plotly_chart(viz.plot_specyloc_prodtime(df,specy,years))
        st.write("--------")
        st.plotly_chart(viz.plot_species_region(df,specy,years)) 

    st.write("-------")
    st.markdown("<h1 style='text-align: center; color: red;'>Country Section</h1>",unsafe_allow_html=True)    
    loccont1,loccount2 = st.columns(2)
    with loccont1:
        st.plotly_chart(viz.plot_top_count_species(df,specy,years))
        st.plotly_chart(viz.plot_top_specycountries_time(df,specy,years))
    with loccount2:
        st.plotly_chart(viz.plot_top_specycountr_method(df,specy,years))
    st.plotly_chart(viz.plot_specycountry_sankey(df,specy,years))

    st.write("-----------")
    st.markdown("<h1 style='text-align: center; color: red;'>Method Section</h1>",unsafe_allow_html=True)
    specymethod1 , specymethod2 = st.columns(2)
    with specymethod1:
        st.plotly_chart(viz.plot_specymethod_prodtime(df, specy,years))
            
    with specymethod2:
        st.subheader("Brief Explanation :")
        st.write("In General, paralel category graph is used to expose the relations between categoric features, showing frequencies.However ı want to show production amount by coloring it")
        st.plotly_chart(viz. plot_parallel_categories(df, specy,years))



    



    


    





