import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



def plot_proddist_boxplotlocations(df,locations,years):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if len(locations) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No location selected. Please select at least one specy.",
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
        )
        return fig
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby("Location")[years].sum().reset_index()
        melted = pd.melt(
            grouped,
            id_vars=["Location"],
            value_vars=years,
            var_name="Years",
            value_name="Production"
        )
        melted["Years"] = pd.to_numeric(melted["Years"], errors='coerce')  # Sayısal forma çevir
        melted = melted.sort_values(by="Years")

        fig = go.Figure(data=go.Heatmap(
            z=melted["Production"],
            x=melted["Years"],  
            y=melted["Location"],
            colorscale='Viridis'
        ))

        fig.update_layout(
            xaxis=dict(
                title='Years',
                #titlefont=dict(color='red'),  # X ekseni başlık rengi
                tickfont=dict(color='black')  # X ekseni işaretleme yazı rengi
            ),
            yaxis=dict(
                title='Locations',
                #titlefont=dict(color='red'),  # Y ekseni başlık rengi
                tickfont=dict(color='black')  # Y ekseni işaretleme yazı rengi
            ),
            height=600,
            width=800
        )
        #i = 1
        #for specy in species:
        #melted1 = melted[melted["Species"] == specy]
        #    fig.add_trace(go.Box(x = melted1["Species"],y = melted1["Production"],name=specy),row = 1,col=i)
        #    i += 1
        #fig.update_layout(
        #    title="Box Plot of Annual Production Distribution by Species",
        #    showlegend=False,
        #    height=400,
        #    width=300 * len(species), 
        #)
        
        return fig
 

def plot_partvsprod_by_locations(df, locations, years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if len(locations) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No location selected. Please select at least one location.",
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
        df = df[df["Location"].isin(locations)]
        df1 = df.groupby("Location")[years].sum().sum(axis = 1).reset_index(name = "Production")
        participation_count = df['Location'].value_counts().reset_index()
        participation_count.columns = ['Location', 'Participation Count']
        df1 = df1.merge(participation_count,on = "Location",how = "left")

        figure = px.scatter(df1, x = "Participation Count", y = "Production",color = "Location",title= "Total Participation vs Total Production Amount",size="Production",symbol="Location")
        figure.update_layout(
            font=dict(size=16),  # Yazı boyutu
            title=dict(font=dict(size=14, color="black")),
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


def plot_locationmethpd_paralelcat(df,locations,years):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]

    if len(locations) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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
    if len(locations) > 0:
        df= df[df["Location"].isin(locations)]
        methodgrouped = df.groupby(["Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production")
        methodpart = df.loc[:,["Location","Detail"]]
        methodpart = methodpart.merge(methodgrouped,on = ["Location","Detail"],how= "left")
        fig = px.parallel_categories(methodpart,dimensions=["Location","Detail"],color="Production",color_continuous_scale="RdBu",title="Locations And Methods Frequencies Colored By Total Production")
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),
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



def plot_locationn_grapyearly(df,locations,years1):

    df = df[df["Location"].isin(locations)]    

    if len(years1) == 0 or len(locations) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No years or locations selected. Please select at least one year or location.",
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
        df = df[df["Location"].isin(locations)]
        melted= pd.melt(df,id_vars="Location",value_vars=years1,value_name="Production",var_name="Years")
        figure = px.histogram(melted,x = "Production",color="Location",marginal="box",hover_data=melted.columns,title="Annual Production Distribution by Locations")
        figure.update_layout(
            title=dict(font=dict(size=14, color="black")),

        )
        return figure

        


def plot_distline_locat(df, locations, years):
    start, end = years
    years = [str(year) for year in range(start, end+1)]  # Yılları stringe dönüştür

    if len(locations) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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

    df = df[df["Location"].isin(locations)]
    # Verileri gruplama ve dönüştürme
    grouped = df.groupby("Location")[years].sum().reset_index()
    melted = pd.melt(grouped, id_vars="Location", value_vars=years, value_name="Production", var_name="Years")

    # Tek bir lokasyon seçildiyse büyük grafik kullan
    if len(locations) == 1:
        fig = go.Figure()
        location = locations[0]
        melted1 = melted[melted["Location"] == location]
        fig.add_trace(go.Scatter(x=melted1["Years"], y=melted1["Production"], mode="lines+markers", name=location))

        fig.update_layout(
            title=f"Production Over Years for {location}",
             # Tek lokasyon için geniş grafik
            showlegend=True
        )

    else:
        # Alt grafik düzeni için satır ve sütun sayısını ayarlama
        fig = go.Figure()
        for location in locations:
            melted1 = melted[melted["Location"] == location]
            trace = go.Scatter(x=melted1["Years"], y=melted1["Production"], mode="lines+markers", name=location)
            fig.add_trace(trace)

        fig.update_layout(
            title="Production Over Years by Locations",
            showlegend=True
        )

    fig.update_xaxes(title="Year", tickfont=dict(size=12, color='black'))
    fig.update_yaxes(title="Production", tickfont=dict(size=12, color='black'))

    fig.update_layout(title_font=dict(size=14, color='black'))

    return fig



def plot_region_species_scatter_line(df, locations, years, species):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Location","Species"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Species"], value_vars=listyears, 
                        value_name="Production", var_name="Years")

    # Yılları numerik hale getir ve sırala
    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Species", "Years"])
    if len(locations) > 1:
        # Scatter + Line grafiği oluştur
        fig = px.line(df_melted,x = "Years",y = "Production",color="Species",line_dash="Species",facet_col="Location",facet_col_spacing=0.1,facet_col_wrap=4,color_discrete_sequence=px.colors.qualitative.Set1)

        # Grafik düzenlemeleri
        fig.update_layout(
            title="Production by Locations and Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            legend=dict(title_font=dict(size=16), font=dict(size=14))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Species",line_dash="Species",color_discrete_sequence=px.colors.qualitative.Set1)

        # Grafik düzenlemeleri
        fig.update_layout(
            title="Production by Locations and Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            legend=dict(title_font=dict(size=16), font=dict(size=14))
        )

        return fig


