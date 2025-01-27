import pandas as pd
import plotly.express as px
import streamlit as st


def plot_locationbox_allyears(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df2 = pd.DataFrame(df[years].sum(),columns=["Production"])
    #df_melted= pd.melt(df2,id_vars=df2.index,value_vars=years,var_name="Years",value_name="Production")
    figure = px.histogram(df2,x = "Production",title=f"Distribution of Total Production Values In Years")
    return figure


def plot_production_increase(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    title = f"Production Change Over Years In All Areas"    
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



def plot_top_countries_by_production(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]

    title = f"Which Countries are produced most in All Areas"
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



def plot_top_species_by_production(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    
    title = f"Which Species are produced most in All Areas:"

    species_total_production = df.groupby('Species')[years].sum().sum(axis = 1).reset_index(name = 'Production').sort_values('Production', ascending = False)

    sayfa_boyutu = 7
    toplam_sayfa = (len(species_total_production.Species) - 1) // sayfa_boyutu + 1

    if "türsayfa" not in st.session_state:
        st.session_state.türsayfa = 1


    # Butonları grafiğin altına taşı
    col1, col2, col3 = st.columns([1, 1, 1])  # Her sütun aynı genişlikte
    with col1:
        geri_al = st.button("⬅️ Geri",key="Species")
    with col2:
        sıfırla =st.button("🔄 Sıfırla",key = "Species sıfırla")
    with col3:
        ileriye =  st.button("➡️ İleri",key = "Species ileri")

    if geri_al and st.session_state.türsayfa > 1:
        st.session_state.türsayfa -= 1
    if sıfırla:
        st.session_state.türsayfa = 1
    if ileriye and st.session_state.türsayfa < toplam_sayfa:
        st.session_state.türsayfa += 1        


    başlangıç = (st.session_state.türsayfa - 1) * sayfa_boyutu
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



def plot_top_production_methods(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]

    title = f"Which Production methods are widely used in All Areas"   
    topused = df.groupby("Detail")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    
    figure = px.pie(topused,values="Production",names="Detail",color="Detail",color_discrete_sequence=px.colors.sequential.RdBu,title=title)
    return figure


def plot_locations_by_prodution(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    
    totalproductionby_locations = df.groupby('Location')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False)

    sayfa_boyutu = 6
    toplam_sayfa = (len(totalproductionby_locations.Location) - 1) // sayfa_boyutu + 1

    if "methodsayfa" not in st.session_state:
        st.session_state.methodsayfa = 1

    # Buton tıklamalarını kontrol etmek için flagler
    cc1,cc2,cc3 = st.columns(3)
    with cc1:
        geri_tiklandi = st.button("⬅️ Geri", key="Location_Geri")
    with cc2:    
        sifirla_tiklandi = st.button("🔄 Sıfırla", key="Location_Sifirla")
    with cc3:
        ileri_tiklandi = st.button("➡️ İleri", key="Location_Ileri")

    # Session state değerlerini güncelle
    if geri_tiklandi and st.session_state.methodsayfa > 1:
        st.session_state.methodsayfa -= 1
    if ileri_tiklandi and st.session_state.methodsayfa < toplam_sayfa:
        st.session_state.methodsayfa += 1
    if sifirla_tiklandi:
        st.session_state.methodsayfa = 1

    # Sayfaya göre verileri al
    başlangıç = (st.session_state.methodsayfa - 1) * sayfa_boyutu
    bitiş = başlangıç + sayfa_boyutu
    current_lcoations = totalproductionby_locations.iloc[başlangıç:bitiş]
    current_lcoations = current_lcoations.sort_values("Production")

    # Grafik oluştur
    fig = px.funnel(
        current_lcoations,
        x="Production",
        y="Location",
        color="Location",
        color_discrete_sequence=px.colors.sequential.RdBu,
        title="Fishery Areas with Total Productions"
    )
    fig.update_layout(
        font=dict(size=16),
        yaxis=dict(
            title_font=dict(size=18, color="red"),
            tickfont=dict(size=14, color="black")
        )
    )
    
    # Session state'in mevcut durumunu yazdır (Debugging için)
    #st.write(f"Mevcut Sayfa: {st.session_state.methodsayfa} / {toplam_sayfa}")

    return fig
