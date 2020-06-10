from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'employees.db')


db = SQLAlchemy(app)


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
    employee1 = MockDB(createdBy = "admin",
                       createdAt = 1580757593333,
                       version = 0,
                       lastModifiedBy = "admin",
                       lastModifiedAt=1580757593333,
                       firstName="PARAS LAMBA")

    db.session.add(employee1)

    test_user = User(first_name='Srishti',
                     last_name='Gupta',
                     email='srishtigupta0605@gmail.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class MockDB(db.Model):
    __tablename__ = 'employees'
    createdBy = Column(String)
    createdAt = Column(Integer)
    version = Column(Integer)
    lastModifiedBy = Column(String)
    lastModifiedAt = Column(Integer)
    firstName = Column(String,primary_key=True)


if __name__ == '__main__':
    app.run()
