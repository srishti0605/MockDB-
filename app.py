import json
from flask import Flask, jsonify, request 

app = Flask(__name__)

class User:
    def __init__(self, success, message, title):
        self.success = success
        self.message = message
        self.title = title

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<User { self.success }>'

json_string = '''{"success":true,
    "message":"",
    "title":null,
    "object":{
        "employee":{
            "createdBy":"admin",
            "createdAt":"1580757593333",
            "version":0,
            "lastModifiedBy":"admin",
            "id":"5e387259a397a439bd5865be",
            "systemId":"30",
            "firstName":"PARAS LAMBA",
            "fatherName":null,
            "contact":"9555625312",
            "secondaryContact":null,
            "email":"paras.lamba@livpure.in",
            "gender":"MALE",
            "imageld":"",
            "address":"Village Tosham, District Bhiwani Road, Tehsil Toasham, District Bhiwani",
            "flatNo":null,
            "landmark":null,
            "city":null,
            "locality":null,
            "state":"",
            "stateCode":null,
            "region":null,
            "country":"India",
            "pincode":null,
            "pincodeType":null,
            "dob":null,
            "location":null,
            "username":"2001696",
            "role":"CALL_CENTRE_ADMIN",
            "status":"ACTIVE",
            "qualification":"",
            "language":"English/Hindi",
            "experience":"",
            "gstin":null,
            "lastPasswordResetAt":null,
            "profileImageUrl":null,
            "stageTypes":["T0",
                "T1",
                "T2",
                "T3"
            ]
        },
        "authToken":"ebddebwbefbrhjfvhrfvevfevfejvrfjehrgfegrfe"
    }
}'''

with open('data.json', 'r') as json_file:
    print(json.loads(json_file.read()))


@app.route('/endpoint1', methods=['POST'])
def form_to_json():
    data = request.form.to_dict(flat=False)
    return jsonify(data)