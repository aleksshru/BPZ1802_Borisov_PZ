from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from data import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    url = 'https://apidata.mos.ru/v1/datasets/3402/rows/'
    url1 = 'https://apidata.mos.ru/v1/datasets/3402/count'
    api_key = '8740e91e3163075c109032ad64d8e736'
    n = 0
    k = 1
    payload = {'api_key': api_key, '$top': k, '$skip': n}
    payload1 = {'api_key': api_key}
    res = requests.get(url, params=payload)
    json = res.json()
    if 200 <= res.status_code < 300:
        count = int(requests.get(url1, params=payload1).text)
        if count != db.session.query(Article).count():
            i = 0
            json.clear()
            k = 500
            c = 500
            if count < 500:
                c = count
                k = count
            while True:
                payload = {'api_key': api_key, '$top': k, '$skip': n}
                json.extend(requests.get(url, params=payload).json())
                if c > 500:
                    c = c - 500
                    n = k
                    k = k + 500
                else:
                    break
            db.drop_all()
            db.create_all()
            for t in json:
                article = Article(num=t['Number'], title=t['Cells']['FullName'], text=t['Cells']['IsOMSprovider'])
                db.session.add(article)
                db.session.commit()
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.id).all()
    return render_template("posts.html", articles=articles)


if __name__ == '__main__':
    app.run(debug=True)

