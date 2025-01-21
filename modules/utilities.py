import pandas as pd


def get_total_features(df,variable):
    return df[variable].nunique()


def get_unique_features(df,variable):
    years = df.columns[4:]
    topcountries= df.groupby(variable)[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return topcountries[variable].values


def get_production_detailsby_species(df,variable,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    df = df[df["Species"].isin(variable)]
    df = df.groupby(["Species","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return df["Detail"].unique()
    





def get_commonspecies_forcountries(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    df = df[df["Country"].isin(countries)]
    df = df.groupby(["Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    speciesvaluesoffirst =  df[df["Country"] == countries[0]]["Species"].values
    commons = []
    for i in range(1,len(countries),1):
        country = countries[i]
        species = df[df["Country"] == country]["Species"].values
        for specy in species:
            if not specy in commons:
                if specy in speciesvaluesoffirst:
                    commons.append(specy)

    return commons                
            




def get_species_bycountries(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    df = df[df["Country"].isin(countries)]
    df = df.groupby(["Country","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return df["Species"].unique()
    
