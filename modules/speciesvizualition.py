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

def plot_partvsprod_by_species(df, species, years,locations = None,methods = None,countries = None):
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    if locations:
            df = df[df["Location"].isin(locations)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if countries:
        df = df[df["Country"].isin(countries)]
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
            coloraxis_colorbar=dict(     
                title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
            )
        )
        return figure



    

def plot_speciesprdouction_by_detail(df,species,years,locations =None):
    start,end = years
    years = [str(year) for year in range(start,end + 1,+1)]
    if locations :
        df = df[df["Location"].isin(locations)]
    
    speciyproductions = df.groupby(["Species","Detail","Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    filteredspeciesproductions = speciyproductions[speciyproductions.Species.isin(species)]
    figure = px.icicle(filteredspeciesproductions,values="Production",path=[px.Constant("All"),"Detail","Location","Species"],color="Production",color_continuous_scale="RdBu",title="Icicle Chart of Species Production With Location Filter")
    figure.update_layout(
        title=dict(
            font=dict(size=22,color = "red")  # Başlık yazı boyutu
        ),
        font=dict(size=16),  # Yazı boyutu
        coloraxis_colorbar=dict(
            title="Production",        # Renk skalası başlığı
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )
    return figure

def plot_species_overyears(df, species, years, locations=None, methods=None, countries=None):
    start, end = years
    years1 = [str(year) for year in range(start, end + 1, +1)]
    
    if locations:
        df = df[df["Location"].isin(locations)]
    if methods:
        df = df[df["Detail"].isin(methods)]
    if countries:
        df = df[df["Country"].isin(countries)]
    
    topcountries = df.groupby("Species")[years1].sum().reset_index()
    melted = pd.melt(topcountries, id_vars=["Species"], value_vars=years1)
    melted = melted[melted["Species"].isin(species)]
    melted.rename({"variable": "Years", "value": "Production"}, axis=1, inplace=True)
    
    figure = px.area(
        melted,
        x="Years",
        y="Production",
        color="Species",
        color_discrete_sequence=px.colors.sequential.RdBu,
        facet_col_wrap=2,
        facet_col="Species"
    )
    
    figure.update_layout(
        title=dict(
            text="Species Production Over Years",
            font=dict(size=22,color = "red")  # Başlık yazı boyutu
        ),
        font=dict(size=16),  # Genel yazı boyutu
        xaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  # X eksen başlık yazı boyutu ve rengi
            tickfont=dict(size=14, color="black")  # X eksen işaret yazı boyutu ve rengi
        ),
        yaxis=dict(
            gridwidth=1,
            title_font=dict(size=18, color="red"),  # Y eksen başlık yazı boyutu ve rengi
            tickfont=dict(size=14, color="black")  # Y eksen işaret yazı boyutu ve rengi
        ),
        coloraxis_colorbar=dict(
            title_font=dict(size=16)  # Renk skalası başlık yazı boyutu
        )
    )

    figure.update_xaxes(
        title_font=dict(size=18, color="red"),  # Başlık yazı boyutu ve rengi
        tickfont=dict(size=14, color="black")  # İşaret yazı boyutu ve rengi
    )
    figure.update_yaxes(
        title_font=dict(size=18, color="red"),  # Başlık yazı boyutu ve rengi
        tickfont=dict(size=14, color="black")  # İşaret yazı boyutu ve rengi
    )


    return figure

def plot_speciescountry_parallel(df, species, years, countries=None):
    start, end = years
    listyears = [str(year) for year in range(start, end + 1, 1)]
    
    # Ülkeleri filtrele (eğer varsa)
    if countries:
        df = df[df["Country"].isin(countries)]
    else:
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
    # Türleri filtrele
    df = df[df["Species"].isin(species)]    
    
    # Yeni veri çerçevesi oluştur: Sadece gerekli sütunlar
    newdf = df.loc[:, ["Species", "Detail", "Country"] + listyears]
    
    # Üretim toplamını hesapla
    newdf2 = df.groupby(["Species", "Detail", "Country"])[listyears].sum().sum(axis=1).reset_index(name="Production")
    
    # Yeni üretim değerini eski veri çerçevesine ekle
    newdf = newdf.merge(newdf2, on=["Species", "Detail", "Country"], how="left")
    
    # Parallel categories grafiği oluştur
    fig = px.parallel_categories(newdf, dimensions=["Species", "Detail", "Country"],
                                 color="Production",  # Renklendirme için 'Production' değerini kullan
                                 color_continuous_scale=px.colors.sequential.Plasma,  # Sürekli renk skalası
                                 title="Parallel Category Chart,Species and Production by Country and Detail")
    
    fig.update_layout(
        title=dict(
            font=dict(size=22,color = "red")  # Başlık yazı boyutu
        ),
        font=dict(size=12),
        coloraxis_colorbar=dict(title="Production")
    )
    
    return fig

def plot_parallel_corgrapyearly(df, species, years, locations=None, methods=None, countries=None):
    # Veriyi filtreleme
    filtered_df = df.copy()
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
            showlegend=False,
            height=400,
            width=600,
        )
        return fig
    # Türleri filtrele
    filtered_df = filtered_df[filtered_df["Species"].isin(species)]

    # Lokasyonları filtrele
    if locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(locations)]

    # Yöntemleri filtrele
    if methods:
        filtered_df = filtered_df[filtered_df["Detail"].isin(methods)]

    # Ülkeleri filtrele
    if countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(countries)]

    # Türleri sayısallaştırma (renk kodlama için)
    filtered_df["Species_num"] = filtered_df["Species"].astype("category").cat.codes
    st.write("Species Cordinates")
    st.dataframe(pd.DataFrame(pd.Series(filtered_df["Species_num"].unique(),index =filtered_df["Species"].unique())).reset_index().rename(columns = {"index": "Species", 0: "Species_num"}))
    # Yılları seçme
    year_cols = [str(year) for year in years if str(year) in filtered_df.columns]
    if not year_cols:
        raise ValueError("Seçilen yıllar, veri çerçevesinde mevcut değil.")

    # Paralel koordinat grafiği için boyutlar oluşturma
    dimensions = [
        dict(
            range=[filtered_df[col].min(), filtered_df[col].max()],
            label=col,  # Eksen adı
            values=filtered_df[col],  # Eksen değerleri
            tickformat=".0f",  # Sayı biçimlendirme
        )
        for col in year_cols
    ]
    # Türler için boyut ekleme (renk ve kategori)
    dimensions.insert(0, dict(
        tickvals=filtered_df["Species_num"].unique(),
        label="Species",
        values=filtered_df["Species_num"],
    ))

    # Paralel koordinat grafiği oluşturma
    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=filtered_df["Species_num"],
                colorscale='viridis',
                showscale=True
            ),
            dimensions=dimensions
        )
    )

    # Grafik düzenlemeleri
    fig.update_layout(
        font=dict(size=14),  # Genel yazı tipi
        margin=dict(l=50, r=50, t=50, b=50),  # Kenar boşlukları
    )
    return fig




