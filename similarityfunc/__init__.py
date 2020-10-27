import logging
import azure.functions as func
from random import Random
import tldextract 
import requests
from bs4 import BeautifulSoup 
import re
import pandas as  pd
import json
from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)
#You can download this file from here https://api.dataforseo.com/_examples/python/_python_Client.zip
client = RestClient("vijaym@intellasphere.com", "VvMRrZP6PuEcN8vi")
rnd = Random()

def simlkey(kw1,kw2,kw3,kw4,kw5):
    df = pd.read_csv("C:/Users/Acer/Desktop/HTTP/anufurniture.csv")
    df6=df[:100] 
    #df6 = df5.sort_values(by = 'totalscore', ascending = False) 
    #for i in names:
       # pattern = '|'.join(names)
    df6=df6[df6.keyword.str.contains(kw1)]
    df7=df6[df6.keyword.str.contains(kw2)]
    df7=df6[df6.keyword.str.contains(kw3)]
    df7=df6[df6.keyword.str.contains(kw4)]
    df7=df6[df6.keyword.str.contains(kw5)]
    return df7.to_json()


def main(req: func.HttpRequest,outputblob: func.Out[str]):
    logging.info('Seoofcompany HTTP trigger function processed a request.')
    
    seo_simlkey = req.params.get("kw1")
    seo_simlkey1=req.params.get("kws2")
    seo_simlkey2=req.params.get("kw3")
    seo_simlkey3=req.params.get("kw4")
    seo_simlkey4=req.params.get("kw5")


    if seo_simlkey is not None:
          if seo_simlkey1 is not None:
                if seo_simlkey2 is not None:
                      if seo_simlkey3 is not None:
                            if seo_simlkey4 is not None:
                              seo_string1 = simlkey(seo_simlkey,seo_simlkey1,seo_simlkey2,seo_simlkey3,seo_simlkey4)
                              seo_string1 = {""}
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