def plot_region_methods_scatter_line(df, locations, years, methods):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Location","Detail"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Detail"], value_vars=listyears, 
                        value_name="Production", var_name="Years")

    # Yılları numerik hale getir ve sırala
    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Detail", "Years"])
    if len(locations) > 1:
        # Scatter + Line grafiği oluştur
        fig = px.line(df_melted,x = "Years",y = "Production",color="Detail",line_dash="Detail",facet_col="Location",facet_col_wrap=4,facet_col_spacing=0.1,color_discrete_sequence=px.colors.qualitative.Set1)

        # Grafik düzenlemeleri
        fig.update_layout(
            title="Production by Locations and Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=20), font=dict(size=20))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Detail",line_dash="Detail",color_discrete_sequence=px.colors.qualitative.Antique)

        # Grafik düzenlemeleri
        fig.update_layout(
            title="Production by Locations and Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=20), font=dict(size=20))
        )

        return fig


def plot_region_methodsspecies_scatter_line(df, locations, years, methods,species):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Location","Detail","Species"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Detail","Species"], value_vars=listyears, 
                        value_name="Production", var_name="Years")


    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Detail","Species", "Years"])
    if len(locations) > 1:

        fig = px.line(
            df_melted,
            x="Years",
            y="Production",
            color="Location",        
            line_dash="Species",       
            title="Production by Locations, Methods, and Species Over Years",
            facet_col= "Detail",
            facet_col_spacing= 0.1,
            facet_col_wrap=2,
            color_discrete_sequence=px.colors.qualitative.Antique
        )

   
        fig.update_layout(
            title="Production by Locations and Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Detail",line_dash="Species",color_discrete_sequence=px.colors.qualitative.Antique)

        # Grafik düzenlemeleri
        fig.update_layout(
            title="Production by Locations and Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig



def plot_locat_country_line(df, locations, years,countries):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]

    # 📌 Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    # 📌 Ülke isimlerinden ISO Alpha-3 kodlarını ekle
    df = df.groupby(["Location","Country"])[listyears].sum().reset_index()

    df_melted = pd.melt(df, id_vars=["Location","Country"], value_vars=listyears, 
                        value_name="Production", var_name="Years")

    df_melted["Years"] = pd.to_numeric(df_melted["Years"])

    if len(locations) > 1:
        fig = px.line(df_melted,x = "Years",y = "Production",color = "Country",line_dash="Country",facet_col="Location",facet_col_wrap=4,facet_col_spacing=0.1,title = "Production Distributions By Locations And Countries",color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
                xaxis_title="Years",
                yaxis_title="Production",
                font=dict(size=16),
                xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
                yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
                legend=dict(title_font=dict(size=18), font=dict(size=18))
            )
        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color = "Country",line_dash="Country",title = "Production Distributions By Location And Countries",color_discrete_sequence=px.colors.qualitative.Antique)
        fig.update_layout(
                xaxis_title="Years",
                yaxis_title="Production",
                font=dict(size=16),
                xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
                yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
                legend=dict(title_font=dict(size=18), font=dict(size=18))
            )
        return fig

