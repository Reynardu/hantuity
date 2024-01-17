import json

from hantuity import NtuityRequest

print("Test The Code")

id = ""
bearer = ""
user = ""
password = ""

json_cred = "./data/ntuityCred.json"

jsonfile = open(json_cred, encoding="utf8")
jsondata = json.load(jsonfile)

id = jsondata["id"]
bearer = jsondata["bearer"]
user = jsondata["user"]
password = jsondata["password"]



nr = NtuityRequest.NtuityRequestClass(id,bearer,user,password)

print(nr)