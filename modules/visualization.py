import pandas as pd
import plotly.express as px


def plot_production_increase(df):
    years = df.columns[4:]
    total_prodution = df[years].sum()
    fig = px.line(total_prodution,x = total_prodution.index, y = total_prodution.values, labels={"x":"Years","y":"Production"})
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


def plot_top_countries_by_production(df):
    years = df.columns[4:]
    top_countries = df.groupby('Country')[years].sum().sum(axis=1).reset_index(name='Production').sort_values('Production', ascending=False).head(10)
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    fig = px.bar(top_countries,x = "Production", y="Country", labels={'x': 'Production', 'y': 'Country'},color="Production",color_continuous_scale="RdBu",orientation='h')
    fig.update_yaxes(categoryorder='total ascending')
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



def plot_top_species_by_production(df):
    years = df.columns[4:]
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    species_total_production = df.groupby('Species')[years].sum().sum(axis = 1).reset_index(name = 'Production').sort_values('Production', ascending = False).head(10)
    fig = px.scatter(species_total_production,x = "Species",y = "Production",labels={"x":"Species","y":"Production"},color = "Production",color_continuous_scale = "RdBu",size="Production")
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


def plot_top_production_methods(df):
    years = df.columns[4:]
    topused = df.groupby("Detail")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    colorscale = {
    "Capture": 'rgb(0, 0, 255)',  # Lacivert
    "Marine Aq": 'rgb(100, 149, 237)',  # Orta mavi (Cornflower Blue)
    "Freshwater Aq": 'rgb(135, 206, 250)',  # Açık mavi (Light Sky Blue)
    "Brackish Aq": 'rgb(255,255,255) '  # Beyaz
    }

    figure = px.pie(topused,values="Production",names="Detail",color="Detail",color_discrete_sequence=px.colors.sequential.RdBu)
    return figure


def plot_locations_by_prodution(df):
    years = df.columns[4:]
    # Haritda kıta isimlerine göre göstermek için
    location_mapping = {
    "Asia - Inland waters": "Asia",
    "Mediterranean and Black Sea": "Mediterranean and Black Sea",
    "Europe - Inland waters": "Europe",
    "Africa - Inland waters": "Africa",
    "Pacific, Eastern Central": "Pacific (Eastern Central)",
    "Oceania - Inland waters": "Oceania",
    "Atlantic, Southeast": "Atlantic (Southeast)",
    "Atlantic, Eastern Central": "Atlantic (Eastern Central)",
    "Atlantic, Western Central": "Atlantic (Western Central)",
    "America, North - Inland waters": "North America",
    "America, South - Inland waters": "South America",
    "Atlantic, Antarctic": "Atlantic (Antarctic)",
    "Atlantic, Southwest": "Atlantic (Southwest)",
    "Pacific, Antarctic": "Pacific (Antarctic)",
    "Indian Ocean, Antarctic": "Indian Ocean (Antarctic)",
    "Indian Ocean, Eastern": "Indian Ocean (Eastern)",
    "Pacific, Southwest": "Pacific (Southwest)",
    "Pacific, Western Central": "Pacific (Western Central)",
    "Indian Ocean, Western": "Indian Ocean (Western)",
    "Atlantic, Northeast": "Atlantic (Northeast)",
    "Pacific, Southeast": "Pacific (Southeast)",
    "Atlantic, Northwest": "Atlantic (Northwest)",
    "Pacific, Northeast": "Pacific (Northeast)",
    "Pacific, Northwest": "Pacific (Northwest)",
    "Arctic Sea": "Arctic",
    "Former USSR area - Inland waters": "Former USSR"
    }

    totalproductionby_locations = df.groupby('Location')[years].sum().sum(axis = 1).reset_index(name = 'Production').sort_values('Production', ascending = False)
    totalloc = totalproductionby_locations.head(5).sort_values("Production",ascending = True)
    
    fig = px.funnel(totalloc,x = "Production",y = "Location",color="Location",color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(
        font=dict(size=16),  # Yazı boyutu
        yaxis=dict(
            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı rengi kırmızı
            tickfont=dict(size=14, color="black")   # Y eksen işaret yazı rengi siyah
        )
    )
    return fig















