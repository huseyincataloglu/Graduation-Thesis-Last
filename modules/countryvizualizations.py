import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import kaleido


# Countries Page Plots

#def plot_countryfreq_qual(df,countries,years, locations = None,methods = None)

def plot_proddist_boxplot(df,countries,years,locations = None,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if len(countries) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No countries selected. Please select at least one country.",
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
    if len(countries) > 0:
        if methods:
            df = df[df["Detail"].isin(methods)]
    
        df = df[df["Country"].isin(countries)]

        if locations:
            df = df[df["Location"].isin(locations)]
    
        grouped = df.groupby("Country")[years].sum().reset_index()
        melted = pd.melt(grouped,id_vars=["Country"],value_vars=years,var_name="Years",value_name="Production")
        fig = go.Figure()
        i = 1
        for country in countries:
            melted1 = melted[melted["Country"] == country]
            fig.add_trace(go.Box(x = melted1["Country"],y = melted1["Production"],name=country,jitter=0.3,pointpos=-1.8, boxpoints='all'))
            i += 1
        fig.update_layout(
            title="Box Plot of Annual Production Distribution by Country",
            showlegend=False,
            height=400,
            width=300 * len(countries),  
        )        

        return fig
    

def plot_proddist_yearly(df, countries, years, locations=None, methods=None):
    years = [str(year) for year in years]
    

    if len(countries) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No countries selected. Please select at least one country.",
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

    if methods:
        df = df[df["Detail"].isin(methods)]
    if locations:
        df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]

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
    
    ulkeler = df.Country.unique()
    ülkerenkleri = {ulke: f"rgb({np.random.randint(0, 255)}, {np.random.randint(0, 255)}, {np.random.randint(0, 255)})" for ulke in ulkeler}
    # Boxplot için veriyi hazırlayalım
    fig = go.Figure()

    for year in years:
        # Yıl için veriyi al
        year_data = df[df["Country"].isin(countries)][["Country", str(year)]]

        # Ülkeleri gruplamak için her ülke için ayrı boxplot ekle
        for country in countries:
            country_data = year_data[year_data["Country"] == country]
            fig.add_trace(
                go.Box(
                    x=[year] * len(country_data),  # X ekseninde yıl
                    y=country_data[str(year)],     # Y ekseninde o yılın üretim verisi
                    name=country,                  # Boxplot ismi ülke olacak
                    marker=dict(color=ülkerenkleri[country]),
                    showlegend=(year == years[0])              
                )
            )

    # Grafik düzenlemelerini yapalım
    fig.update_layout(
        title="Production Distribution by Year and Country",
        xaxis_title="Year",
        yaxis_title="Production",
        height=500,
        width=1000,
        showlegend=True,
        boxmode = "group"
    )

    return fig