def plot_parallel_corgrap(df, species, years, locations=None, methods=None, countries=None):
    # Yıllar aralığını oluştur
    start, end = years
    years = [str(year) for year in range(start, end + 1)]
    
    # Veriyi filtreleme
    filtered_df = df.copy()

    # Türleri filtrele
    filtered_df = filtered_df[filtered_df["Species"].isin(species)]

    # Lokasyonları filtrele
    if locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(locations)]

    # Yöntemleri filtrele
    if methods:
        filtered_df = filtered_df[filtered_df["Detail"].isin(methods)]

    # Ülkeleri filtrele
    if countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(countries)]

    # Yıllara göre toplam üretimi ekle
    filtered_df["Total Production"] = filtered_df[years].sum(axis=1)

    # Gruplama: Tür temel alınır, seçilen diğer argümanlara göre gruplanır
    group_columns = ["Species"]  # Tür her zaman temel
    if locations:
        group_columns.append("Location")
    if methods:
        group_columns.append("Detail")
    if countries:
        group_columns.append("Country")

    grouped_df = filtered_df.groupby(group_columns, as_index=False).agg({"Total Production": "sum"})

    # Kategorik verileri sayısallaştırma
    for column in group_columns:
        grouped_df[f"{column}_num"] = grouped_df[column].astype("category").cat.codes

    
    grouped_df["hovertext"] = grouped_df.apply(lambda row: ",".join([f"{col} :{row[col]}" for col in group_columns])+ f"Total Production : {row["Total Production"]}",axis = 1)

    dimensions = [
        dict(range=[grouped_df[f"{col}_num"].min(), grouped_df[f"{col}_num"].max()],
             label=f"{col}_num", values=grouped_df[f"{col}_num"])
        for col in group_columns
    ]

    dimensions.append(
        dict(range=[grouped_df["Total Production"].min(), grouped_df["Total Production"].max()],
             label="Total Production", values=grouped_df["Total Production"])
    )

    # Paralel koordinat grafiği oluşturma
    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=grouped_df["Species_num"],
                colorscale="viridis",
                showscale=True,
            ),
            dimensions=dimensions
        )
    )


    # Kullanıcıya seçilen argümanları gösterme
    st.subheader("Selected Dimensions")
    for col in group_columns:
        st.dataframe(grouped_df[[col, f"{col}_num"]].drop_duplicates(subset=[col]))

    # Grafik düzenlemeleri
    fig.update_layout(
        font=dict(size=14),
        margin=dict(l=50, r=50, t=50, b=50),
    )
    return fig
    
    