def plot_region_countriesspecies_scatter_line(df, locations, years, countries,species):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Location","Country","Species"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Country","Species"], value_vars=listyears, 
                        value_name="Production", var_name="Years")


    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Country","Species", "Years"])
    if len(locations) > 1:

        fig = px.line(
            df_melted,
            x="Years",
            y="Production",
            color="Country",        
            line_dash="Species",       
            title="Production by Locations, Methods, and Species Over Years",
            facet_col= "Location",
            facet_col_spacing= 0.1,
            facet_col_wrap=2,
            color_discrete_sequence=px.colors.qualitative.Set1
        )

   
        fig.update_layout(
            title="Production by Locations ,Countries,Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Country",line_dash="Species",color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            title="Production by Locations,Countries,Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig



def plot_region_countriesmethod_scatter_line(df, locations, years, countries,methods):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]

    df = df.groupby(["Location","Country","Detail"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Country","Detail"], value_vars=listyears, 
                        value_name="Production", var_name="Years")


    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Country","Detail", "Years"])
    if len(locations) > 1:

        fig = px.line(
            df_melted,
            x="Years",
            y="Production",
            color="Country",        
            line_dash="Detail",       
            title="Production by Locations, Methods, and Species Over Years",
            facet_col= "Location",
            facet_col_spacing= 0.1,
            facet_col_wrap=2,
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        fig.update_layout(
            title="Production by Locations ,Countries,Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Country",line_dash="Detail",color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            title="Production by Location,Countries,Methods Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig



def plot_region_countriesmethod_speciesscatter_line(df, locations, years, countries,methods,species):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Location","Country","Detail","Species"])[listyears].sum().reset_index()
    # Veriyi uzun formata dönüştür
    df_melted = pd.melt(df, id_vars=["Location", "Country","Detail","Species"], value_vars=listyears, 
                        value_name="Production", var_name="Years")


    df_melted["Years"] = pd.to_numeric(df_melted["Years"])
    df_melted = df_melted.sort_values(by=["Location", "Country","Detail", "Years","Species"])
    if len(locations) > 1:

        fig = px.line(
            df_melted,
            x="Years",
            y="Production",
            color="Country",        
            line_dash="Species",       
            title="Production by Locations,Countries, Methods And Species Over Years",
            facet_col= "Location",
            facet_row="Detail",
            facet_col_spacing= 0.1,
            facet_row_spacing= 0.1,
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        fig.update_layout(
            title="Production by Locations ,Countries,Methods And Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig
    else:
        fig = px.line(df_melted,x = "Years",y = "Production",color="Country",line_dash="Species",facet_col="Detail",facet_col_spacing=0.1,color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            title="Production by Location,Countries,Methods And Species Over Years",
            xaxis_title="Years",
            yaxis_title="Production",
            font=dict(size=16),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=17)),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig




def plot_specygrouped_bar(df,locations,years,species):
    start, end = years
    years = [str(year) for year in range(start, end+1)] 
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        df = df[df["Species"].isin(species)]
        grouped = df.groupby(["Location","Species"])[years].sum().sum(axis = 1).reset_index(name ="Production")
        fig = px.bar(grouped,x = "Location",y = "Production",color="Species",title="Total Productions By Species And  Grouped Locations",barmode="group")
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),  
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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



def plot_groupedbarloc(df,locations,years):
    start, end = years
    years = [str(year) for year in range(start, end+1)]  
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby("Location")[years].sum().sum(axis = 1).reset_index(name ="Production")
        fig = px.bar(grouped,x = "Location",y = "Production",color="Location",title="Total Productions By Locations")
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),  
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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


def plot_groupedbarlocandmethod(df,locations,years,methods):
    start, end = years
    years = [str(year) for year in range(start, end+1)] 
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        df = df[df["Detail"].isin(methods)]
        grouped = df.groupby(["Location","Detail"])[years].sum().sum(axis = 1).reset_index(name ="Production")

        fig = px.bar(grouped,
            x = "Location",
            y = "Production",
            color="Detail",
            title="Total Productions By Methods And Grouped Locations",
            barmode="group")
        
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),  
            height=600,
            width=700,
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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

def plot_locmethod_specy(df,locations,years,methods,species):
    start, end = years
    years = [str(year) for year in range(start, end+1)]  # Yılları stringe dönüştür

    if len(locations) > 0:
        # Filtreleme
        df = df[df["Location"].isin(locations)]
        df = df[df["Detail"].isin(methods)]
        df = df[df["Species"].isin(species)]
        
        # Grup bazlı toplama
        grouped = df.groupby(["Location", "Detail", "Species"])[years].sum().sum(axis=1).reset_index(name="Production")

        # Alt grafiklerin satır ve sütun düzeni
        fig = px.bar(grouped,x = "Location",y = "Production",color="Species",facet_col="Detail",facet_col_spacing=0.1)

        
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),
            title_text="Total Productions by Species, Methods And Locations",
        )

        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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


