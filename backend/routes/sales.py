from database import db
from models import Sale, Product, User, Region, Team



from flask import Blueprint, jsonify, request
from models import db, Sale, Product, User, Region

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify([{
        'sale_id': sale.sale_id,
        'product_name': sale.product.product_name,
        'username': sale.user.username,
        'region_name': sale.region.region_name,
        'quantity': sale.quantity,
        'total_price': sale.total_price,
        'sale_date': sale.sale_date
    } for sale in sales])

@sales_bp.route('/', methods=['POST'])
def add_sale():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    user = User.query.get(data['user_id'])
    region = Region.query.get(data['region_id'])

    if product and user and region:
        total_price = product.price * data['quantity']
        new_sale = Sale(product_id=data['product_id'], user_id=data['user_id'], region_id=data['region_id'], quantity=data['quantity'], total_price=total_price)
        db.session.add(new_sale)
        product.stock -= data['quantity']  # Update stock
        db.session.commit()
        return {"message": "Sale added successfully!"}, 201

    return {"message": "Invalid product, user, or region."}, 400
