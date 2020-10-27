import logging
from json import loads
from json import dumps
import azure.functions as func
import pandas as pd
def Seo_competitors(names1,names2,names3,names4,names5):
    df = pd.read_csv("C:/Users/Acer/Desktop/HTTP/anufurniture.csv")
    df6=df[:100]
    #for i in names:
       # pattern = '|'.join(names)
    df6=df6[~df6.keyword.str.contains(names1)]
    df7=df6[~df6.keyword.str.contains(names2)]
    df7=df6[~df6.keyword.str.contains(names3)]
    df7=df6[~df6.keyword.str.contains(names4)]
    df7=df6[~df6.keyword.str.contains(names5)]
    return df7.to_json()


def main(req: func.HttpRequest,outputblob: func.Out[str]):
    logging.info('Seoofcompany HTTP trigger function processed a request.')
    
    seo_comp = req.params.get("names1")
    seo_comp1=req.params.get("names2")
    seo_comp2=req.params.get("names3")
    seo_comp3=req.params.get("names4")
    seo_comp4=req.params.get("names5")


    if seo_comp is not None:
          if seo_comp1 is not None:
                if seo_comp2 is not None:
                      if seo_comp3 is not None:
                            if seo_comp4 is not None:
                              seo_string1 = Seo_competitors(seo_comp,seo_comp1,seo_comp2,seo_comp3,seo_comp4)
                              outputblob.set(seo_string1)
            #return func.HttpResponse(
                #json.dumps(seo_string),
              #  mimetype="application/json",
            #)
                              return func.HttpResponse(
                                  json.dumps(seo_string1),
                                mimetype="application/json",
            )
    return func.HttpResponse(
         "Please pass the URL parameter ?names1=&names2=.... to specify a input.(max=5,if not parametes specify /)",
         status_code=400
    )