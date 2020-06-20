import json
import base64
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'employee.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    credential = Credential(email='paras.lamba@livpure.in',
                            password='password')
    user = User(createdBy='admin',
                createdAt='1580757593333',
                version=0,
                lastModifiedBy='',
                id='5e387259a397a439bd5865be',
                systemId=30,
                firstName='PARAS LAMBA',
                fatherName='',
                contact='9555625312',
                secondaryContact='',
                email='paras.lamba@livpure.in',
                gender='MALE',
                imageId='',
                address='Village Tosham, District Bhiwani Road, Tehsil Toasham, District Bhiwani',
                flatNo='',
                landmark='',
                city='',
                locality='',
                state='',
                stateCode='',
                region='',
                country='India',
                pincode='',
                pincodeType='',
                dob='',
                location='',
                username='2001696',
                role='CALL_CENTRE_ADMIN',
                status='ACTIVE',
                qualification='',
                language='English/Hindi',
                experience='null',
                gstin='',
                lastPasswordResetAt='',
                profileImageUrl='',
                stageTypes='T0')

    db.session.add(user)
    db.session.add(credential)
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def welcome():
    with open('data.json', 'r') as json_file:
        emp_data = json.loads(json_file.read())

    print(emp_data)
    return jsonify(emp_data)


@app.route('/add_employee', methods=['POST'])
@jwt_required
def register():

    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        data = request.form.to_dict()
        with open('data.json', 'r') as json_file:
            y = json.load(json_file)
            y.update(data)
        with open('data.json', 'w') as f:
            json.dump(y, f, indent=4)
        return jsonify(message="User created successfully."), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = Credential.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        message = "Login succeeded!"

        with open("static/0.jpg", "rb") as imageFile:
            str1 = str(base64.b64encode(imageFile.read()))

        with open('data.json', 'r') as json_file:
            emp_data = json.loads(json_file.read())
        dictionary = {'success': True, 'imgstring': str1,
                      'message': message, 'title': None,
                      'object': emp_data, 'authToken': access_token}
        return jsonify(dictionary)
    else:
        return jsonify(message="Incorrect email or password"), 401


# database models
class User(db.Model):
    __tablename__ = 'users'
    email = Column(String)
    createdBy = Column(String)
    createdAt = Column(String)
    version = Column(Integer)
    lastModifiedBy = Column(String)
    lastModifiedAt = Column(String)
    id = Column(String, primary_key=True)
    systemId = Column(Integer)
    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)
    fullName = Column(String)
    fatherName = Column(String)
    contact = Column(String)
    secondaryContact = Column(String)
    gender = Column(String)
    imageId = Column(String)
    address = Column(String)
    flatNo = Column(String)
    landmark = Column(String)
    city = Column(String)
    locality = Column(String)
    district = Column(String)
    state = Column(String)
    stateCode = Column(String)
    region = Column(String)
    country = Column(String)
    pincode = Column(String)
    pincodeType = Column(String)
    dob = Column(String)
    location = Column(String)
    username = Column(String)
    role = Column(String)
    status = Column(String)
    qualification = Column(String)
    language = Column(String)
    experience = Column(String)
    gstin = Column(String)
    lastPasswordResetAt = Column(String)
    profileImageUrl = Column(String)
    stageTypes = Column(String)
    password = Column(String)


class Credential(db.Model):
    __tablename__ = 'credentials'
    email = Column(String, primary_key=True)
    password = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('createdBy', 'createdAt', 'version', 'lastModifiedBy', 'lastModifiedAt', 'id', 'systemId', 'firstName', 'middleName', 'lastName', 'fullName', 'fatherName', 'contact', 'secondaryContact', 'email', 'gender', 'imageId', 'address', 'flatNo', 'landmark', 'city', 'locality', 'district', 'state', 'stateCode', 'region', 'country', 'pincode', 'pincodeType', 'dob', 'location', 'username', 'role', 'status', 'qualification', 'language', 'experience', 'gstin', 'lastPasswordResetAt', 'profileImageUrl', 'stageTypes', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
