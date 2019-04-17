from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/customer-management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db  = SQLAlchemy(app)
from app.controllers import Routes
from app.models import Tables