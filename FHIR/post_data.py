import requests
import json
import os

URL = "https://stu3.test.pyrohealth.net/fhir"


FHIRJSONMimeType = 'application/fhir+json'
header_defaults = {
            'Accept': FHIRJSONMimeType,
            'Accept-Charset': 'UTF-8',
        }

def create_resource():
     with open(os.path.join("resource-examples", "SimplePatient-resources", 
                        "PatientResourceExample1.json")) as f:
        data = json.load(f)
     r = requests.post(URL+"/Patient", json = data,
                       headers = header_defaults)
     if r.ok:
         return r.json()["id"]
     else:
         raise Exception("Something went wrong")


