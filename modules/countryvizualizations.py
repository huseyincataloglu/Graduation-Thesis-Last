import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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
        columns = len(countries)

        if locations:
            df = df[df["Location"].isin(locations)]
    
        grouped = df.groupby("Country")[years].sum().reset_index()
        melted = pd.melt(grouped,id_vars=["Country"],value_vars=years,var_name="Years",value_name="Production")
        fig = make_subplots(rows = 1,cols=columns)
        i = 1
        for country in countries:
            melted1 = melted[melted["Country"] == country]
            fig.add_trace(go.Box(x = melted1["Country"],y = melted1["Production"],name=country),row = 1,col=i)
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

    if len(years) == 0:
        # Eğer yıl verilmemişse boş bir grafik oluştur
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

    if len(countries) == 1:
        # Eğer tek bir ülke varsa, yıllar sütun olarak gösterilir
        country = countries[0]
        filtered = df[df["Country"] == country]
        
        fig = make_subplots(rows=1, cols=len(years), subplot_titles=years)

        for i, year in enumerate(years, start=1):
            year_data = filtered[year]
            fig.add_trace(
                go.Box(
                    x=[year] * len(year_data),
                    y=year_data,
                    name=year
                ),
                row=1, col=i
            )

        fig.update_layout(
            title=f"Production Distribution for {country} by Year",
            height=400,
            width=300 * len(years),
            showlegend=False
        )
        return fig

    if len(countries) > 1 and  len(years) == 1:
        # Eğer tek bir yıl varsa, ülkeler sütun olarak gösterilir
        year = years[0]
        columns = len(countries)

        grouped = df.loc[:, ["Country", year]]
        fig = make_subplots(rows=1, cols=columns)

        for i, country in enumerate(countries, start=1):
            filtereddata = grouped[grouped["Country"] == country]
            fig.add_trace(
                go.Scatter(
                    x=[country] * len(filtereddata),
                    y=filtereddata[year],
                    mode="markers",
                    name=country,
                    marker=dict(size=10)
                ),
                row=1, col=i
            )

        fig.update_layout(
            title=f"Data Distribution for {year}",
            xaxis_title="Countries",
            yaxis_title="Production",
            height=400,
            width=300 * len(countries),
        )
        return fig

    elif len(years) > 1:
        # Eğer birden fazla ülke ve yıl varsa, hem ülke hem yıl eksenleri için alt grafikler oluşturulur
        fig = make_subplots(
            rows=len(years),
            cols=len(countries),
            subplot_titles=[f"{year} - {country}" for year in years for country in countries]
        )

        for l, year in enumerate(years, start=1):
            for c, country in enumerate(countries, start=1):
                filtered = df[df["Country"] == country]
                fig.add_trace(
                    go.Scatter(
                        x=[year] * len(filtered),
                        y=filtered[year],
                        mode="markers",
                        name=f"{year} - {country}",
                        marker=dict(size=10)
                    ),
                    row=l, col=c
                )

        fig.update_layout(
            title="Production Distribution by Year and Country",
            height=300 * len(years),
            width=300 * len(countries),
            showlegend=False
        )
        return fig





