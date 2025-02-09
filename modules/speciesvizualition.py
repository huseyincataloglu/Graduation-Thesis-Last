import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly as pl
import streamlit as st


def plot_proddist_boxplotspecies(df,species,years,locations = None,methods = None,countries = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No specy selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    if len(species) > 0:
        if methods:
            df = df[df["Detail"].isin(methods)]
    
        df = df[df["Species"].isin(species)]
        columns = len(species)
        if countries:
            df = df[df["Country"].isin(countries)]
        if locations:
            df = df[df["Location"].isin(locations)]
    
        grouped = df.groupby("Species")[years].sum().reset_index()
        melted = pd.melt(grouped,id_vars=["Species"],value_vars=years,var_name="Years",value_name="Production")
        fig = make_subplots(rows = 1,cols=columns)
        i = 1
        for specy in species:
            melted1 = melted[melted["Species"] == specy]
            fig.add_trace(go.Box(x = melted1["Species"],y = melted1["Production"],name=specy),row = 1,col=i)
            i += 1
        fig.update_layout(
            title=dict(text='Box Plot of Annual Production Distribution by Species"',font=dict(size=24, color="red")),
            showlegend=False,
            height=400,
            width=300 * len(species), 
        )        

        return fig


def plot_participation_by_species(df, species, years,locations = None,methods = None,countries= None):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    if len(species) > 0:
        if locations:
            df = df[df["Location"].isin(locations)]
        if methods:
            df = df[df["Detail"].isin(methods)]

        if countries:
            df = df[df["Country"].isin(countries)]        
        df_filtered = df[df["Species"].isin(species)]

        
        participation_count = df_filtered['Species'].value_counts().reset_index()
        participation_count.columns = ['Species', 'Participation Count']
        
       
        fig = px.bar(participation_count, x='Species', y='Participation Count', color='Species', 
                    title="Production Participation Count by Species", 
                    labels={'Participation Count': 'Number of Participation'},
                    color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
            title=dict(font=dict(size=24, color="red")),
            font=dict(size=16),  # Yazı boyutu
            xaxis=dict(
                gridwidth=1,
                title_font=dict(size=18,color="red"),  # X eksen başlık yazı boyutu
                tickfont=dict(size=14,color="black")     # X eksen işaret yazı boyutu
            ),
            yaxis=dict(
                gridwidth=1,
                title_font=dict(size=18,color="red"),  # Y eksen başlık yazı boyutu
                tickfont=dict(size=14,color="black")     # Y eksen işaret yazı boyutu
            ),
            coloraxis_colorbar=dict(       # Renk skalası başlığı
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
            )
        )
        return fig
    else:
        return None    


def plot_proddistspecies_yearly(df, species, years):
    years = [str(year) for year in years]
    
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one country.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig

    df = df[df["Species"].isin(species)]

    # Eğer yıllar seçilmemişse, uyarı ver ve boş grafik döndür
    if len(years) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No years selected. Please select at least one year.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            height=400,
            width=600,
            showlegend=False
        )
        return fig
    
    türler = df.Species.unique()
    türrenkleri = {tür: f"rgb({np.random.randint(0, 255)}, {np.random.randint(0, 255)}, {np.random.randint(0, 255)})" for tür in türler}
    #
    fig = go.Figure()

    for year in years:
        
        year_data = df[df["Species"].isin(species)][["Species", str(year)]]

        for specy in species:
            specy_data = year_data[year_data["Species"] == specy]
            fig.add_trace(
                go.Box(
                    x=[year] * len(specy_data), 
                    y=specy_data[str(year)],     
                    name=specy,                  
                    marker=dict(color=türrenkleri[specy]),
                    showlegend=(year == years[0])              
                )
            )

    
    fig.update_layout(
        title="Production Distribution By Year And Specy",
        xaxis_title="Year",
        yaxis_title="Production",
        height=600,
        width=1000,
        showlegend=True,
        boxmode = "group"
    )
    return fig


