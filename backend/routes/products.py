from database import db
from models import Sale, Product, User, Region, Team


from flask import Blueprint, jsonify, request
from models import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'product_id': product.product_id, 'product_name': product.product_name, 'category': product.category, 'price': product.price, 'stock': product.stock} for product in products])

@products_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(product_name=data['product_name'], category=data['category'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return {"message": "Product added successfully!"}, 201