def plot_countrymethpd_paralelcat(df,countries,years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    if len(countries) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No countries selected. Please select at least one country.",
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
    if len(countries) > 0:
        df= df[df["Country"].isin(countries)]
        methodgrouped = df.groupby(["Country","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production")
        methodpart = df.loc[:,["Country","Detail"]]
        methodpart = methodpart.merge(methodgrouped,on = ["Country","Detail"],how= "left")
        fig = px.parallel_categories(methodpart,dimensions=["Country","Detail"],color="Production",color_continuous_scale="RdBu",title="Countries And Methods Frequencies Colored By Total Production")
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

def plot_partvsprod_by_country(df, countries, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if len(countries) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No countries selected. Please select at least one country.",
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
        df = df[df["Country"].isin(countries)]
        df1 = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
        participation_count = df['Country'].value_counts().reset_index()
        participation_count.columns = ['Country', 'Participation Count']
        df1 = df1.merge(participation_count,on = "Country",how = "left")

        figure = px.scatter(df1, x = "Participation Count", y = "Production",color = "Country",title= "Total Participation vs Total Production Amount",size="Production")
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
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
            )
        )
        return figure





        




def plot_countries_prod_map(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    title = "Total Productions By Countries Map"
    countryproductions = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
    countryproductions = countryproductions[countryproductions.Country.isin(countries)]
    figure = px.choropleth(countryproductions,locations="Country",locationmode="country names",color="Country",title=title,hover_data="Production")
    figure.update_layout(
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
    return figure
    



def plot_countrieswithspecies(df,countries,species,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]
    totalproductions = df.groupby(["Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquespecies = list(totalproductions.Species.unique())
    all_nodes = uniquecountry + uniquespecies

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Species"]]
    values = totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquespecies)]  
    node_colors = country_colors + location_colors  

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title =  "Countries-Species Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig


def plot_countrmethod_sankey(df,countries,years,methods):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]
    totalproductions = df.groupby(["Country","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquedetails = list(totalproductions.Detail.unique())
    all_nodes = uniquecountry + uniquedetails

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Detail"]]
    values = totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    detail_colors = px.colors.qualitative.Pastel[:len(uniquedetails)]  
    node_colors = country_colors + detail_colors

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title =  "Countries-Methods Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig


def plot_countrmethodspecy_sankey(df,countries,years,methods,species):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Species"].isin(species)]
    totalproductions = df.groupby(["Country","Detail","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquedetails = list(totalproductions.Detail.unique())
    uniquespecies = list(totalproductions.Species.unique())
    all_nodes = uniquecountry + uniquedetails + uniquespecies

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Detail"]]
    values = totalproductions["Production"].tolist()

    sources += [node_dict[detail] for detail in totalproductions["Detail"]]
    target += [node_dict[specy] for specy in totalproductions["Species"]]
    values += totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquedetails)]  
    species_colors = px.colors.qualitative.Set1[:len(uniquespecies)]
    node_colors = country_colors + location_colors + species_colors

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title =  "Countries-Methods-Species Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig

def plot_countrlocat_sankey(df,countries,years,locations):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]
    totalproductions = df.groupby(["Country","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquelocats = list(totalproductions.Location.unique())
    all_nodes = uniquecountry + uniquelocats

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Location"]]
    values = totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocats)]  
    node_colors = country_colors + location_colors  

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
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
        ))
    )
    fig.update_layout(
        title =  "Countries-Locations Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig

def plot_countrlocatspecy_sankey(df,countries,years,locations,species):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Species"].isin(species)]
    totalproductions = df.groupby(["Country","Location","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquelocations = list(totalproductions.Location.unique())
    uniquespecies = list(totalproductions.Species.unique())
    all_nodes = uniquecountry + uniquelocations + uniquespecies

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Location"]]
    values = totalproductions["Production"].tolist()

    sources += [node_dict[locat] for locat in totalproductions["Location"]]
    target += [node_dict[specy] for specy in totalproductions["Species"]]
    values += totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocations)]  
    species_colors = px.colors.qualitative.Set1[:len(uniquespecies)]
    node_colors = country_colors + location_colors + species_colors

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title =  "Countries-Locations-Species Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig

def plot_countrlocatmethod_sankey(df,countries,years,locations,methods):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    totalproductions = df.groupby(["Country","Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquelocations = list(totalproductions.Location.unique())
    uniquedetails = list(totalproductions.Detail.unique())
    all_nodes = uniquecountry + uniquelocations + uniquedetails

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Location"]]
    values = totalproductions["Production"].tolist()

    sources += [node_dict[locat] for locat in totalproductions["Location"]]
    target += [node_dict[detail] for detail in totalproductions["Detail"]]
    values += totalproductions["Production"].tolist()

    
    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocations)]  
    detail_colors = px.colors.qualitative.Set1[:len(uniquedetails)]
    node_colors = country_colors + location_colors + detail_colors

    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title = "Countries-Locations-Methods Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig

def plot_countrlocatmethodspecy_sankey(df,countries,years,locations,methods,species):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
 
    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Species"].isin(species)]

    totalproductions = df.groupby(["Country","Location","Detail","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    uniquecountry = list(totalproductions.Country.unique())
    uniquelocations = list(totalproductions.Location.unique())
    uniquedetails = list(totalproductions.Detail.unique())
    uniquespecies = list(totalproductions.Species.unique())
    all_nodes = uniquecountry + uniquelocations + uniquedetails + uniquespecies

    node_dict = {node: i for i, node in enumerate(all_nodes)}

    sources = [node_dict[country] for country in totalproductions["Country"]]
    target = [node_dict[locat] for locat in totalproductions["Location"]]
    values = totalproductions["Production"].tolist()

    sources += [node_dict[locat] for locat in totalproductions["Location"]]
    target += [node_dict[detail] for detail in totalproductions["Detail"]]
    values += totalproductions["Production"].tolist()

    sources += [node_dict[detail] for detail in totalproductions["Detail"]]
    target += [node_dict[species] for species in totalproductions["Species"]]
    values += totalproductions["Production"].tolist()

    country_colors = px.colors.qualitative.Safe[:len(uniquecountry)] 
    location_colors = px.colors.qualitative.Pastel[:len(uniquelocations)]  
    detail_colors = px.colors.qualitative.Set1[:len(uniquedetails)]
    species_colors = px.colors.qualitative.Dark2[:len(uniquespecies)]
    node_colors = country_colors + location_colors + detail_colors + species_colors
    link_opacity = [0.4 + (v / max(values)) * 0.6 for v in values] 
    fig = go.Figure(
        go.Sankey(node=dict(
            pad=20,
            thickness=15,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color=[f"rgba(31, 119, 180, {op})" for op in link_opacity] # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title = "Countries-Locations-Methods-Species Total Productions Using Sankey Chart",
        title_font=dict(color="black"), 
        template="plotly_white",  
        font=dict(size=14, family="Arial")
    )
    return fig





def plot_justcountryprod(df,years,countries):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    df = df[df["Country"].isin(countries)]

    df = df.groupby(["Country"])[years].sum().reset_index()
    df_melted =  pd.melt(df,id_vars="Country",value_vars=years,value_name="Production",var_name="Years")
    fig = px.area(df_melted,x = "Years",y="Production",color="Country",title="Total Productions Distributions By Countries Over Years")
    """ fig.update_layout(
        width = 500 + len(countries)*50,
        height = 500 + len(countries)*50
    ) """
    return fig


def plot_justcountr_methodprod(df,years,countries,methods):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Country","Detail"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Detail"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Country",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Detail",facet_row_spacing=0.1,facet_col_spacing=0.05,title="Production Method Effect On Countries In Years",facet_col_wrap=3)
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        for i, method in enumerate(methods):
            figure.layout.annotations[i].update(text=method)
        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Detail",color_discrete_sequence=px.colors.sequential.RdBu,title=f"Production Method Effect On {countries[0]} Over Years")
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        return figure



def plot_countryspeciesprod_by_time2(df,countries,species,years):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Country","Species"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Country",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Species",facet_row_spacing=0.1,facet_col_spacing=0.05,title="Species Production Distribution Of Countries In Years",facet_col_wrap=3)
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        for i, specy in enumerate(species):
            figure.layout.annotations[i].update(text=specy)
        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Species",color_discrete_sequence=px.colors.sequential.RdBu,title=f"Species Production Distribution Of {countries[0]} Over Years")
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        return figure


def plot_countrymethod_specyprod(df,years,countries,methods,species):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Country","Species","Detail"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species","Detail"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Country",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Detail",facet_row="Species",facet_row_spacing=0.4,facet_col_spacing=0.09,title="Production Distribution Of Countries Filtered By Species and Methods Over Years")
        figure.update_layout(
            width = 600 + len(methods) * 50,
            height = 300 +len(species) * 100,
            plot_bgcolor='#F0F2F6',
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
        for i, annotation in enumerate(figure.layout.annotations):
            if "Detail=" in annotation.text:
                # "Location=" kısmını kaldır ve sadece lokasyon adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 20

            elif "Species=" in annotation.text:
                # "Detail=" kısmını kaldır ve sadece method adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 15
            

        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Species",facet_col="Detail",facet_col_spacing=0.2,color_discrete_sequence=px.colors.sequential.RdBu,title=f"Species Production Distribution Of {countries[0]} Over Years")
        figure.update_layout(
            width = 600 + len(methods) * 50,
            plot_bgcolor='#F0F2F6',
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
        for i, detail in enumerate(methods):
            figure.layout.annotations[i].update(text=detail)
        figure.update_yaxes(matches=None, showticklabels=True)    
        return figure
    

def plot_justcountr_locatprod(df,years,countries,locations):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]

    df = df.groupby(["Country","Location"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Location"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Country",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Location",facet_row_spacing=0.2,facet_col_spacing=0.1,title="Production Method Effect On Countries In Years",facet_col_wrap=3)
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        for i, location in enumerate(locations):
            figure.layout.annotations[i].update(text=location)
        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Location",color_discrete_sequence=px.colors.sequential.RdBu,title=f"{countries[0]}'s Production Distributions By Locations Over Years")
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        return figure


def plot_countrylocat_specyprod(df,years,countries,locations,species):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]
    df = df[df["Location"].isin(locations)]

    df = df.groupby(["Country","Species","Location"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species","Location"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Country",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Location",facet_row="Species",facet_row_spacing=0.4,facet_col_spacing=0.09,title="Production Distribution Of Countries Filtered By Species and Locations Over Years")
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        for i, annotation in enumerate(figure.layout.annotations):
            if "Location=" in annotation.text:
                # "Location=" kısmını kaldır ve sadece lokasyon adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 20

            elif "Species=" in annotation.text:
                # "Detail=" kısmını kaldır ve sadece method adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 15
            # Başlık font boyutunu küçült


        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Species",facet_col="Location",facet_col_spacing=0.2,color_discrete_sequence=px.colors.sequential.RdBu,title=f"Species Production Distribution Of {countries[0]} In Locations Over Years")
        figure.update_layout(
            width = 600 + len(locations) * 50,
            plot_bgcolor='#F0F2F6',
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
        for i, location in enumerate(locations):
            figure.layout.annotations[i].update(text=location)
        figure.update_yaxes(showticklabels=True)    
        return figure
    

def plot_countrymethod_locyprod(df, years, countries, locations, methods):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]

    # Veriyi filtrele ve grupla
    df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Country", "Location", "Detail"])[listyears].sum().reset_index()
    df_melted = pd.melt(df, id_vars=["Country", "Location", "Detail"], value_vars=listyears, value_name="Production", var_name="Years")

    if len(countries) > 1:
        # Grafik oluştur
        figure = px.area(
            df_melted,
            x="Years",
            y="Production",
            color="Country",
            color_discrete_sequence=px.colors.sequential.RdBu,
            facet_col="Detail",
            facet_row="Location",
            facet_row_spacing=0.3,  
            facet_col_spacing=0.09,
            title="Production Distribution Of Countries Filtered By Locations and Methods Over Years"
        )

        # Grafik düzenlemeleri
        figure.update_layout(
            width = 1000,
            height = 600 + len(locations) * 50,
            plot_bgcolor='#F0F2F6',
            font=dict(size=16),
            xaxis=dict(
                gridcolor="white",
                gridwidth=1,
                title_font=dict(size=18),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                gridwidth=1,
                title_font=dict(size=18),
                tickfont=dict(size=14)
            ),
            legend=dict(
                title=dict(font=dict(size=16)),
                font=dict(size=14),
                itemclick="toggleothers",
                itemsizing="constant",
                traceorder="normal",
            )
        )

        # Başlıkları özelleştir
        for i, annotation in enumerate(figure.layout.annotations):
            if "Location=" in annotation.text:
                # "Location=" kısmını kaldır ve sadece lokasyon adını al
                annotation.text = annotation.text.split("=")[1].strip()
            elif "Detail=" in annotation.text:
                # "Detail=" kısmını kaldır ve sadece method adını al
                annotation.text = annotation.text.split("=")[1].strip()
            # Başlık font boyutunu küçült
            annotation.font.size = 20  # Font boyutunu ayarla

        # Eksen başlıklarını güncelle
        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15), title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(color='black', size=15), title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)

        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Location",facet_col="Detail",facet_col_spacing=0.2,color_discrete_sequence=px.colors.sequential.RdBu,title=f"{countries[0]}'s Production Distributions Using Methods In Locations Over Years")
        figure.update_layout(
            width = 600 + len(methods) * 50,
            plot_bgcolor='#F0F2F6',
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
        for i, detail in enumerate(methods):
            figure.layout.annotations[i].update(text=detail)
        figure.update_yaxes(showticklabels=True)    
        return figure
    

def plot_countrylocat_specymethodprod(df,years,countries,locations,species,methods):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]


    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Country","Species","Location","Detail"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species","Location","Detail"],value_vars=listyears,value_name="Production",var_name="Years")
    if len(countries) > 1:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Species",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Detail",facet_row="Location",facet_row_spacing=0.4,facet_col_spacing=0.09,title="Production Distribution Of Species Filtered By Countries,Methods and Locations Over Years")
        figure.update_layout(
            plot_bgcolor='#F0F2F6',
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
        for i, annotation in enumerate(figure.layout.annotations):
            if "Location=" in annotation.text:
                # "Location=" kısmını kaldır ve sadece lokasyon adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 14

            elif "Detail=" in annotation.text:
                # "Detail=" kısmını kaldır ve sadece method adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 20
            # Başlık font boyutunu küçült
        figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
        figure.update_yaxes(showticklabels=True)
        return figure
    else:
        figure = px.area(df_melted,x = "Years",y = "Production", color="Species",facet_col="Detail",facet_row="Location",facet_col_spacing=0.2,facet_row_spacing=0.2,color_discrete_sequence=px.colors.sequential.RdBu,title=f"Species Production Distribution Of {countries[0]} Filtered By Locations And Methods Over Years")
        figure.update_layout(
            width = 600 + len(locations) * 50,
            plot_bgcolor='#F0F2F6',
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
            title=dict(font=dict(size=20)),  # Legend başlığı yazı boyutu
            font=dict(size=14),              # Legend öğelerinin yazı boyutu
            itemclick="toggleothers",        # Legend öğelerinin tıklama davranışı
            itemsizing="constant",           # Legend simge boyutunu sabit tutar
            traceorder="normal",             # Legend sıralama düzeni
            )
        )
        for i, annotation in enumerate(figure.layout.annotations):
            if "Location=" in annotation.text:
                # "Location=" kısmını kaldır ve sadece lokasyon adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 14

            elif "Detail=" in annotation.text:
                # "Detail=" kısmını kaldır ve sadece method adını al
                annotation.text = annotation.text.split("=")[1].strip()
                annotation.font.size = 20
        figure.update_yaxes(showticklabels=True)    
        return figure    