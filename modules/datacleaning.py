
def clean_data(dataframe):

    
    production_mapping = {
    "Capture production": "Capture",
    "Aquaculture production (marine)": "Marine Aq",
    "Aquaculture production (freshwater)": "Freshwater Aq",
    "Aquaculture production (brackishwater)": "Brackish Aq"
    }
    dataframe["Detail"] = dataframe["Detail"].map(production_mapping)

    return dataframe