import logging
import azure.functions as func
from random import Random
import tldextract 
import requests
from bs4 import BeautifulSoup 
import re
import pandas
import json
from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
#from azure.storage.blob import BlockBlobService, PublicAccess
#from azure.storage.blob.blockblobservice import BlockBlobService

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
rnd = Random() #you can set as "index of post_data" your ID, string, etc. we will return it with all results.


#stop = input()
def Seo(company_name):
    a1='https://www.google.dz/search?q='
    a2=company_name
    a3=a1+a2
    page = requests.get(a3)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    k=1
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        if k==2:
            break
    #print(re.split(":(?=http)",link["href"].replace("/url?q=","")))
        websitelink=re.split(":(?=http)",link["href"].replace("/url?q=",""))
        k=k+1

        list = tldextract.extract(websitelink[0])
        domain_name = list.domain + '.' + list.suffix
        country_code = "IN"
        language = "en"
        response = client.get("/v2/kwrd_for_domain/%s/%s/%s" % (domain_name, country_code, language))
        if response["status"] == "error":
            "error. Code: %d Message: %s" % (response["error"]["code"], response["error"]["message"])
        else:
            response["results"]
        cat= []
        cat1=[]
        cat2=[]
        cat3=[]
        key=next(iter(response["results"]))
        l=len(response["results"])
        for i in range(l):
            a=response["results"][i]['key']
            b=response["results"][i]['sv']
            c=response["results"][i]['cpc']
            d=response["results"][i]['cmp']
            cat.append(a)
            cat1.append(b)
            cat2.append(c)
            cat3.append(d)
        df = pandas.DataFrame(cat,columns = ["keyword"])
        df1 = pandas.DataFrame(cat1,columns = ["Sv"])
        df2 = pandas.DataFrame(cat2,columns = ["cpc"])
        df3 = pandas.DataFrame(cat3,columns = ["cmp"])
        df4 = pandas.concat([df,df1,df2,df3],axis=1)
        df5=df4[:50]
        df5['total'] = df5['Sv'].sum()
        df5['Sv_score'] = df5['Sv']/df5['total']
        df5['totalscore']=df5['Sv_score']*5-df5['cmp']
        df5["Rank"] = df5["totalscore"].rank(ascending=0) 
        return df5.to_json()

#def main(req: func.HttpRequest,outputblob: func.Out[str]):
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Seoofcompany HTTP trigger function processed a request.')

    seo_param = req.params.get('company_name')

    if seo_param is not None:
        try:
            company_name = seo_param
        except ValueError:
            company_name = "Null"   # A default

        if company_name != "Null":
            seo_string1 = {company_name:Seo(company_name)}
            return func.HttpResponse(
                                  json.dumps(seo_string1),
                                mimetype="application/json",
            )
            return func.HttpResponse("success")
    return func.HttpResponse(
         "Please pass the URL parameter ?company_name= to specify a positive number of digits.",
         status_code=400
    )
    