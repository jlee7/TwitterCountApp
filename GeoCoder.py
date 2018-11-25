"""
This class converts the address into coordinates via opencagedata.com services.
"""
import requests
import json
import opencagedata_credentials

class GeoCoder:
    """This Class uses the OpenCageData API to convert an address into coordinates."""
    def __init__(self):
        self.api_key = opencagedata_credentials.api_key
        self.address = ""

    def set_new_address(self, address):
        self.address = address

    def get_coordinates_from_address(self):
        req = requests.request("GET","https://api.opencagedata.com/geocode/v1/json?q="+self.address+"&key="+self.api_key)

        req_json = req.json()

        print(req_json['results'][1]['geometry']['lat'], req_json['results'][1]['geometry']['lng'])
        return req_json['results'][1]['geometry']['lat'], req_json['results'][1]['geometry']['lng']

if __name__ == '__main__':
    gc = GeoCoder()
    gc.set_new_address("Unterdoernen 10, 42283, Wuppertal, Deutschland")
    gc.get_coordinates_from_address()


"""
Example: 'https://api.opencagedata.com/geocode/v1/json?q=-23.5373732,-46.8374628&pretty=1&key=5e98858142fc4b61ac9c6e5316b5d080' 

# pretty print json
parsed = json.loads(a.text)
print json.dumps(parsed, indent=4, sort_keys=True)
"""

# What I want is here: results [1] geometry lat, lng 