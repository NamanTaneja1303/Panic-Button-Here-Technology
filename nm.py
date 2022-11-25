import requests
import json
import pandas as pd
r = requests.get('https://get.geojs.io/')
ip_request=requests.get('https://get.geojs.io/v1/ip.json')
ipAdd = ip_request.json()
import json 
from urllib.request import urlopen
url = 'https://ipinfo.io/json'
response=urlopen(url)
data=json.load(response)
# print(data)
url ='https://get.geojs.io/v1/ip/geo/'+data['ip']+'.json'
geo_request=requests.get(url)
geo_data = geo_request.json()
# print(geo_data)
# print(geo_data['longitude'])
# print(geo_data['latitude'])

response_API = requests.get(' https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=6&lang=en&q=hospital+greaternoida&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
print(response_API.status_code)
data = response_API.text
datay = json.loads(data)
print(data)
x=(datay['items'])
print(len(datay['items']))
print(x[5]['position'])
for i in range(len(x)):
    print(x[i]['position'])
    print(x[i]['title'])


