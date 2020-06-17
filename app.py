import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token


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
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def welcome():
    with open('data.json', 'r') as json_file:
        emp_data = json.loads(json_file.read())

    print(emp_data)
    return jsonify(emp_data[1])


@app.route('/enter_employers', methods=['POST'])
def form_to_json():
    data = request.form.to_dict(flat=False)
    with open('data.json', 'r') as json_file:
        y = json.load(json_file)
        y.append(data)

    with open('data.json', 'w') as f:
        json.dump(y, f, indent=4)
    return jsonify(y[1])


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        createdBy = request.form['createdBy']
        createdAt = request.form['createdAt']
        version = request.form['version']
        lastModifiedBy = request.form['lastModifiedBy']
        lastModifiedAt = request.form['lastModifiedAt']
        id = request.form['id']
        systemId = request.form['systemId']
        firstName = request.form['firstName']
        middleName = request.form['middleName']
        lastName = request.form['lastName']
        fullName = request.form['fullName']
        fatherName = request.form['fatherName']
        contact = request.form['contact']
        secondaryContact = request.form['secondaryContact']
        gender = request.form['gender']
        imageId = request.form['imageId']
        address = request.form['address']
        flatNo = request.form['flatNo']
        landmark = request.form['landmark']
        city = request.form['city']
        locality = request.form['locality']
        district = request.form['district']
        state = request.form['state']
        stateCode = request.form['stateCode']
        region = request.form['region']
        country = request.form['country']
        pincode = request.form['pincode']
        pincodeType = request.form['pincodeType']
        dob = request.form['dob']
        location = request.form['location']
        username = request.form['username']
        role = request.form['role']
        status = request.form['status']
        qualification = request.form['qualification']
        language = request.form['language']
        experience = request.form['experience']
        gstin = request.form['gstin']
        lastPasswordResetAt = request.form['lastPasswordResetAt']
        profileImageUrl = request.form['profileImageUrl']
        stageTypes = request.form['stageTypes']
        password = request.form['password']
        user = User(createdBy=createdBy, createdAt=createdAt, version=version, lastModifiedBy=lastModifiedBy, lastModifiedAt=lastModifiedAt, id=id, systemId=systemId, firstName=firstName, middleName=middleName, lastName=lastName, fullName=fullName, fatherName=fatherName, contact=contact, secondaryContact=secondaryContact, email=email, gender=gender, imageId=imageId, address=address, flatNo=flatNo, landmark=landmark, city=city, locality=locality, district=district, state=state, stateCode=stateCode, region=region, country=country, pincode=pincode, pincodeType=pincodeType, dob=dob, location=location, username=username, role=role, status=status, qualification=qualification, language=language, experience=experience, gstin=gstin, lastPasswordResetAt=lastPasswordResetAt, profileImageUrl=profileImageUrl, stageTypes=stageTypes, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email).first()
    if test:
        access_token = create_access_token(identity=email)
        message = "Login succeeded!"
        with open('data.json', 'r') as json_file:
            emp_data = json.loads(json_file.read())
        dictionary = {'success':True, 'message': message, 'title': None,'object':emp_data, 'authToken': access_token}
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('createdBy', 'createdAt', 'version', 'lastModifiedBy', 'lastModifiedAt', 'id', 'systemId', 'firstName', 'middleName', 'lastName', 'fullName', 'fatherName', 'contact', 'secondaryContact', 'email', 'gender', 'imageId', 'address', 'flatNo', 'landmark', 'city', 'locality', 'district', 'state', 'stateCode', 'region', 'country', 'pincode', 'pincodeType', 'dob', 'location', 'username', 'role', 'status', 'qualification', 'language', 'experience', 'gstin', 'lastPasswordResetAt', 'profileImageUrl', 'stageTypes', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
