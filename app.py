from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init DB
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# Product class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    cost = db.Column(db.Float)
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, cost, price, qty):
        self.name = name
        self.description = description
        self.cost = cost
        self.price = price
        self.qty = qty

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'cost', 'price', 'qty')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    cost = request.json['cost']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, cost, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Create a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    cost = request.json['cost']
    price = request.json['price']
    qty = request.json['qty']

    product.name =name
    product.description = description
    product.cost = cost
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# Get Single Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# run server
if __name__=="__main__":
    app.run(debug=True)