import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_locbox_allyears(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Location"] == location]
    df = df.groupby("Location")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Location"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df_melted,x = "Production",marginal="box",title=f"{location}'s Distribution of Total Production Values from {start} to {end}")
    figure.update_layout(
        width = 800,
        height = 500
    )
    return figure





def plot_locationproduction_increase(df,years,location):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Location"] == location]
    title = f"Production Change Over Years in {location}"
    total_prodution = df[years].sum()
    fig = px.line(total_prodution,x = total_prodution.index, y = total_prodution.values, labels={"x":"Years","y":"Production"},title=title)
    fig.update_traces(line = dict(color = "#31333F",width = 3))
    fig.update_layout(xaxis_title="Years",yaxis_title="Production")
    fig.update_layout(
        width = 600,
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  # X eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # X eksen işaret yazı rengi siyah
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
        )
    )
    return fig


def locatcountry_meth(df, years, locations):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    df = df[df["Location"] == locations]

    # Üretimi toplamak
    grouped = df.groupby(["Country", "Detail"])[years].sum().sum(axis=1).reset_index(name="Production").sort_values("Production", ascending=False).head(30)

    fig = px.pie(grouped,names ="Country",values="Production",color = "Country",facet_col="Detail",facet_col_wrap=2,title=f"Countries's most used methods in {locations}",hole=0.4)
    fig.update_layout(
        width = 700,
        height = 700,
        showlegend = True
    )
    return fig
    


def locatcountrprod_inc(df,years,locations):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Location"] == locations]
    gr = df.groupby("Country")[years].sum().reset_index()
    melted = pd.melt(gr,id_vars="Country",value_vars=years,value_name="Production",var_name="Years")
    grouped = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False).head(10)
    melted = melted[melted["Country"].isin(grouped["Country"].values)]

    fig = px.scatter(melted,x = "Years",
            y = "Production",
            color="Country",
            size="Production",
            title=f"Which countries are most efficient in {locations} in years")
    
    fig.update_layout(
        width = 700,
        height = 700,
        showlegend = True
    )
    return fig


def plot_top_count_byloc(df,years,location):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Location"] == location]
    title = f"Total Productions By Countries in {location}"

    top_countries = df.groupby('Country')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False)
    
    #sayfa_boyutu = 7
    #toplam_sayfa = (len(top_countries.Country) - 1) // sayfa_boyutu + 1

    #if "ülkesayfa" not in st.session_state:
    #    st.session_state.ülkesayfa = 1

    # Butonları grafiğin altına taşı
    #col1, col2, col3 = st.columns([1, 1, 1])  # Her sütun aynı genişlikte
    #with col1:
    #    geri_al = st.button("⬅️ Geri",key = "Country")
    #with col2:
    #    sıfırla = st.button("🔄 Sıfırla",key = "Country Sıfırla")
    #with col3:
    #    ileri_al = st.button("➡️ İleri",key = "Country ileri")

    #if geri_al and st.session_state.ülkesayfa > 1:
    #    st.session_state.ülkesayfa -= 1 
    #if sıfırla:
    #    st.session_state.ülkesayfa = 1 
    #if ileri_al and st.session_state.ülkesayfa < toplam_sayfa:
    #        st.session_state.ülkesayfa += 1           

    #başlangıç = (st.session_state.ülkesayfa - 1) * sayfa_boyutu
    #bitiş = başlangıç + sayfa_boyutu
    #current_countries = top_countries.iloc[başlangıç:bitiş]

    # Grafik oluşturma
    fig = px.choropleth(
        top_countries,
        locations="Country",
        locationmode="country names",
        color="Production",
        color_continuous_scale="RdBu",
        title=title
    )
    fig.update_layout(
    width=1000,  # Adjust the width
    height=600,  # Adjust the height if needed
    geo=dict(
        projection_type='natural earth',  # You can specify the type of projection
        showcoastlines=True,  # Optional, to show coastlines
        coastlinecolor="Black",  # Optional, to set the coastline color
    )
    )
    #fig.update_yaxes(categoryorder="total ascending")
    #fig.update_layout(
        #font=dict(size=16),
        #xaxis=dict(
        #    gridwidth=1,
        #    title_font=dict(size=18, color="red"),
        #    tickfont=dict(size=14, color="black"),
        #),
        #yaxis=dict(
        #    gridwidth=1,
        #    title_font=dict(size=18, color="red"),
        #    tickfont=dict(size=14, color="black"),
        #),
    #)
    return fig