def plot_speciesmethpd_paralelcat(df, species, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    
    if not species:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one species.",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400, width=600,
        )
        return fig

    df = df[df["Species"].isin(species)]

    method_grouped = df.groupby(["Species", "Detail"])[years].sum().sum(axis=1).reset_index(name="Total Production")
    method_part = df.loc[:, ["Species", "Detail"]]
    method_part = method_part.merge(method_grouped, on=["Species", "Detail"], how="left")
   
    fig = px.parallel_categories(
        method_part,
        dimensions=["Species", "Detail"],
        color="Total Production",
        color_continuous_scale="Viridis", 
        title="Species and Methods Frequencies Colored by Total Production"
    )

    fig.update_layout(
        title=dict(font=dict(color="black")),
        font=dict(size=18), 
        coloraxis_colorbar=dict(
            title="Production",
            title_font=dict(size=16),
            tickfont=dict(size=14)
        ),
        paper_bgcolor="white", 
        plot_bgcolor="white",
        margin=dict(l=50, r=50, t=80, b=50)  
    )

    return fig

def plot_partvsprod_by_species(df, species, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df1 = df.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production")
        participation_count = df['Species'].value_counts().reset_index()
        participation_count.columns = ['Species', 'Participation Count']
        df1 = df1.merge(participation_count,on = "Species",how = "left")

        figure = px.scatter(df1, x = "Participation Count", y = "Production",color = "Species",title= "Total Participation vs Total Production Amount",size="Production")
        figure.update_layout(
            title=dict(font=dict(size=20, color="black")),
            font=dict(size=16),  # Yazı boyutu
            xaxis=dict(
                gridwidth=1    
            ),
            yaxis=dict(
                gridwidth=1
            ),
            coloraxis_colorbar=dict(     
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
            )
        )
        return figure



def plot_species_overyears(df, species, years):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, +1)]
    
    topcountries = df.groupby("Species")[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    fig = go.Figure()
    for specy in species:
        filtered = melted[melted["Species"] == specy]
        fig.add_trace(go.Bar(x=filtered["Years"],y=filtered["Production"], name=f'{specy}'))
                 
    fig.update_layout(
        title=dict(text='Species Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15,
        bargroupgap=0.1
    )
    return fig




def plot_speciesmethods_overyears(df, species, years,methods):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Detail"].isin(methods)]
    topcountries = df.groupby(["Species","Detail"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Detail"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    if len(species) == 1:
        fig = px.bar(melted,x = "Years",y = "Production",color="Detail",color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
        title=dict(text='Specy And Related Methods Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,detail in enumerate(df.Detail.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Species",pattern_shape="Detail",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Plotly)
                 
    fig.update_layout(
        title=dict(text='Species And Related Methods Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_specieslocats_overyears(df, species, years,locations):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Location"].isin(locations)]
    topcountries = df.groupby(["Species","Location"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Location"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    if len(species) == 1:
        fig = px.bar(melted,x = "Years",y = "Production",color="Location",color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(
        title=dict(text='Specy And Related Methods Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,loc in enumerate(df.Location.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Species",pattern_shape="Location",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Plotly)
                 
    fig.update_layout(
        title=dict(text='Species And Related Locations Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_specieslocats_methodsoveryears(df, species, years,locations,methods):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    topcountries = df.groupby(["Species","Location","Detail"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Location","Detail"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    if len(species) == 1:
        pattern_list = [
            "-",  # Yatay çizgi
            "|",  # Dikey çizgi
            "+",  # Artı işareti
            "/",  # Eğik çizgi
            "\\", # Ters eğik çizgi
            "x",  # Çarpı işareti
            "."   # Nokta
        ]
        pattern_map = [pattern_list[i] for i,loc in enumerate(df.Detail.unique(),start = 0)]
        fig = px.bar(melted,x = "Years",y = "Production",color="Location",color_discrete_sequence=px.colors.qualitative.Plotly,pattern_shape="Detail",pattern_shape_sequence=pattern_map)
        fig.update_layout(
        title=dict(text='Specy,Location And Related Methods Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
         "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,detal in enumerate(df.Detail.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Location",pattern_shape="Detail",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Plotly,facet_col="Species",facet_col_spacing=0.1)
                 
    fig.update_layout(
        title_text="Species, Methods, and Related Locations Production Over Time",
        xaxis_title="Years",
        yaxis_title="Total Production",
        plot_bgcolor='white',
        height=700,
        legend=dict(
            x=0, y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15,
        bargroupgap=0.1
    )
    return fig


def plot_specieslocats_countroveryears(df, species, years,locations,countries):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    topcountries = df.groupby(["Species","Location","Country"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Location","Country"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)

    if len(species) == 1:
        pattern_list = [
            "-",  # Yatay çizgi
            "|",  # Dikey çizgi
            "+",  # Artı işareti
            "/",  # Eğik çizgi
            "\\", # Ters eğik çizgi
            "x",  # Çarpı işareti
            "."   # Nokta
        ]
        pattern_map = [pattern_list[i] for i,locat in enumerate(df.Location.unique(),start = 0)]
        fig = px.bar(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.qualitative.Set1,pattern_shape="Location",pattern_shape_sequence=pattern_map)
        fig.update_layout(
        title=dict(text='Specy,Location And Related Countries Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
            "-",  # Yatay çizgi
            "|",  # Dikey çizgi
            "+",  # Artı işareti
            "/",  # Eğik çizgi
            "\\", # Ters eğik çizgi
            "x",  # Çarpı işareti
            "."   # Nokta
        ]
    pattern_map = [pattern_list[i] for i,locat in enumerate(df.Location.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Country",pattern_shape="Location",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Set1,facet_col="Species",facet_col_spacing=0.1)
                 
    fig.update_layout(
        title=dict(text='Species,Methods And Related Locations Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_speciesountries_overyears(df, species, years,countries):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Country"].isin(countries)]
    topcountries = df.groupby(["Species","Country"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Country"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    if len(species) == 1:
        fig = px.bar(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
        title=dict(text='Specy And Related Countries Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,countr in enumerate(df.Country.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Species",pattern_shape="Country",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Set1)
                 
    fig.update_layout(
        title=dict(text='Species And Related Countries Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_speciesmethod_countoveryears(df, species, years,methods,countries):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]
    topcountries = df.groupby(["Species","Country","Detail"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Country","Detail"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    if len(species) == 1:
        pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
        ]
        pattern_map = [pattern_list[i] for i,loc in enumerate(df.Detail.unique(),start = 0)]
        fig = px.bar(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.qualitative.Set1,pattern_shape="Detail",pattern_shape_sequence=pattern_map)
        fig.update_layout(
        title=dict(text='Specy,Countries And Related Methods Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,detal in enumerate(df.Detail.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",
                y = "Production",
                color="Country",
                pattern_shape="Detail",
                pattern_shape_sequence=pattern_map,
                color_discrete_sequence=px.colors.qualitative.Set1,
                facet_col="Species",
                facet_col_spacing=0.1)
                 
    fig.update_layout(
        title=dict(text='Species,Methods And Related Countries Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_specieslocat_methcountroveryears(df, species, years,locations,methods,countries):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, 3)]
    
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Country"].isin(countries)]
    topcountries = df.groupby(["Species","Location","Detail","Country"])[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species","Location","Detail","Country"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)

    if len(species) == 1:
        pattern_list = [
            "-",  # Yatay çizgi
            "|",  # Dikey çizgi
            "+",  # Artı işareti
            "/",  # Eğik çizgi
            "\\", # Ters eğik çizgi
            "x",  # Çarpı işareti
            "."   # Nokta
        ]
        pattern_map = [pattern_list[i] for i,loc in enumerate(df.Detail.unique(),start = 0)]
        fig = px.bar(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.qualitative.Set1,pattern_shape="Detail",pattern_shape_sequence=pattern_map,facet_col="Location",facet_col_spacing=0.07,facet_col_wrap=4,facet_row_spacing=0.1)
        fig.update_layout(
        title=dict(text='Specy,Location,Methods And Related Location Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    pattern_map = [pattern_list[i] for i,detal in enumerate(df.Detail.unique(),start = 0)]
    fig  = px.bar(melted,x = "Years",y = "Production",color="Country",pattern_shape="Detail",pattern_shape_sequence=pattern_map,color_discrete_sequence=px.colors.qualitative.Set1,facet_col="Species",facet_col_spacing=0.1,facet_row="Location",facet_row_spacing=0.07)
                 
    fig.update_layout(
        title=dict(text='Species,Methods,Countries And Related Locations Production Distributions Over Time'),
        height = 700,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='stack',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig


def plot_speciespolar(df, species, years):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
   
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        grouped = df.groupby("Species")[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        fig = px.bar_polar(
            grouped,
            r="Production",
            theta="Species",
            color="Production",
            title="🌿 Species Total Productions (Polar Bar Chart)",
            color_continuous_scale=px.colors.sequential.Tealgrn
        )
        
        # 📌 **Gelişmiş Grafik Düzenlemeleri**
        fig.update_traces(marker=dict(
            line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
            opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
        ))

        fig.update_layout(
            width=850,
            height=850,
            polar=dict(
                bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
            ),
            title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
            coloraxis_colorbar=dict(
                title="Production Level", tickfont=dict(size=12)
            )
        )
        return fig

def plot_speciesmethodspolar(df, species, years,methods):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Detail"].isin(methods)]
        grouped = df.groupby(["Species","Detail"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) > 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Detail",
                title="🌿 Species And Methods Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Detail",
                color="Detail",
                title="🌿 Specy And Methods Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig

    

def plot_speciescountries_polar(df, species, years,countries):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Country"].isin(countries)]
        grouped = df.groupby(["Species","Country"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) > 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Country",
                title="🌿 Species And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Country",
                color="Country",
                title="🌿 Specy And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig


def plot_specieslocat_polar(df, species, years,locations):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby(["Species","Location"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) > 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Location",
                title="🌿 Species And Locations Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Location",
                color="Location",
                title="🌿 Specy And Locations Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig


def plot_speciesmethods_locatpolar(df, species, years,locations,methods):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Detail"].isin(methods)]
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby(["Species","Detail","Location"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) == 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Location",
                color="Detail",
                title="🌿 Specy ,Location And Methods Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Location",
                pattern_shape="Detail",
                pattern_shape_sequence=pattern_list,
                title="🌿 Species ,Location And Methods Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig

        
def plot_speciescountr_methodpolar(df, species, years,methods,countries):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Country"].isin(countries)]
        df = df[df["Detail"].isin(methods)]
        grouped = df.groupby(["Species","Country","Detail"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) == 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Country",
                color="Detail",
                title="🌿 Specy ,Methods And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
           
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5), 
                opacity=0.8  
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Country",
                pattern_shape="Detail",
                pattern_shape_sequence=pattern_list,
                title="🌿 Species ,Method And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  
                opacity=0.8 
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig


def plot_speciescountr_locatpolar(df, species, years,locations,countries):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    pattern_list = [
        "-",  # Yatay çizgi
        "|",  # Dikey çizgi
        "+",  # Artı işareti
        "/",  # Eğik çizgi
        "\\", # Ters eğik çizgi
        "x",  # Çarpı işareti
        "."   # Nokta
    ]
    if len(species) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No species selected. Please select at least one specy.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df[df["Country"].isin(countries)]
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby(["Species","Country","Location"])[listyears].sum().sum(axis=1).reset_index(name="Production")
        
        if len(species) == 1:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Country",
                color="Location",
                title="🌿 Specy ,Locations And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig
        else:
            fig = px.bar_polar(
                grouped,
                r="Production",
                theta="Species",
                color="Country",
                pattern_shape="Location",
                pattern_shape_sequence=pattern_list,
                title="🌿 Species ,Locations And Countries Total Productions (Polar Bar Chart)",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            # 📌 **Gelişmiş Grafik Düzenlemeleri**
            fig.update_traces(marker=dict(
                line=dict(color="black", width=1.5),  # Çubukların kenar çizgisi
                opacity=0.8  # Hafif şeffaflık ekleyerek daha yumuşak bir görünüm sağlar
            ))

            fig.update_layout(
                width=850,
                height=850,
                polar=dict(
                    bgcolor="#f8f9fa",  # Arkaplanı açık gri yaparak şık bir görünüm
                    angularaxis=dict(showgrid=False, linewidth=1, linecolor="gray"),
                    radialaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
                ),
                title_font=dict(size=20, family="Arial", color="#2C3E50"),  # Başlık stili
                coloraxis_colorbar=dict(tickfont=dict(size=12)
                )
            )
            return fig




def plot_histogram_yearlytotal(df, species, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1, 1)]
    df = df[df["Species"].isin(species)]    

    if len(years) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No years selected. Please select at least one year or species.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="No Data Available",
            showlegend=False,
            height=400,
            width=600,
            hoverinfo="x+y+name"
        )
        return fig
    else:
        df = df[df["Species"].isin(species)]
        df = df.groupby("Species")[years].sum().reset_index()
        melted= pd.melt(df,id_vars="Species",value_vars=years,value_name="Production",var_name="Years")
        figure = px.histogram(melted,x = "Production",color="Species",marginal="box",title="Annual Total Production Distribution By Species")
        figure.update_layout(
            title=dict(font=dict(size=15, color="black")),
            height = 800
        )
        return figure



def plot_specylocatmethods_countr_sankey(df, species, years, locations, methods, countries):
    start, end = years
    years = [str(year) for year in range(start, end + 1, 1)]

    df = df[df["Species"].isin(species)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Country"].isin(countries)]

    totalproductions = df.groupby(["Country", "Location", "Detail", "Species"])[years].sum().sum(axis=1).reset_index(name="Production").sort_values("Production", ascending=False)
    
    uniquecountry = list(totalproductions.Country.unique())
    uniquelocations = list(totalproductions.Location.unique())
    uniquedetails = list(totalproductions.Detail.unique())
    uniquespecies = list(totalproductions.Species.unique())
    all_nodes = uniquecountry + uniquelocations + uniquedetails + uniquespecies

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[specy] for specy in totalproductions["Species"]]
    target = [node_dict[detail] for detail in totalproductions["Detail"]]
    values = totalproductions["Production"].tolist()

    sources += [node_dict[detail] for detail in totalproductions["Detail"]]
    target += [node_dict[locat] for locat in totalproductions["Location"]]
    values += totalproductions["Production"].tolist()

    sources += [node_dict[locat] for locat in totalproductions["Location"]]
    target += [node_dict[countr] for countr in totalproductions["Country"]]
    values += totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)]
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocations)]
    detail_colors = px.colors.qualitative.Set1[:len(uniquedetails)]
    species_colors = px.colors.qualitative.Dark2[:len(uniquespecies)]
    node_colors = country_colors + location_colors + detail_colors + species_colors

    
    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 

   
    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=20,  
                thickness=15,  
                label=all_nodes,
                color=node_colors
            ),
            link=dict(
                source=sources,
                target=target,
                value=values,
                color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] 
            )
        )
    )

    
    fig.update_layout(
        title="Species-Method-Location-Country Total Productions Using Sankey Chart",
        title_font=dict(size=20, family="Arial", color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")  
    )
    return fig