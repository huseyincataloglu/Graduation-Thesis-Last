import pandas as pd


def get_total_features(df,variable):
    return df[variable].nunique()


def get_uniquefeature(df,main_feature):
    years = df.columns[4:]
    topproduction_byfeature= df.groupby(main_feature)[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return topproduction_byfeature[main_feature].values




# Specy Page
def get_production_detailsby_species(df,variable,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    df = df[df["Species"].isin(variable)]
    df = df.groupby(["Species","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return df["Detail"].unique()
#Specy Page

def get_commonlocations_forcountries(df,countries,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = []
    if len(countries) > 0:
        df = df[df["Country"].isin(countries)]
        df = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
        speciesvaluesoffirst =  df[df["Country"] == countries[0]]["Location"].values
        if len(countries) > 1: 
            for i in range(1,len(countries),1):
                country = countries[i]
                species = df[df["Country"] == country]["Location"].values
                for specy in species:
                    if not specy in commons and specy in speciesvaluesoffirst:
                        commons.append(specy)
            return commons
        return speciesvaluesoffirst
    return commons

def get_methodsfor_locandcountry(df,countries,years,locations = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = []
    if len(countries) > 0:
        if locations:
            df = df[df["Location"].isin(locations)]
        df = df[df["Country"].isin(countries)]
        grouped = df.groupby(["Country","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
        speciesvaluesoffirst =  grouped[grouped["Country"] == countries[0]]["Detail"].values
        if len(countries) > 1: 
            for i in range(1,len(countries),1):
                country = countries[i]
                species = grouped[grouped["Country"] == country]["Detail"].values
                for specy in species:
                    if not specy in commons and specy in speciesvaluesoffirst:
                        commons.append(specy)
        else:
            commons = list(speciesvaluesoffirst)
        if locations and len(locations) > 1:
            location_methods = []
            for location in locations:
                loc_methods = df[df["Location"] == location]["Detail"].values
                location_methods.append(set(loc_methods))
            if commons:
                commons = [method for method in commons if all(method in loc_set for loc_set in location_methods)]
            else:
                commons = list(set.intersection(*location_methods))
    return commons
    


def get_species_bycountries(df,countries,years,locations = None,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    newdf= df.copy()
    if len(countries) > 0:
        if locations:
            newdf = newdf[newdf["Location"].isin(locations)]

        if methods:
            newdf = newdf[newdf["Detail"].isin(methods)]

        newdf = newdf[newdf["Country"].isin(countries)]
        newdf = newdf.groupby(["Country","Species","Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
        commons = set(df[df["Country"] == countries[0]]["Species"].values)
        if len(countries) > 1:
            for i in range(1,len(countries),1):
                country = countries[i]
                species = set(newdf[newdf["Country"] == country]["Species"].values)
                commons = commons.intersection(species)

        if locations and len(locations) > 1:
            sub_locations = set()
            for location in locations:
                if len(sub_locations) == 0:
                    sub_locations = set(newdf[newdf["Location"] == location]["Species"].values)
                else:
                    sub_locations = sub_locations.intersection(set(newdf[newdf["Location"] == location]["Species"].values))
            commons = commons.intersection(sub_locations)       
        if methods and len(methods) > 1:
            sub_methods = set()
            for method in methods:
                if len(sub_methods) == 0:
                    sub_methods = set(newdf[newdf["Detail"] == method]["Species"].values)
                else:
                    sub_methods = sub_methods.intersection(set(newdf[newdf["Detail"] == method]["Species"].values))
            commons = commons.intersection(sub_methods)  
    return commons
                 

