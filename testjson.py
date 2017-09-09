import json

with open('config_pl.json') as json_data:
    d = json.load(json_data)
    print(type(d))
    #print(d)
    #print(d["imageSettings"])
    #print(json.dumps(d, indent=4))
    #print(d.imageSettings)


    print(d['imageSettings']['quality'])

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d




#data = json.loads(d, object_hook=JSONObject)
