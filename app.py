from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api,Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price


    def __repr__(self):
        return self.name


with app.app_context():
    db.create_all()

    #Item.query.filter_by(id=19).delete()
    db.session.commit()

    articles = Item.query.all()
    print(articles)


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data=items)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price)
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']

        item = Item(name=name, weight=weight, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)