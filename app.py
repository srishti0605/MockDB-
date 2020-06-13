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

json_string = ""


@app.route('/')
def welcome():
    with open('data.json', 'r') as json_file:
        user_data = json.loads(json_file.read())

    print(user_data)
    return jsonify(user_data)


@app.route('/endpoint1', methods=['POST'])
def form_to_json():
    data = request.form.to_dict(flat=False)
    return jsonify(data)
