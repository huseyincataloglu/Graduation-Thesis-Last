import pandas as pd
import plotly.express as px
import plotly as pl

def plot_species_totalprodamount(df,species,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    speciyproductions = df.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production")
    filteredcountryproductions = speciyproductions[speciyproductions.Species.isin(species)]
    figure = px.bar(filteredcountryproductions,x = "Species",y = "Production",color="Production",color_continuous_scale="RdBu")
    figure.update_layout(
        bargap = 0.7,
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            title_font=dict(size=18),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14)     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14)     # Y eksen işaret yazı boyutu
        ),
        coloraxis_colorbar=dict(
            title="Production",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure

def plot_speciesprdouction_by_detail(df,species,years,detail):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    speciyproductions = df.groupby(["Species","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    filteredspeciesproductions = speciyproductions[speciyproductions.Species.isin(species)]
    filteredspeciesproductions = filteredspeciesproductions[filteredspeciesproductions.Detail.isin(detail)]
    figure = px.treemap(filteredspeciesproductions,values="Production",path=[px.Constant("All"),"Detail","Species"],color="Production",color_continuous_scale="RdBu")
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        coloraxis_colorbar=dict(
            title="Production",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure

def plot_species_overyears(df,species,years):
    start, end = years
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    color_sequence = [f"rgb({color},{color},255)" for color in range(220,0,-20)]
    years1 = [str(year) for year in range(start,end+1,+1)]
    topcountries = df.groupby("Species")[years1].sum().reset_index()

    melted = pd.melt(topcountries,id_vars=["Species"],value_vars=years1)

    melted = melted[melted["Species"].isin(species)]

    melted.rename({"variable" : "Years", "value" : "Production"},axis = 1,inplace=True)
    figure = px.area(melted,x = "Years",y = "Production",color="Species",color_discrete_sequence=px.colors.sequential.RdBu)
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            gridwidth=1,
            title_font=dict(size=18),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14)     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14)     # Y eksen işaret yazı boyutu
        ),
        coloraxis_colorbar=dict(
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure

def plot_speciesondetails_overyears(df,species,years,detail):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]
    df = df.groupby(["Species","Detail"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Species","Detail"],value_vars=listyears,value_name="Production",var_name="Years")
    df_melted = df_melted[df_melted["Species"].isin(species)]
    df_melted = df_melted[df_melted["Detail"].isin(detail)]
    figure = px.line(df_melted,x = "Years",y = "Production", color="Detail",facet_col="Detail",facet_row="Species",facet_row_spacing=0.1,color_discrete_sequence=px.colors.sequential.RdBu)
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            gridcolor="white",  # Çizgilerin rengini beyaz yapar
            gridwidth=1,
            title_font=dict(size=18),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14)     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14)     # Y eksen işaret yazı boyutu
        ),
        legend=dict(
        title=dict(font=dict(size=16)),  # Legend başlığı yazı boyutu
        font=dict(size=14),              # Legend öğelerinin yazı boyutu
        itemclick="toggleothers",        # Legend öğelerinin tıklama davranışı
        itemsizing="constant",           # Legend simge boyutunu sabit tutar
        traceorder="normal",             # Legend sıralama düzeni
        )
    )
    figure.for_each_yaxis(lambda yaxis: yaxis.update(title_text = "",tickfont=dict(color='black', size=18),title_font=dict(color='red',size=18)))
    figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=18),title_font=dict(color='red',size=18)))
    figure.for_each_annotation(lambda a : a.update(text = ""))
    return figure


