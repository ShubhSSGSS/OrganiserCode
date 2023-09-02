from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.dirname(__file__)}/plans.db'
app.config['SECRET_KEY'] = 'random-key-here'

database = SQLAlchemy(app)

from codeDir import routes