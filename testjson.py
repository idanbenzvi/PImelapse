import json

with open('config_pl.json') as json_data:
    d = json.load(json_data)
    print(d)