def plot_participation_by_country(df, countries, years,locations = None,methods = None):
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
        if locations:
            df = df[df["Location"].isin(locations)]
        if methods:
            df = df[df["Detail"].isin(methods)]    
        df_filtered = df[df["Country"].isin(countries)]
        
        participation_count = df_filtered['Country'].value_counts().reset_index()
        participation_count.columns = ['Country', 'Participation Count']
        
       
        fig = px.bar(participation_count, x='Country', y='Participation Count', color='Country', 
                    title="Production Participation Count by Country", 
                    labels={'Participation Count': 'Number of Participation'},
                    color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
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


def plot_partvsprod_by_country(df, countries, years,locations = None,methods = None):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if locations:
            df = df[df["Location"].isin(locations)]
    if methods:
        df = df[df["Detail"].isin(methods)]
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





        




def plot_countries_prod_map(df,countries,years,locations,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    title = "Total Productions By Countries Map"
    if methods:
        df = df[df["Detail"].isin(methods)]
    if len(locations) > 0 :
        countryproductions = df.groupby(["Country","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production")
        filteredcountryproductions = countryproductions[countryproductions.Location.isin(locations)]
        filteredcountryproductions = filteredcountryproductions[filteredcountryproductions.Country.isin(countries)]
        if len(locations) > 1:
            grouped_filteredcountryproductions = filteredcountryproductions.groupby("Country")["Production"].sum().reset_index()
        else:
            grouped_filteredcountryproductions = filteredcountryproductions    
        figure = px.choropleth(grouped_filteredcountryproductions,locations="Country",locationmode="country names",color="Production",title=title)
        figure.update_layout(
            font=dict(size=16),  # Yazı boyutu
            coloraxis_colorbar=dict(
                title="Production",        # Renk skalası başlığı
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
            )
        )
        return figure
    else:
        countryproductions = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
        filteredcountryproductions = countryproductions[countryproductions.Country.isin(countries)]
        figure = px.choropleth(filteredcountryproductions,locations="Country",locationmode="country names",color="Production",title=title)
        figure.update_layout(
            font=dict(size=16),  # Yazı boyutu
            coloraxis_colorbar=dict(
                title="Production",        # Renk skalası başlığı
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
                )
            )
        return figure



def plot_countries_by_production(df,countries,years,locations,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if len(locations) > 0:
        countryproductions = df.groupby(["Country","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production")
        filteredcountryproductions = countryproductions[countryproductions.Location.isin(locations)]
        filteredcountryproductions = filteredcountryproductions[filteredcountryproductions.Country.isin(countries)]
        if len(locations) > 1:
            grouped_filteredcountryproductions = filteredcountryproductions.groupby("Country")["Production"].sum().reset_index()
        else:
            grouped_filteredcountryproductions = filteredcountryproductions
        figure = px.bar(grouped_filteredcountryproductions,x = "Country",y = "Production",color="Production",color_continuous_scale=px.colors.sequential.RdBu_r)
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
    else:
        countryproductions = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
        filteredcountryproductions = countryproductions[countryproductions.Country.isin(countries)]
        figure = px.bar(filteredcountryproductions,x="Country",y="Production",color="Production",color_continuous_scale=px.colors.sequential.RdBu_r)
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


    
def plot_countryprod_by_time(df,countries,years,locations,methods = None):
    start, end = years
    years1 = [str(year) for year in range(start,end+1,+1)]

    if methods:
        df= df[df["Detail"].isin(methods)]
    title = "Countries Production Distribution In Years"
    if len(locations) > 0 :
        countryproductions = df.groupby(["Country","Location"])[years1].sum().reset_index()
        filteredcountryproductions = countryproductions[countryproductions.Location.isin(locations)]
        filteredcountryproductions = filteredcountryproductions[filteredcountryproductions.Country.isin(countries)]
        if len(locations) > 1:
            grouped_filteredcountryproductions = filteredcountryproductions.groupby("Country")[years1].sum().reset_index() 
            melted = pd.melt(grouped_filteredcountryproductions,id_vars=["Country"],value_vars=years1)
            melted = melted[melted["Country"].isin(countries)]
            melted.rename({"variable" : "Years", "value" : "Production"},axis = 1,inplace=True)
            figure = px.area(melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.sequential.RdBu,title=title)
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
        else:
            grouped_filteredcountryproductions = filteredcountryproductions
        grouped_filteredcountryproductions = pd.melt(grouped_filteredcountryproductions,id_vars=["Country","Location"],value_vars= years1,var_name="Years",value_name="Production")
        figure = px.area(grouped_filteredcountryproductions,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.sequential.RdBu,title=title)
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
    new = df.groupby("Country")[years1].sum().reset_index()
    new = new[new["Country"].isin(countries)]
    df_melted = pd.melt(new,id_vars="Country",value_vars=years1,var_name="Years",value_name="Production")
    figure = px.area(df_melted,x = "Years",y = "Production",color="Country",color_discrete_sequence=px.colors.sequential.RdBu,title = title)
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



def plot_countrieswithspecies(df,countries,species,years,locations = None,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]

    if locations:
        df = df[df["Location"].isin(locations)]        
    if methods:
        df = df[df["Detail"].isin(methods)]
    
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

    fig = go.Figure(
        go.Sankey(node=dict(
            pad=15,
            thickness=20,
            label=all_nodes,
            color=node_colors  # Her düğüme farklı renk atandı
        ),
        link=dict(
            source=sources,
            target=target,
            value=values,
            color="rgba(100, 100, 250, 0.3)"  # Bağlantıları saydam hale getirdik
        ))
    )
    fig.update_layout(
        title = "Countries Species Production Using Sankey Chart"
    )
    return fig


    


def plot_countryspeciesprod_by_time(df,countries,species,years,locations = None,methods = None):
    start,end = years
    listyears = [str(year) for year in range(start,end+1,1)]

    if locations:
        df = df[df["Location"].isin(locations)]
    if methods:
        df = df[df["Detail"].isin(methods)]

    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Country","Species"])[listyears].sum().reset_index()
    df_melted =  pd.melt(df,id_vars=["Country","Species"],value_vars=listyears,value_name="Production",var_name="Years")
    figure = px.scatter(df_melted,x = "Years",y = "Production", color="Species",symbol="Country",size="Production",color_discrete_sequence=px.colors.sequential.RdBu,facet_col="Species",facet_row="Country",facet_row_spacing=0.1,facet_col_spacing=0.05,title="Species Production Distribution Of Countries In Years")
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
    figure.for_each_annotation(lambda annotation: annotation.update(text=""))
    figure.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    figure.for_each_xaxis(lambda yaxis: yaxis.update(tickfont=dict(color='black', size=15),title_font=dict(color='red', size=18)))
    figure.update_yaxes(matches=None, showticklabels=True)
    return figure



def plot_country_productiondetail(df,countries,years,locations = None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if locations:
        df = df[df["Location"].isin(locations)]
    df = df.groupby(["Country","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    df = df[df["Country"].isin(countries)]
    figure = px.bar(df,x="Country",y = "Production",color="Detail",barmode="group",color_discrete_sequence=px.colors.sequential.RdBu,title="Production Methods Of Countries By Total Amount")
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


