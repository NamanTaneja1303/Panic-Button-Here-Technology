import json
import os

from here_location_services import LS


LS_API_KEY = os.environ.get("tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY")  # Get API KEY from environment.
ls = LS(api_key=LS_API_KEY)

address = "Invalidenstr 116, 10115 Berlin, Germany"
geo = ls.geocode(query=address)
print(json.dumps(geo.to_geojson(), indent=2, sort_keys=True))