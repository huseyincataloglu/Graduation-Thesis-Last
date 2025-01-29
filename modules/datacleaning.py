# Veri setinin temizlenmesi
def clean_data(dataframe):
    # Tekrar eden değerleri düşürdüm
    dataframe = dataframe.drop_duplicates()
    # Eksik verileri doldurdum

    kayıp_ülkeler = dataframe[dataframe["Country"].isnull()][["Country","Location"]]
    kayıp_olmayan_ülkeler = dataframe[dataframe["Country"].notnull()][["Country","Location","Species"]]

    def fill_country(row):
        match = kayıp_olmayan_ülkeler[
                (kayıp_olmayan_ülkeler["Location"] == row["Location"])
                ]
        if len(match) > 0:
            return match["Country"].mode()[0]
        else:
            return row["Country"]

    kayıp_ülkeler["Country"] = kayıp_ülkeler.apply(fill_country,axis = 1)
    dataframe.loc[dataframe["Country"].isnull(),"Country"] = kayıp_ülkeler["Country"]    




    kayıp_türler = dataframe[dataframe["Species"].isnull()][["Species","Country","Location"]]
    kayıp_olmayan_türler = dataframe[dataframe["Species"].notnull()][["Species","Country","Location"]]

    def fill_species(row):
        match = kayıp_olmayan_türler[(kayıp_olmayan_türler["Location"] == row["Location"]) & (kayıp_olmayan_türler["Country"] == row["Country"])]

        if match.shape[0] > 0:
            return match["Species"].mode()[0]
        else:
            return row["Species"] 

    kayıp_türler["Species"] = kayıp_türler.apply(fill_species,axis = 1)     
    dataframe.loc[dataframe["Species"].isnull(),"Species"] = kayıp_türler["Species"]


    # Making Some Features More Useful
    production_mapping = {
    "Capture production": "Capture",
    "Aquaculture production (marine)": "Marine Aq",
    "Aquaculture production (freshwater)": "Freshwater Aq",
    "Aquaculture production (brackishwater)": "Brackish Aq"
    }
    dataframe["Detail"] = dataframe["Detail"].map(production_mapping)


    
    return dataframe