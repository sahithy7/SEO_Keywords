#print("hello")
import pandas as pd
df = pd.read_csv("C:/Users/Acer/Desktop/HTTP/anufurniture.csv")
def Seo_competitors(names):
    #df=pd.read_csv("anufurniture.csv")
    df5=df[:100]
    df5['total'] = df5['Searchvolume'].sum()
    df5['Sv_score'] = df5['Searchvolume']/df5['total']
    df5['totalscore']=df5['Sv_score']*5-df5['cmp']
    df5["Rank"] = df5["totalscore"].rank(ascending=0) 
    df6 = df5.sort_values(by = 'totalscore', ascending = False) 
    #for i in names:
    #pattern = '|'.join(names)
    df6=df6[~df6.keyword.str.contains(names)]
    return df6
print(Seo_competitors("online"))