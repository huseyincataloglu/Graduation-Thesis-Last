import pandas as pd
import plotly.express as px
import streamlit as st



def plot_locbox_allyears(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Location"] == location]
    df = df.groupby("Location")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Location"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df_melted,x = "Production",title=f"{location}'s Distribution of Total Production Values from {start} to {end}")
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


    # Butonları grafiğin altına taşı
    col1, col2, col3 = st.columns([1, 1, 1])  # Her sütun aynı genişlikte
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


def plot_locyprod_methods(df,years,location):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"Production Methods Treemap for {location} in {start}"
    else:
        title=f"Production Methods Treemap for {location} in {start} to {end}"
    df = df[df["Location"] == location]
    grouped_by_method = (
        df.groupby(["Detail", "Location"])[years]
        .sum()
        .sum(axis=1)
        .reset_index(name="Production")
        .sort_values("Production", ascending=False)
    )

    fig = px.treemap(
        grouped_by_method,
        names="Detail", 
        values="Production",  
        path=["Location", "Detail"],  
        color="Production",  
        color_continuous_scale="RdBu",  
        title=title  
    )
    return fig





# Locations End
# --------------------------------





def plot_prodcountry_incr(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    title = f"Production Change Over Years In {country}"
    df = df[df["Country"] == country]
    total_prodution = df[years].sum()
    fig = px.line(total_prodution,x = total_prodution.index, y = total_prodution.values, labels={"x":"Years","y":"Production"},title=title)
    fig.update_traces(line = dict(color = "#31333F",width = 3))
    fig.update_layout(xaxis_title="Years",yaxis_title="Production")
    fig.update_layout(
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




def plot_countryspeciy_prod(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title = f"Which Species are produced most in {country} for {start}:"
    else:
        title = f"Which Species are produced most in {country} for {start} to {end}:"    
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

    fig = px.scatter(current_species,x = "Species",y = "Production",labels={"x":"Species","y":"Production"},color = "Production",color_continuous_scale = "RdBu",size="Production",title=title)
    fig.update_layout(
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

def plot_countries_region(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"{country}'s Production Distribution by Fishery Areas in {start}"
    else:
        title=f"{country}'s Production Distribution by Fishery Areas in {start} to {end}"
    df = df[df["Country"] == country]
    grouped_by_location = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    total_product = grouped_by_location["Production"].sum()
    grouped_by_location["Percentage"] = grouped_by_location["Production"] / total_product * 100
    figure = px.bar(grouped_by_location,x="Location",y = "Production",color="Production",color_continuous_scale="Rdbu",title=title)

    #figure.update_traces(
    #    text=grouped_by_location["Percentage"].map(lambda x: f"{x:.1f}%"),
    #    textposition = "outside"
    #)

    figure.update_layout(
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
    return figure

    

def plot_countryprod_methods(df, country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"Production Methods Treemap for {country} in {start}"
    else:
        title=f"Production Methods Treemap for {country} in {start} to {end}"
    df = df[df["Country"] == country]
    grouped_by_method = (
        df.groupby(["Detail", "Country"])[years]
        .sum()
        .sum(axis=1)
        .reset_index(name="Production")
        .sort_values("Production", ascending=False)
    )

    fig = px.treemap(
        grouped_by_method,
        names="Detail", 
        values="Production",  
        path=["Country", "Detail"],  
        color="Production",  
        color_continuous_scale="RdBu",  
        title=title  
    )
    return fig


def plot_countrybox_allyears(df,country,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Country"] == country]
    df = df.groupby("Country")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Country"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df_melted,x = "Production",title=f"{country}'s Distribution of Total Production Values from {start} to {end}")
    return figure



#-------------------------------------------------
#Specy

def plot_specybox_allyears(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df = df[df["Species"] == specy]
    df = df.groupby("Species")[years].sum().reset_index()
    df_melted= pd.melt(df,id_vars=["Species"],value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df_melted,x = "Production",title=f"{specy}'s Distribution of Total Production Values from {start} to {end}")
    return figure

def plot_prodspecy_incr(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    title = f"Production Change Over Years In {specy}"
    df = df[df["Species"] == specy]
    total_prodution = df[years].sum()
    fig = px.line(total_prodution,x = total_prodution.index, y = total_prodution.values, labels={"x":"Years","y":"Production"},title=title)
    fig.update_traces(line = dict(color = "#31333F",width = 3))
    fig.update_layout(xaxis_title="Years",yaxis_title="Production")
    fig.update_layout(
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


def plot_species_region(df,specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"{specy}'s Production Distribution by Fishery Areas in {start}"
    else:
        title=f"{specy}'s Production Distribution by Fishery Areas in {start} to {end}"
    df = df[df["Species"] == specy]
    grouped_by_location = df.groupby(["Location","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    total_product = grouped_by_location["Production"].sum()
    grouped_by_location["Percentage"] = grouped_by_location["Production"] / total_product * 100
    figure = px.sunburst(grouped_by_location,path=["Species","Location"],names="Location",values= "Production",color="Production",color_continuous_scale="Rdbu",title=title)

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

def plot_specyprod_methods(df, specy,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,+1)]
    if len(years) == 1:
        title=f"Production Methods Treemap for {specy} in {start}"
    else:
        title=f"Production Methods Treemap for {specy} in {start} to {end}"
    df = df[df["Species"] == specy]
    grouped_by_method = (
        df.groupby(["Detail", "Species"])[years]
        .sum()
        .sum(axis=1)
        .reset_index(name="Production")
        .sort_values("Production", ascending=False)
    )

    fig = px.treemap(
        grouped_by_method,
        names="Detail", 
        values="Production",  
        path=["Species", "Detail"],  
        color="Production",  
        color_continuous_scale="RdBu",  
        title=title  
    )
    return fig


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








