import pandas as pd
import plotly.express as px


# Countries Page Plots
def plot_countries_by_production(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    countryproductions = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
    filteredcountryproductions = countryproductions[countryproductions.Country.isin(countries)]
    figure = px.bar(filteredcountryproductions,x = "Country",y = "Production",color="Production",color_continuous_scale="RdBu")
    figure.update_layout(
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
        coloraxis_colorbar=dict(
            title="Production",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure




def plot_countrieswithcommonspecies(df,countries,common_species,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(common_species)]
    totalproductions = df.groupby(["Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    figure = px.bar(totalproductions,x = "Production", y = "Country",color="Species",color_discrete_sequence=px.colors.sequential.RdBu,orientation="h")
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            title_font=dict(size=18,color = "red"),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth = 1,
            title_font=dict(size=18,color = "red"),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # Y eksen işaret yazı boyutu
        ),
        coloraxis_colorbar=dict(
            title="Species",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure





def plot_countrieswithspecies(df,countries,species,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]
    totalproductions = df.groupby(["Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    figure = px.bar(totalproductions,x = "Production", y = "Country",color="Species",color_discrete_sequence=px.colors.sequential.RdBu,orientation="h")
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            title_font=dict(size=18,color = "red"),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth = 1,
            title_font=dict(size=18,color = "red"),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # Y eksen işaret yazı boyutu
        ),
        coloraxis_colorbar=dict(
            title="Species",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure





def plot_countryprod_by_time(df,countries,years):
    start, end = years
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    color_sequence = [f"rgb({color},{color},255)" for color in range(220,0,-20)]
    years1 = [str(year) for year in range(start,end+1,+1)]
    topcountries = df.groupby("Country")[years1].sum().reset_index()

    melted = pd.melt(topcountries,id_vars=["Country"],value_vars=years1)

    melted = melted[melted["Country"].isin(countries)]

    melted.rename({"variable" : "Years", "value" : "Production"},axis = 1,inplace=True)
    figure = px.area(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.sequential.RdBu)
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            gridwidth=1,
            title_font=dict(size=18,color = "red"),  # X eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # X eksen işaret yazı boyutu
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18,color = "red"),  # Y eksen başlık yazı boyutu
            tickfont=dict(size=14,color = "black")     # Y eksen işaret yazı boyutu
        ),
        coloraxis_colorbar=dict(
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure


def plot_countrycommonspeciesprod_by_time(df,countries,common_species,years):
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]
    df = df.groupby(["Country","Species"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species"],value_vars=listyears,value_name="Production",var_name="Years")
    df_melted = df_melted[df_melted["Country"].isin(countries)]
    df_melted = df_melted[df_melted["Species"].isin(common_species)]
    figure = px.scatter(df_melted,x = "Years",y = "Production", color="Species",symbol="Country",size="Production",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Species",facet_row="Country")
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
    figure.for_each_annotation(lambda annotation: annotation.update(text=""))
    figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    return figure




def plot_countryspeciesprod_by_time(df,countries,species,years):
    colorscale = ['rgb(255, 255, 255)', 'rgb(0, 0, 255)']
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]
    df = df.groupby(["Country","Species"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species"],value_vars=listyears,value_name="Production",var_name="Years")
    df_melted = df_melted[df_melted["Country"].isin(countries)]
    df_melted = df_melted[df_melted["Species"].isin(species)]
    figure = px.scatter(df_melted,x = "Years",y = "Production", color="Species",symbol="Country",size="Production",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Species",facet_row="Country")
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
    figure.for_each_annotation(lambda annotation: annotation.update(text=""))
    figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    return figure

def plot_country_productiondetail(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    color_sequence = [f"rgb({color},{color},255)" for color in range(255,0,-15)]
    df = df.groupby(["Country","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    df = df[df["Country"].isin(countries)]
    figure = px.bar(df,x="Country",y = "Production",color="Detail",barmode="group",color_discrete_sequence=px.colors.sequential.RdBu)
    figure.update_layout(
        font=dict(size=16),  # Yazı boyutu
        xaxis=dict(
            gridcolor="white",  # Çizgilerin rengini beyaz yapar
            gridwidth=0.5,
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
    return figure