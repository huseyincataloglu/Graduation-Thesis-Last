import pandas as pd


def get_total_features(df,variable):
    return df[variable].nunique()


def get_uniquefeature(df,main_feature,filter_feature = None,filter_value = None):
    years = df.columns[4:]
    if filter_feature:
        df = df[df[filter_feature] == filter_value]    
    topproduction_byfeature= df.groupby(main_feature)[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    return topproduction_byfeature[main_feature].values

                    

def get_summary_df(df,filter_name,filter_value,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    if filter_value != "All Areas":
        df1 = df[df[filter_name] == filter_value]
        total_production = df1[years].sum().sum()
        mean_production = df1[years].mean().mean()
        median_production = df1[years].median().median()
        std_production = df1[years].std().mean()
        min_production = df1[years].min().min()
        max_production = df1[years].max().max()
        pd.options.display.float_format = "{:,.2f}".format
        datafra = pd.DataFrame({
            filter_value : ["Total","Mean","Median","Standart deviation","Min","Max"],
            "Values" : [total_production, mean_production,median_production,std_production,min_production,max_production]
        })
        return datafra
    else:
        copy = df
        total_production = copy[years].sum().sum()
        mean_production = copy[years].mean().mean()
        median_production = copy[years].median().median()
        std_production = copy[years].std().mean()
        min_production = copy[years].min().min()
        max_production = copy[years].max().max()
        pd.options.display.float_format = "{:,.2f}".format
        datafra = pd.DataFrame({
            filter_value : ["Total","Mean","Median","Standart deviation","Min","Max"],
            "Values" : [total_production, mean_production,median_production,std_production,min_production,max_production]
        })
        return datafra

        

def get_yearly_stats(df,filter_name,filter_value,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    if filter_value != "All Areas":
        df = df[df[filter_name] == filter_value]
        pd.options.display.float_format = "{:,.2f}".format
        aggdf = df[years].agg(["sum","mean","median","min","max","std"]).transpose()
        return aggdf
    else:
        pd.options.display.float_format = "{:,.2f}".format
        aggdf = df[years].agg(["sum","mean","median","min","max","std"]).transpose()
        return aggdf

        



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
    if len(countries) == 0:
        return []
    df = df[df["Country"].isin(countries)]
    df = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    commons = None
    for country in countries:
        locations = set(df[df["Country"] == country]["Location"].values)
        if commons is None:
            commons = locations
        else:
            commons = commons.intersection(locations) 
    return list(commons) if commons else []         
    

def get_methodsfor_locandcountry(df,countries,years,locations = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    if len(countries) > 0:
        if locations:
            df = df[df["Location"].isin(locations)]
        df = df[df["Country"].isin(countries)]
        grouped = df.groupby(["Country","Detail","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)

        for country in countries:
            methods = set(grouped[grouped["Country"] == country]["Detail"].values)
            if len(commons) == 0:
                commons = methods
            else:
                commons = commons.intersection(methods)

        if locations and len(locations) > 1:
            for location in locations:
                location_methods = set(grouped[grouped["Location"] == location]["Detail"].values)
                commons = commons.intersection(location_methods)
                
        return list(commons)        
    return list(commons)
    


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
        commons = set(newdf[newdf["Country"] == countries[0]]["Species"].values)
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
                 



#specy page
#----------------------
def get_commonlocations_forspecies(df,species,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    if len(species) == 0:
        return []
    df = df[df["Species"].isin(species)]
    df = df.groupby(["Location","Species"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    commons = None
    for country in species:
        locations = set(df[df["Species"] == country]["Location"].values)
        if commons is None:
            commons = locations
        else:
            commons = commons.intersection(locations) 
    return list(commons) if commons else []     


def get_methodsfor_locandspecies(df,species,years,locations = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    if len(species) > 0:
        if locations:
            df = df[df["Location"].isin(locations)]
        df = df[df["Species"].isin(species)]
        grouped = df.groupby(["Species","Detail","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)

        for specy in species:
            methods = set(grouped[grouped["Species"] == specy]["Detail"].values)
            if len(commons) == 0:
                commons = methods
            else:
                commons = commons.intersection(methods)

        if locations and len(locations) > 1:
            for location in locations:
                location_methods = set(grouped[grouped["Location"] == location]["Detail"].values)
                commons = commons.intersection(location_methods)
                
        return list(commons)        
    return list(commons)


def get_countries_byspecies(df,species,years,locations = None,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    newdf= df.copy()
    if len(species) > 0:
        if locations:
            newdf = newdf[newdf["Location"].isin(locations)]

        if methods:
            newdf = newdf[newdf["Detail"].isin(methods)]

        species = list(species)

        newdf = newdf[newdf["Species"].isin(species)]
        newdf = newdf.groupby(["Species","Country","Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
        commons = set(newdf[newdf["Species"] == species[0]]["Country"].values)
        if len(species) > 1:
            for specy in species[1:]:
                species_countries = set(newdf[newdf["Species"] == specy]["Country"].values)
                commons = commons.intersection(species_countries)

        if locations and len(locations) > 1:
            sub_locations = set()
            for location in locations:
                if len(sub_locations) == 0:
                    sub_locations = set(newdf[newdf["Location"] == location]["Country"].values)
                else:
                    sub_locations = sub_locations.intersection(set(newdf[newdf["Location"] == location]["Country"].values))
            commons = commons.intersection(sub_locations)       
        if methods and len(methods) > 1:
            sub_methods = set()
            for method in methods:
                if len(sub_methods) == 0:
                    sub_methods = set(newdf[newdf["Detail"] == method]["Country"].values)
                else:
                    sub_methods = sub_methods.intersection(set(newdf[newdf["Detail"] == method]["Country"].values))
            commons = commons.intersection(sub_methods)  
    return commons




# location page -----------------



def get_commoncountr_forlocs(df,locations,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    if len(locations) == 0:
        return []
    df = df[df["Location"].isin(locations)]
    df = df.groupby(["Location","Country"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    commons = None
    for location in locations:
        locations = set(df[df["Location"] == location]["Country"].values)
        if commons is None:
            commons = locations
        else:
            commons = commons.intersection(locations) 
    return list(commons) if commons else []     


def get_methodsfor_locandcount(df,locations,years,countries = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    if len(locations) > 0:
        if countries:
            df = df[df["Country"].isin(countries)]
        df = df[df["Location"].isin(locations)]
        grouped = df.groupby(["Country","Detail","Location"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)

        for location in locations:
            methods = set(grouped[grouped["Location"] == location]["Detail"].values)
            if len(commons) == 0:
                commons = methods
            else:
                commons = commons.intersection(methods)

        if countries and len(countries) > 1:
            for country in countries:
                location_methods = set(grouped[grouped["Country"] == country]["Detail"].values)
                commons = commons.intersection(location_methods)
                
        return list(commons)        
    return list(commons)


def get_species_bycountlocmethd(df,locations,years,countries = None,methods = None):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    commons = set()
    newdf= df.copy()
    if len(locations) > 0:
        if countries:
            newdf = newdf[newdf["Country"].isin(countries)]

        if methods:
            newdf = newdf[newdf["Detail"].isin(methods)]

        species = list(locations)

        newdf = newdf[newdf["Location"].isin(locations)]
        newdf = newdf.groupby(["Species","Country","Location","Detail"])[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
        commons = set(newdf[newdf["Location"] == locations[0]]["Species"].values)
        if len(locations) > 1:
            for location in locations[1:]:
                species_countries = set(newdf[newdf["Location"] == location]["Species"].values)
                commons = commons.intersection(species_countries)

        if countries and len(countries) > 1:
            sub_locations = set()
            for country in countries:
                if len(sub_locations) == 0:
                    sub_locations = set(newdf[newdf["Country"] == country]["Species"].values)
                else:
                    sub_locations = sub_locations.intersection(set(newdf[newdf["Country"] == country]["Species"].values))
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


  