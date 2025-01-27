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
