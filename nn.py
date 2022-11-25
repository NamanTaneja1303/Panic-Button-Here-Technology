import requests
import json
r = requests.get('https://get.geojs.io/')
ip_request=requests.get('https://get.geojs.io/v1/ip.json')
ipAdd = ip_request.json()
import json 
from urllib.request import urlopen
url = 'https://ipinfo.io/json'
response=urlopen(url)
data=json.load(response)

url ='https://get.geojs.io/v1/ip/geo/'+data['ip']+'.json'
geo_request=requests.get(url)
geo_data = geo_request.json()
response_API = requests.get(' https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=6&lang=en&q=police+greaternoida&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
print(response_API.status_code)
data = response_API.text
datay = json.loads(data)
print(data)
x=(datay['items'])
print(len(datay['items']))
print(x[5]['position'])
for i in range(len(x)):
    q=(x[i]['distance'])
    p=(x[i]['title'])
    r=(x[i]['position'])
t=(r['lat'])
o=(r['lng'])


response_APIi = requests.get('https://router.hereapi.com/v8/routes?transportMode=car&origin='+geo_data['latitude']+','+geo_data['longitude']+'&destination='+str(t)+','+str(o)+'&return=summary&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
print(response_APIi.status_code)
data = response_APIi.text
data = json.loads(data)
x=(datay['routes'])

response_APIi = requests.get('https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=2&lang=en&q=india&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
data = response_API.text
datay = json.loads(data)
print(datay)