from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


data = Flask(__name__)
data.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
data.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(data)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id