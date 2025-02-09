import pandas as pd
def get_summary_dfOverview(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    copy = df
    total_production = copy[years].sum().sum()
    mean_production = copy[years].mean().mean()
    median_production = copy[years].median().median()
    std_production = copy[years].std().mean()
    min_production = copy[years].min().min()
    max_production = copy[years].max().max()
    pd.options.display.float_format = "{:,.2f}".format
    datafra = pd.DataFrame({
        "Summary" : ["Total","Mean","Median","Standart deviation","Min","Max"],
        "Values" : [total_production, mean_production,median_production,std_production,min_production,max_production]
    })
    return datafra

        

def get_yearly_statsOverview(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]

    pd.options.display.float_format = "{:,.2f}".format
    aggdf = df[years].agg(["sum","mean","median","min","max","std"]).transpose()
    return aggdf

def get_most_features(df,years):
    start,end = years
    years = [str(year) for year in range(start,end+1,1)]
    detail = df.groupby("Detail")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    detail = detail[detail["Production"] == detail["Production"].max()]

    locat = df.groupby("Location")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    locat = locat[locat["Production"] == locat["Production"].max()]

    countr = df.groupby("Country")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    countr = countr[countr["Production"] == countr["Production"].max()]

    specy = df.groupby("Species")[years].sum().sum(axis = 1).reset_index(name = "Production").sort_values("Production",ascending = False)
    specy = specy[specy["Production"] == specy["Production"].max()]

    data = pd.DataFrame({"Stages" : [detail["Detail"].values[0],locat["Location"].values[0] ,countr["Country"].values[0],specy["Species"].values[0]] ,"Production": [detail["Production"].values[0],locat["Production"].values[0] ,countr["Production"].values[0],specy["Production"].values[0]]})
    data["Production"] = data["Production"].map(lambda x: "{:_}".format(int(x)))

    data.rename({"Stages" : " Top Features"},inplace=True,axis=1)
    return data



