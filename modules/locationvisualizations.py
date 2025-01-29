import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_proddist_boxplotlocations(df,locations,years,countries = None,methods = None,species = None):
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
            height=400,
            width=600,
        )
        return fig
    if len(locations) > 0:
        if methods:
            df = df[df["Detail"].isin(methods)]

        df = df[df["Location"].isin(locations)]

        if countries:
            df = df[df["Country"].isin(countries)]
        if species:
            df = df[df["Species"].isin(species)]

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
            title=dict(text='Production Distribution by Location and Year',font=dict(size=24, color="red")),
            xaxis=dict(
                title='Years',
                titlefont=dict(color='red'),  # X ekseni başlık rengi
                tickfont=dict(color='black')  # X ekseni işaretleme yazı rengi
            ),
            yaxis=dict(
                title='Locations',
                titlefont=dict(color='red'),  # Y ekseni başlık rengi
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


def plot_participation_by_locations(df, locations, years,countries = None,methods = None,species= None):
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
    if len(locations) > 0:
        if countries:
            df = df[df["Country"].isin(countries)]
        if methods:
            df = df[df["Detail"].isin(methods)]

        if species:
            df = df[df["Species"].isin(species)]        
        df_filtered = df[df["Location"].isin(locations)]

        
        participation_count = df_filtered['Location'].value_counts().reset_index()
        participation_count.columns = ['Location', 'Participation Count']
        
       
        fig = px.scatter(participation_count, x='Location', y='Participation Count', color='Location',
                    symbol= "Location",
                    size = 'Participation Count',
                    title="Production Participation Count by Locations", 
                    labels={'Participation Count': 'Number of Participation'},
                    color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(
            font=dict(size=16),  # Yazı boyutu
            title=dict(font=dict(size=24, color="red")),
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

def plot_partvsprod_by_locations(df, locations, years,countries = None,methods = None,species = None):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if species:
        df = df[df["Species"].isin(species)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if countries:
        df = df[df["Country"].isin(countries)]
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
            title=dict(font=dict(size=24, color="red")),
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


def plot_locationn_grapyearly(df,locations,years1,species=None,countries=None,methods = None):

    if species:
        df = df[df["Species"].isin(species)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if countries:
        df = df[df["Country"].isin(countries)]
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
        if species:
            df = df[df["Species"].isin(species)]
        if methods:
            df = df[df["Detail"].isin(methods)]
        if countries:
            df = df[df["Country"].isin(countries)]
        df = df[df["Location"].isin(locations)]
        melted= pd.melt(df,id_vars="Location",value_vars=years1,value_name="Production",var_name="Years")
        figure = px.histogram(melted,x = "Production",color="Location",marginal="box",hover_data=melted.columns,title="Annual Production Distribution by Locations")
        figure.update_layout(
            title=dict(font=dict(size=24, color="red")),

        )
        return figure

        


def plot_distline_locat(df, locations, years, countries=None, methods=None, species=None):
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
    if species:
        df = df[df["Species"].isin(species)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if countries:
        df = df[df["Country"].isin(countries)]
    df = df[df["Location"].isin(locations)]

    # Verileri gruplama ve dönüştürme
    grouped = df.groupby("Location")[years].sum().reset_index()
    melted = pd.melt(grouped, id_vars="Location", value_vars=years, value_name="Production", var_name="Years")
    
    # Alt grafik düzeni için satır ve sütun sayısını ayarlama
    num_plots = len(locations)
    cols = 2
    rows = (num_plots + 1) // cols
    if num_plots % cols != 0:
        rows += 1

    # Subplotları oluşturma
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=locations)

    # Her bir lokasyon için çizgi grafiği ekleme
    for i, location in enumerate(locations):
        row = i // cols + 1
        col = i % cols + 1
        melted1 = melted[melted["Location"] == location]
        trace = go.Scatter(x=melted1["Years"], y=melted1["Production"], mode="lines+markers", name=location)
        fig.add_trace(trace, row=row, col=col)

    # Genel düzenlemeler ve başlıklar
    fig.update_layout(
        title="Production Over Years by Locations",
        showlegend=False,
        height=600,
        width=800,
    )

    # X ve Y eksenlerinin düzenlenmesi
    fig.update_xaxes(title="Year", tickfont=dict(size=12, color='black'))
    fig.update_yaxes(title="Production", tickfont=dict(size=12, color='black'))

    # Başlıkları kırmızı yapmak
    fig.update_layout(
        title_font=dict(size=20, color='red')
    )

    return fig



def plot_locandmethod(df,locations,years):
    start, end = years
    years = [str(year) for year in range(start, end+1)]

    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby(["Detail","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production")
        fig = px.sunburst(grouped,values="Production",path=["Detail","Location"],color="Detail",title="Total Production By Methods and Locations ")
        fig.update_layout(
            height=600,  
            width=800,  
            font=dict(size=18),  
            title=dict(
                font=dict(size=24, color="red"),
            )
        )
        
        fig.update_traces(
            textinfo="label+percent entry",  
            textfont_size=18,  
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




def plot_country_map(df,locations, years, countries=None, methods=None, species=None):
    start, end = years
    years = [str(year) for year in range(start, end+1)]
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        if countries:
            df = df[df["Country"].isin(countries)]
        if methods:
            df = df[df["Detail"].isin(methods)]
        if species:
            df = df[df["Species"].isin(species)]

        grouped = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production")
        fig = px.choropleth(grouped,locations="Country",locationmode="country names",color="Production",color_continuous_scale="RdBu")
        fig.update_layout(
            height=600,  # Yüksekliği artır
            width=800,  # Genişliği artır
            font=dict(size=18),  # Genel font boyutunu büyüt
            title=dict(
                text=f"Total Productions By Countries and Locations",
                font=dict(size=24, color="red"),
            )
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





def plot_specygrouped_bar(df,locations,years,species):
    start, end = years
    years = [str(year) for year in range(start, end+1)] 
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        df = df[df["Species"].isin(species)]
        grouped = df.groupby(["Location","Species"])[years].sum().sum(axis = 1).reset_index(name ="Production")
        fig = px.bar(grouped,x = "Location",y = "Production",color="Species",title="Total Productions By Species and Locations",barmode="group")
        fig.update_layout(
            title=dict(font=dict(size=24, color="red")),  
            height=400,
            width=600,
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
        fig = px.bar(grouped,x = "Location",y = "Production",color="Location",title="Total Productions")
        fig.update_layout(
            title=dict(font=dict(size=24, color="red")),  
            height=400,
            width=600,
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
    years = [str(year) for year in range(start, end+1)]  # Yılları stringe dönüştür
    if len(locations) > 0:
        df = df[df["Location"].isin(locations)]
        df = df[df["Detail"].isin(methods)]
        grouped = df.groupby(["Location","Detail"])[years].sum().sum(axis = 1).reset_index(name ="Production")

        fig = px.bar(grouped,x = "Location",y = "Production",color="Detail",title="Total Productions By Methods and Locations",barmode="group")
        fig.update_layout(
            title=dict(font=dict(size=24, color="red")),  
            height=400,
            width=600,
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
        rows = len(methods)  # Yöntemlere göre satır
        cols = len(locations)  # Ülkelere göre sütun

        # Çoklu grafik oluşturma
        figure = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"{method} - {location}" for method in methods for location in locations]
        )

        
        for i, method in enumerate(methods, start=1):  
            filtered = grouped[grouped["Detail"] == method]  
            for j, location in enumerate(locations, start=1):  
                sub_filtered = filtered[filtered["Location"] == location]  

                if not sub_filtered.empty:
                    # Çubuk grafiği oluştur
                    bar_trace = go.Bar(
                        x=sub_filtered["Species"], 
                        y=sub_filtered["Production"], 
                        name=f"{method} - {location}",
                        marker=dict(line=dict(width=1)),
                    )
                    
                    figure.add_trace(bar_trace, row=i, col=j)

        
        figure.update_layout(
            title=dict(font=dict(size=24, color="red")),
            height=rows * 400,  
            width=cols * 400, 
            title_text="Total Productions by Species, Methods, and Locations",
        )

        return figure
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



        


