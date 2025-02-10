import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_locationbox_allyears(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]
    df2 = pd.DataFrame(df[years].sum(),columns=["Production"])
   
    figure = px.histogram(df2,x = "Production",marginal="box",title=f"Distribution of Total Production Values In Years")
    figure.update_layout(
        width = 800,
        height = 500
    )
    return figure


def plot_funnel_hiearchi(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1)]

    detail = df.groupby("Detail")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    detail = detail[detail["Production"] == detail["Production"].max()]
    locat = df[df["Detail"] == detail["Detail"].values[0]]
    locat = locat.groupby("Location")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    locat = locat[locat["Production"] == locat["Production"].max()]
    countr = df[(df["Detail"] == detail["Detail"].values[0]) & (df["Location"] == locat["Location"].values[0])]
    countr = countr.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    countr = countr[countr["Production"] == countr["Production"].max()]
    species = df[(df["Detail"] == detail["Detail"].values[0]) & (df["Location"] == locat["Location"].values[0]) & (df["Country"] == countr["Country"].values[0])]
    species = species.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    species = species[species["Production"] == species["Production"].max()]

    data_funnel = pd.DataFrame({"Stage" : [f"Method","Location","Country","Species"], "Category": [detail["Detail"].values[0], locat["Location"].values[0], countr["Country"].values[0], species["Species"].values[0]],  # Her aşamanın en yüksek değeri
        "Production": [detail["Production"].values[0], locat["Production"].values[0], countr["Production"].values[0], species["Production"].values[0]]})
    data_funnel.sort_values("Production",ascending=True,inplace=True)

    fig = px.funnel(data_funnel,
                x = "Production",
                y = "Category",
                color = "Category",
                title="Funnel Chart for Highest Productions Hierarchi")

    return fig



    

def plot_production_increase(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    title = f"Production Change Over Years In All Areas"    
    total_prodution = df[years].sum()

    fig = px.line(total_prodution,
                x = total_prodution.index,
                y = total_prodution.values,
                labels={"x":"Years","y":"Production"},
                title=title)
    
    fig.update_traces(line = dict(color = "#31333F",width = 3))
    fig.update_layout(xaxis_title="Years",yaxis_title="Production")
    fig.update_layout(
        width = 600,
        height = 500,
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



def plot_top_countries_by_production(df, years):
    start, end = years
    year_list = [str(year) for year in range(start, end + 1)]
    
    title = "Which Countries Produced the Most Over Time (Cumulative)"

   
    production_over_time = df.groupby('Country')[year_list].sum()

    
    cumulative_production = production_over_time.cumsum(axis=1).reset_index()

   
    melted_df = pd.melt(
        cumulative_production, 
        id_vars=["Country"], 
        value_vars=year_list, 
        var_name="Year", 
        value_name="Cumulative_Production"
    )
    melted_df = melted_df[melted_df["Country"] != "China"]
    
    fig = px.choropleth(
        melted_df,
        locations="Country",
        locationmode="country names",
        color="Cumulative_Production",
        animation_frame="Year",  
        color_continuous_scale="RdBu",
        title=title
    )
    
    fig.update_layout(
        width=1000,  
        height=600,  
        geo=dict(
            projection_type='natural earth',  
            showcoastlines=True,  
            coastlinecolor="Black",  
        ),
    )
    fig.write_html("cumulative_production_map.html")
    
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


    
    col1, col2, col3 = st.columns([1, 1, 1]) 
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
        width = 700,
        height = 500,
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



def plot_top_production_methods(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]

    title = f"Which Production methods are widely used in All Areas"   
    topused = df.groupby("Detail")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    
    fig = go.Figure(data=[go.Pie(labels=topused["Detail"], values=topused["Production"], pull=[0, 0, 0.2, 0.3])])
    fig.update_layout(
        title = title,
        width = 600,
        height = 600
    )
    return fig


def plot_locations_by_prodution(df,years):
    start ,end = years
    years = [str(year) for year in range(start,end+1)]
    
    totalproductionby_locations = df.groupby('Location')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False)

    sayfa_boyutu = 6
    toplam_sayfa = (len(totalproductionby_locations.Location) - 1) // sayfa_boyutu + 1

    if "methodsayfa" not in st.session_state:
        st.session_state.methodsayfa = 1

    
    cc1,cc2,cc3 = st.columns(3)
    with cc1:
        geri_tiklandi = st.button("⬅️ Geri", key="Location_Geri")
    with cc2:    
        sifirla_tiklandi = st.button("🔄 Sıfırla", key="Location_Sifirla")
    with cc3:
        ileri_tiklandi = st.button("➡️ İleri", key="Location_Ileri")

    
    if geri_tiklandi and st.session_state.methodsayfa > 1:
        st.session_state.methodsayfa -= 1
    if ileri_tiklandi and st.session_state.methodsayfa < toplam_sayfa:
        st.session_state.methodsayfa += 1
    if sifirla_tiklandi:
        st.session_state.methodsayfa = 1

    
    başlangıç = (st.session_state.methodsayfa - 1) * sayfa_boyutu
    bitiş = başlangıç + sayfa_boyutu
    current_lcoations = totalproductionby_locations.iloc[başlangıç:bitiş]
    current_lcoations = current_lcoations.sort_values("Production",ascending = True)

    
    fig = px.bar(
        current_lcoations,
        x = "Production",
        y = "Location",
        color="Production",
        color_continuous_scale=px.colors.sequential.RdBu,
        title="Fishery Areas with Total Productions H Bar Chart",
        orientation="h"
    )
    fig.update_layout(
        width = 700,
        height = 600,
        font=dict(size=16),
        yaxis=dict(
            title_font=dict(size=18, color="red"),
            tickfont=dict(size=14, color="black")
        )
    )
    

    return fig