def plot_locaspecy_intime(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Timeline of most produced species in {location} for {start}:"
    else:
        title = f"Timeline of most produced species in {location} for {start} to {end}:"
    df = df[df["Location"] == location]
    mostspecies =df.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending =False).head(7)
    group = df.groupby("Species")[years].sum().reset_index()
    group = group[group["Species"].isin(mostspecies.Species.unique())]
    melted = pd.melt(group,id_vars="Species",value_vars=years,var_name="Years",value_name="Production")
    fig = px.line(melted,x = "Years",y = "Production",color="Species",title=title)
    fig.update_layout(
        width = 800,
        height = 800,
        showlegend = True
    )
    return fig


def plot_locatspecy_methods(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    df = df[df["Location"] == location]

    grouped = df.groupby(["Location","Detail","Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    grouped = grouped[grouped.Production > 0]
    fig = px.treemap(grouped,names = "Species",values = "Production",path=[px.Constant("All"),"Location","Detail","Country","Species"],color="Production",color_continuous_scale=px.colors.sequential.RdBu,title=f"Top Species Produced By Methods And Countries In {location}")
    fig.update_layout(
        height = 1000,
        margin = dict(t=50, l=25, r=25, b=25)
    )
    return fig







def plot_locatspeciy_prod(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Which Species are produced most in {location} for {start}:"
    else:
        title = f"Which Species are produced most in {location} for {start} to {end}:"    
    df = df[df["Location"] == location]
    species_total_production = df.groupby('Species')[years].sum().sum(axis = 1).reset_index(name = 'Production').sort_values('Production', ascending = False)

    sayfa_boyutu = 7
    toplam_sayfa = (len(species_total_production.Species) - 1) // sayfa_boyutu + 1

    if "loctürsayfa" not in st.session_state:
        st.session_state.loctürsayfa = 1


    
    col1, col2, col3 = st.columns([1, 1, 1])  
    with col1:
        geri_al = st.button("⬅️ Geri",key="loc-speciy")
    with col2:
        sıfırla =st.button("🔄 Sıfırla",key = "loc-specy sıfırla")
    with col3:
        ileriye =  st.button("➡️ İleri",key = "loc-specy ileri")

    if geri_al and st.session_state.loctürsayfa > 1:
        st.session_state.loctürsayfa -= 1
    if sıfırla:
        st.session_state.loctürsayfa = 1
    if ileriye and st.session_state.loctürsayfa < toplam_sayfa:
        st.session_state.loctürsayfa += 1        


    başlangıç = (st.session_state.loctürsayfa - 1) * sayfa_boyutu
    bitiş = başlangıç + sayfa_boyutu
    current_species = species_total_production.iloc[başlangıç:bitiş]

    fig = px.scatter(current_species,x = "Species",y = "Production",labels={"x":"Species","y":"Production"},color = "Production",color_continuous_scale = "RdBu",size="Production",title=title)
    fig.update_layout(
        width = 700,
        height = 700,
        font=dict(size=16),  
        xaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  
            tickfont=dict(size=14, color="black")   
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  
            tickfont=dict(size=14, color="black")   
        )
    )
    return fig

def plot_locamethods_bar(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    df = df[df["Location"] == location]
    grouped_by_method = (
        df.groupby(["Detail", "Location"])[years]
        .sum().reset_index()
    )
    melted = pd.melt(grouped_by_method,id_vars="Detail",value_vars=years,value_name="Production",var_name="Years")
    fig = px.bar(melted,x="Years",y="Production",color="Detail",barmode="stack",title=f"{location}'s production methods distributions in years")
    return fig

def plot_locyprod_methods(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"Production Methods Donut Chart for {location} in {start}"
    else:
        title=f"Production Methods Donut Chart for {location} in {start} to {end}"
    df = df[df["Location"] == location]
    grouped_by_method = (
        df.groupby(["Detail", "Location"])[years]
        .sum()
        .sum(axis=1)
        .reset_index(name="Production")
        .sort_values("Production", ascending=False)
    )

    fig = px.pie(
        grouped_by_method,
        names="Detail", 
        values="Production",  
        color="Production",  
        title=title,
        hole=0.5
    )
    return fig





# Locations End
# --------------------------------



def plot_prodcountry_waterfall(df,country,years):
    
    start, end = years
    years = [str(year) for year in range(start, end + 1,4)]
    filtered_df = df[df["Country"] == country]

    # 2️⃣ Yıllara Göre Üretimi Hesapla
    total_production = filtered_df[years].sum()  
    yearly_changes = total_production.diff().dropna()  

    # 3️⃣ Waterfall Chart için DataFrame
    waterfall_data = pd.DataFrame({
        "Years": yearly_changes.index,
        "Production Change": yearly_changes.values
    })
    fig = go.Figure()
    fig.add_trace(go.Waterfall(x=waterfall_data["Years"], y=waterfall_data["Production Change"]))
    fig.update_layout(
        width = 700,
        height = 700,
        title = f"Production Change Of {country} Waterfall Chart", waterfallgap = 0.1
    )
    return fig

def plot_prodcountry_incr(df, country, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    title = f"Production Change Over Years In {country}"
    
    # Veriyi filtreleme (ülke ve yıl aralığı)
    df = df[df["Country"] == country]
    
    # Toplam üretimi hesapla
    total_production = df[years].sum()
    fig = px.line(total_production,x = total_production.index.astype(int),y = total_production.values,title=title)
    fig.update_layout(
        width = 600,
        height = 600,
        xaxis_title="Years",
        yaxis_title="Production",
        font=dict(size=16),
        xaxis=dict(title_font=dict(size=18, color="red"), tickfont=dict(size=14, color="black")),
        yaxis=dict(title_font=dict(size=18, color="red"), tickfont=dict(size=14, color="black"))
    )
    return fig
   
def plot_prodmethod_incr(df,country,years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    df = df[df["Country"] == country]
    df = df.groupby(["Country","Detail"])[years].sum().reset_index()
    df_long = df.melt(id_vars=["Country", "Detail"], value_vars=years, 
                       var_name="Year", value_name="Production")
    
    df_long["Year"] = df_long["Year"].astype(int)  # Yılları integer formatına çevir
    
    # Grafik oluştur
    fig = px.bar(df_long, x="Year", y="Production", color="Detail", 
                title="Production Change Over Years Using Methods", labels={"Production": "Production"},barmode="stack")
    
    # Grafik boyutunu ve eksen ayarlarını düzenle
    fig.update_layout(
        xaxis_title="Years",
        yaxis_title="Production",
        font=dict(size=16),
        xaxis=dict(title_font=dict(size=18, color="red"), tickfont=dict(size=14, color="black")),
        yaxis=dict(title_font=dict(size=18, color="red"), tickfont=dict(size=14, color="black")),
        width=1200,
        height=600
    )
    return fig

def plot_countryspeciy_pordline(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Timeline of most produced species in {country} for {start}:"
    else:
        title = f"Timeline of most produced species in {country} for {start} to {end}:"
    df = df[df["Country"] == country]
    mostspecies =df.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending =False).head(7)
    group = df.groupby("Species")[years].sum().reset_index().sort_values(years,ascending =False)
    group = group[group["Species"].isin(mostspecies.Species.unique())]
    melted = pd.melt(group,id_vars="Species",value_vars=years,var_name="Years",value_name="Production")
    fig = px.line(melted,x = "Years",y = "Production",color="Species",title=title)
    fig.update_layout(
        showlegend = True,
        width =800,
        height = 800
    )
    return fig

def plot_countryspecy_methodprod(df, country, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    
   
    df = df[df["Country"] == country]

    grouped = df.groupby(["Species", "Detail"])[years].sum().sum(axis=1).reset_index(name="Production").sort_values("Production",ascending = False).head(40)


    fig = px.bar(
        grouped, 
        x="Species", 
        y="Production", 
        color="Detail", 
        title=f"Top Species and Their Production Methods in {country} ({start} - {end})",
        labels={"Production": "Total Production", "Species": "Species", "Detail": "Method"},
        barmode="stack"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        width = 1000,
        height = 700,
        bargap=0.2
    )

    return fig




def plot_countryspecy_locatprod(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Which Species are produced most in {country} With Locations And Methods for {start}"
    else:
        title = f"Top Species Produced in {country} by Location and Method from {start} to {end}"
    df = df[df["Country"] == country]
    group = df.groupby(["Country","Location","Species","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending =False).head(40)
    group = group[group.Production > 0]
    fig = px.sunburst(group,values="Production",path=["Location","Detail","Country","Species"],color="Production",title=title,color_continuous_scale="RdBu")
    fig.update_layout(
        width = 800,
        height = 800
    )
    return fig

def plot_countryspeciy_prod(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Which Species are produced most in {country} for {start}"
    else:
        title = f"Which Species are produced most in {country} for {start} to {end}"    
    df = df[df["Country"] == country]
    species_total_production = df.groupby('Species')[years].sum().sum(axis = 1).reset_index(name = 'Production').sort_values('Production', ascending = False)

    sayfa_boyutu = 7
    toplam_sayfa = (len(species_total_production.Species) - 1) // sayfa_boyutu + 1

    if "ülketürsayfa" not in st.session_state:
        st.session_state.ülketürsayfa = 1


    # Butonları grafiğin altına taşı
    col1, col2, col3 = st.columns([1, 1, 1])  # Her sütun aynı genişlikte
    with col1:
        geri_al = st.button("⬅️ Geri",key="country-speciy")
    with col2:
        sıfırla =st.button("🔄 Sıfırla",key = "country-specy sıfırla")
    with col3:
        ileriye =  st.button("➡️ İleri",key = "country-specy ileri")

    if geri_al and st.session_state.ülketürsayfa > 1:
        st.session_state.ülketürsayfa -= 1
    if sıfırla:
        st.session_state.ülketürsayfa = 1
    if ileriye and st.session_state.ülketürsayfa < toplam_sayfa:
        st.session_state.ülketürsayfa += 1        


    başlangıç = (st.session_state.ülketürsayfa - 1) * sayfa_boyutu
    bitiş = başlangıç + sayfa_boyutu
    current_species = species_total_production.iloc[başlangıç:bitiş]

    fig = px.bar_polar(current_species,r = "Production",theta="Species",color = "Production",color_continuous_scale = "RdBu",title=title)
    fig.update_layout(
        width = 800,
        height = 700
    )
    return fig

def plot_countries_region(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"On Which Areas {country} is effective most in {start}"
    else:
        title=f"On Which Areas {country} is effective most in {start} to {end}"
    df = df[df["Country"] == country]
    grouped_by_location = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False).head(5)
    total_product = grouped_by_location["Production"].sum()
    grouped_by_location["Percentage"] = grouped_by_location["Production"] / total_product * 100
    fig = go.Figure(data=[go.Pie(labels=grouped_by_location["Location"], values=grouped_by_location["Percentage"], pull=[0, 0, 0.2, 0.2,0.2])])
    
    #figure.update_traces(
    #    text=grouped_by_location["Percentage"].map(lambda x: f"{x:.1f}%"),
    #    textposition = "outside"
    #)

    fig.update_layout(
        width = 700,
        height = 700,
        title = title,
        uniformtext_minsize=8, uniformtext_mode="hide",
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            title_font=dict(size=18, color="red"),  # X eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # X eksen işaret yazı rengi siyah
        ),
        yaxis=dict(
            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
        )
    )
    return fig


def plot_countryloc_inc(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    df = df[df["Country"] == country]
    if len(years) == 1:
        title=f"On Which Areas {country} is effective most in {start} Heatmap"
    else:
        title=f"On Which Areas {country} is effective most in {start} to {end} Heatmap"
    
    most = df.groupby("Location")[years].sum().sum(axis=1).reset_index(name = "Production").sort_values("Production",ascending = False).head(8)
    unique = most["Location"]
    grouped = df.groupby("Location")[years].sum().reset_index()
    grouped = grouped[grouped["Location"].isin(unique)]
    grouped = grouped[grouped[years].sum(axis = 1) > 0]
    melted = pd.melt(grouped,id_vars="Location",value_vars=years,value_name="Production",var_name="Years")
    fig = go.Figure(data=go.Heatmap(
            z=melted["Production"],
            x=melted["Years"],  
            y=melted["Location"],
            colorscale='RdBu'
        ))
    fig.update_layout(
        width = 700,
        height = 600,
        title = title
    )
    return fig

    
def plot_countryloc_method(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    df = df[df["Country"] == country]
    grouped = df.groupby(["Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    fig = px.bar(grouped,x = "Location",y = "Production",color = "Detail",barmode="stack",title = f"Which methods are widely used in {country}'s fishing areas ")
    fig.update_layout(
        width = 700,
        height = 700
    )
    return fig
    

def plot_countryprod_methods(df, country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"Production Methods Funnel Area Chart for {country} in {start}"
    else:
        title=f"Production Methods Funnel Area Chart for {country} in {start} to {end}"
    df = df[df["Country"] == country]
    grouped_by_method = (
        df.groupby(["Detail", "Country"])[years]
        .sum()
        .sum(axis=1)
        .reset_index(name="Production")
        .sort_values("Production", ascending=False)
    )

    fig = px.funnel_area(
        grouped_by_method,names="Detail",values="Production",color="Detail",color_discrete_sequence=px.colors.qualitative.Pastel1,title=title
    )
    fig.update_layout(
        width = 700,
        height = 600
    )
    return fig


def plot_countrybox_allyears(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Country"] == country]
    df = df.groupby("Country")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Country"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df_melted,x = "Production",marginal="rug",title=f"{country}'s Distribution of Total Production Values from {start} to {end}")
    figure.update_layout(
        width = 800,
        height = 500,
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            title_font=dict(size=18, color="red"),  # X eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # X eksen işaret yazı rengi siyah
        ),
        yaxis=dict(
            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
        )
    )
    return figure

#def plot_rainbow_foryears(df,country,years):
 #   start,end = years
 #   years = [str(year) for year in range(start,end+1)]
 #   df = df[df["Country"] == country]
 #   df_melted = pd.melt(df,id_vars=["Country"],value_vars=years,value_name="Production",var_name="Years")
 #   fig = px.box(df_melted,x = "Years",y = "Production",color = "Years",title="Production Distributions Within Years")
 #   fig.update_layout(
 #       width = 800,
 #       height = 500,
 #       font=dict(size=16),  # Yazı boyutu
 #       xaxis=dict(
 #           title_font=dict(size=18, color="red"),  # X eksen başlık yazı rengi kırmızı
 #           tickfont=dict(size=14, color="black")   # X eksen işaret yazı rengi siyah
 #       ),
#      yaxis=dict(
#            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
#            tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
#        )
    #)
    #return fig





#-------------------------------------------------
#Specy

def plot_specybox_allyears(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    df = df.groupby("Species")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Species"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.density_heatmap(df_melted,x = "Years",y = "Production",title=f"{specy}'s Distribution of Total Production Values from {start} to {end}",marginal_x="histogram",marginal_y="histogram",color_continuous_scale=px.colors.sequential.RdBu)
    figure.update_layout(
        width = 800,
        height = 500
    )
    return figure

def plot_prodspecy_incr(df,specy,years):
    start, end = years
    years = [str(year) for year in range(start, end + 1,4)]
    filtered_df = df[df["Species"] == specy]

    # 2️⃣ Yıllara Göre Üretimi Hesapla
    total_production = filtered_df[years].sum()  # Yıllık toplam üretim
    yearly_changes = total_production.diff().dropna()  # Yıllık değişim farkı

    # 3️⃣ Waterfall Chart için DataFrame
    waterfall_data = pd.DataFrame({
        "Years": yearly_changes.index,
        "Production Change": yearly_changes.values
    })
    fig = go.Figure()
    # 4️⃣ Waterfall Chart Çiz
    fig.add_trace(go.Waterfall(x=waterfall_data["Years"], y=waterfall_data["Production Change"]))
    fig.update_layout(
        width = 700,
        height = 700,
        title = f"Production Change Of {specy} Waterfall Chart", waterfallgap = 0.1
    )
    return fig


def plot_specyloc_prodtime(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    most = df.groupby("Location")[years].sum().sum(axis=1).reset_index(name = "Production").sort_values("Production",ascending = False).head(8)
    unique = most["Location"]
    grouped = df.groupby("Location")[years].sum().reset_index()
    grouped = grouped[grouped["Location"].isin(unique)]
    melted = pd.melt(grouped,id_vars="Location",value_vars = years,value_name="Production",var_name="Years")
    figure = go.Figure()
    trace  = go.Heatmap(z=melted["Production"],x=melted["Years"],y = melted["Location"],colorscale="RdBu")
    figure.add_trace(trace=trace)
    figure.update_layout(
        title = f"Production Distributions of {specy}'s most productive locations",
        width = 800,
        height = 600
    )
    return figure




def plot_species_region(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"{specy}'s production distributions in locations by mehthods.Icicle Graph"
    else:
        title=f"{specy}'s production distributions in locations by mehthods.Icicle Graph"
    df = df[df["Species"] == specy]
    grouped_by_location = df.groupby(["Location","Detail","Species","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    grouped_by_location = grouped_by_location[grouped_by_location["Production"] > 0]
    figure = px.icicle(grouped_by_location,path=[px.Constant("All Production"),"Location","Detail","Country","Species"],names="Location",values= "Production",color="Production",color_continuous_scale="RdBu",title=title)

    figure.update_layout(
        height =900
    )
    #figure.update_traces(
    #    text=grouped_by_location["Percentage"].map(lambda x: f"{x:.1f}%"),
    #    textposition = "outside"
    #)

    #figure.update_layout(
        #uniformtext_minsize=8, uniformtext_mode="hide",
        #font=dict(size=16),  # Yazı boyutu
        #xaxis=dict(
        #   title_font=dict(size=18, color="red"),  # X eksen başlık yazı rengi kırmızı
        #    tickfont=dict(size=14, color="black")   # X eksen işaret yazı rengi siyah
        #),
        #yaxis=dict(
        #    title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
        #   tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
        #)
    #)
    return figure


def plot_specymethod_prodtime(df, specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    df = df[df["Species"] == specy]
    group = df.groupby("Detail")[years].sum().reset_index()
    melt = pd.melt(group,id_vars="Detail",value_name="Production",var_name="Years",value_vars=years)
    fig = px.bar(melt,x = "Years",y = "Production",color="Detail",barmode="stack",title=f"Which methods are commonly used annualy in {specy} production")
    fig.update_layout(
        width = 700,
        height = 700
    )
    return fig




def plot_parallel_categories(df, specy,years):
        start,end = years
        years = [str(year) for year in range(start,end+1,+1)]
        df = df[df["Species"] == specy]
        grouped_by_method = (
            df.groupby(["Detail", "Species"])[years]
            .sum()
            .sum(axis=1)
            .reset_index(name="Production")
            .sort_values("Production", ascending=False)
        )
        nongrouped = df[["Species","Detail"]].merge(grouped_by_method,on=["Species","Detail"],how= "left")
        fig = px.parallel_categories(nongrouped, dimensions=["Species", "Detail"],
                                 color="Production",
                                 color_continuous_scale=px.colors.sequential.RdBu,labels={"Species":f"{specy}","Detail":"Methods"})
        fig.update_layout(title=f"Production Methods for {specy} Using Paralel Category Chart",width = 600,height = 600)
        
        return fig


""" def plot_top_locforspecy(df,specy,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    top_countries = df.groupby('Location')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False)
    top_countries = top_countries[top_countries["Production"] > 0]
    fig = px.bar(top_countries,x = "Production", y = "Location",color  = "Production",color_continuous_scale="RdBu",title=f"In Which locations {specy} is produced most",orientation="h")
    fig.update_layout(
        width = 700,
        height = 600
    )
    fig.update_yaxes(categoryorder="total ascending")
    return fig """

def plot_top_count_species(df,specy,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    title = f"Total Productions By Countries for {specy}"

    top_countries = df.groupby('Country')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False)
    
    #sayfa_boyutu = 7
    #toplam_sayfa = (len(top_countries.Country) - 1) // sayfa_boyutu + 1

    #if "ülkesayfa" not in st.session_state:
    #    st.session_state.ülkesayfa = 1

    # Butonları grafiğin altına taşı
    #col1, col2, col3 = st.columns([1, 1, 1])  # Her sütun aynı genişlikte
    #with col1:
    #    geri_al = st.button("⬅️ Geri",key = "Country")
    #with col2:
    #    sıfırla = st.button("🔄 Sıfırla",key = "Country Sıfırla")
    #with col3:
    #    ileri_al = st.button("➡️ İleri",key = "Country ileri")

    #if geri_al and st.session_state.ülkesayfa > 1:
    #    st.session_state.ülkesayfa -= 1 
    #if sıfırla:
    #    st.session_state.ülkesayfa = 1 
    #if ileri_al and st.session_state.ülkesayfa < toplam_sayfa:
    #        st.session_state.ülkesayfa += 1           

    #başlangıç = (st.session_state.ülkesayfa - 1) * sayfa_boyutu
    #bitiş = başlangıç + sayfa_boyutu
    #current_countries = top_countries.iloc[başlangıç:bitiş]

    # Grafik oluşturma
    fig = px.choropleth(
        top_countries,
        locations="Country",
        locationmode="country names",
        color="Production",
        color_continuous_scale="RdBu",
        title=title
    )
    fig.update_layout(
        width=1000,  # Adjust the width
        height=600,  # Adjust the height if needed
        geo=dict(
            projection_type='natural earth',  # You can specify the type of projection
            showcoastlines=True,  # Optional, to show coastlines
            coastlinecolor="Black",  # Optional, to set the coastline color
            lataxis_range=[-60, 85],  # Enlem aralığı (dünya haritasını sınırlar)
            lonaxis_range=[-180, 180],  # Boylam aralığı
        ),
)
    #fig.update_yaxes(categoryorder="total ascending")
    #fig.update_layout(
        #font=dict(size=16),
        #xaxis=dict(
        #    gridwidth=1,
        #    title_font=dict(size=18, color="red"),
        #    tickfont=dict(size=14, color="black"),
        #),
        #yaxis=dict(
        #    gridwidth=1,
        #    title_font=dict(size=18, color="red"),
        #    tickfont=dict(size=14, color="black"),
        #),
    #)
    return fig



def plot_top_specycountries_time(df,specy,years):
    start, end = years
    years = [str(year) for year in range(start, end + 1, 10)]
    df = df[df["Species"] == specy]
    temporariy = df.groupby("Country",)[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False).head(10)
    grouped = df.groupby("Country",)[years].sum().reset_index()
    grouped = grouped[grouped["Country"].isin(temporariy["Country"].values)]
    melt = pd.melt(grouped,id_vars="Country",value_vars=years,value_name="Production",var_name="Years")
    fig = px.line(melt,x = "Years",y = "Production",color="Country",facet_col="Country",facet_col_wrap=2,facet_col_spacing=0.2,title=f"Top Countries production change for {specy}")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig.update_yaxes(showticklabels=True)

    fig.update_layout(width=800, height=700)

    return fig




def plot_specycountry_sankey(df, specy, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1, 10)]
    df = df[df["Species"] == specy]

    grouped = df.groupby(["Country", "Location","Detail"])[years].sum().sum(axis=1).reset_index(name="Production").sort_values("Production", ascending=False).head(15)

    uniquecountry = list(grouped.Country.unique())
    uniquelocation = list(grouped.Location.unique())
    uniquemethods = list(grouped.Detail.unique())
    all_nodes = uniquecountry + uniquelocation + uniquemethods

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in grouped["Country"]]
    target = [node_dict[locat] for locat in grouped["Location"]]
    values = grouped["Production"].tolist()
    
    sources += [node_dict[locat] for locat in grouped["Location"]]
    target += [node_dict[detail] for detail in grouped["Detail"]]
    values += grouped["Production"].tolist()
    # Farklı renkler atamak için renk paleti kullanma
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)]  # Ülkeler için renkler
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocation)]  # Lokasyonlar için renkler
    method_colors = px.colors.qualitative.Pastel[:len(uniquelocation)]
    node_colors = country_colors + location_colors + method_colors  # Tüm düğümler için birleşik renk listesi

    link_colors = [node_colors[source] for source in sources]
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=20,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=link_colors  # Bağlantıları saydam hale getirdik
        ))
    )

    fig.update_layout(
    title_text=f"Where the top countries produced most in {specy} production",
    font=dict(size=20, color="white")
    )
    return fig

def plot_top_specycountr_method(df,specy,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    title = f"Which methods are common in Countries for {specy} production"
    grouped = df.groupby(["Country","Detail"])[years].sum().sum(axis =1).reset_index(name = "Production").sort_values("Production",ascending = False)
    rows = len(grouped.Detail.unique())
    fig = make_subplots(rows=rows,cols=1)

    for i,detail in enumerate(grouped.Detail.unique(),start = 1):
        filtered = grouped[grouped["Detail"] == detail].head(20)
        trace = go.Bar(x = filtered["Country"],y = filtered["Production"],name=detail)
        fig.add_trace(trace=trace,row=i,col=1)

    fig.update_layout(
        title=title,
        height=rows * 300,
        width=800,
        showlegend=True,
        xaxis_tickangle=-45,  # Yazıları 45 derece döndür
        xaxis=dict(tickfont=dict(size=10))  # Font boyutunu küçült
    )    
    return fig    