def plot_countrygrouped_bar(df,locations,years,countries):
    start, end = years
    years = [str(year) for year in range(start, end+1)] 
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        df = df[df["Country"].isin(countries)]
        grouped = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name ="Production")
        fig = px.bar(grouped,x = "Location",y = "Production",color="Country",barmode="stack",title="Total Productions By Countries And  Grouped Locations")
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),  
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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



        
def plot_loccountry_specy(df,locations,years,countries,species):
    start, end = years
    years = [str(year) for year in range(start, end+1)]  # Yılları stringe dönüştür

    if len(locations) > 0:
        # Filtreleme
        df = df[df["Location"].isin(locations)]
        df = df[df["Country"].isin(countries)]
        df = df[df["Species"].isin(species)]
        
        # Grup bazlı toplama
        grouped = df.groupby(["Location", "Country", "Species"])[years].sum().sum(axis=1).reset_index(name="Production")

        # Alt grafiklerin satır ve sütun düzeni
        fig = px.bar(grouped,x = "Country",y = "Production",color="Species",facet_col="Location",facet_col_spacing=0.1)

        
        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),
            title_text="Total Productions by Species, Countries And Locations",
        )

        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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


def plot_loccountry_method(df,locations,years,countries,methods):
    start, end = years
    years = [str(year) for year in range(start, end+1)]  

    if len(locations) > 0:

        df = df[df["Location"].isin(locations)]
        df = df[df["Country"].isin(countries)]
        df = df[df["Detail"].isin(methods)]
        
        
        grouped = df.groupby(["Location", "Country", "Detail"])[years].sum().sum(axis=1).reset_index(name="Production")

       
        fig = px.bar(grouped,x = "Location",y = "Production",color="Country",facet_col="Detail",facet_col_spacing=0.1)

        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),
            title_text="Total Productions By Methods, Countries And Locations",
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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
    

def plot_locat_countriesmethod_specy_bar(df, locations, years, countries,methods,species):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1)]
    # Veriyi filtrele
    df = df[df["Location"].isin(locations)]
    df = df[df["Country"].isin(countries)]
    df = df[df["Detail"].isin(methods)]
    df = df[df["Species"].isin(species)]

    df = df.groupby(["Location","Country","Detail","Species"])[listyears].sum().sum(axis = 1).reset_index(name  ="Production")
    # Veriyi uzun formata dönüştür
   

    if len(locations) > 0:
        fig = px.bar(
            df,
            x="Country",
            y="Production",
            color="Species",        
            title="Total Production By Locations,Countries, Methods And Species s",
            facet_col= "Location",
            facet_row="Detail",
            facet_col_spacing= 0.1,
            facet_row_spacing= 0.1,
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        fig.update_layout(
            title=dict(font=dict(size=14, color="black")),
            legend=dict(title_font=dict(size=18), font=dict(size=18))
        )

        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No locations selected. Please select at least one location.",
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
    