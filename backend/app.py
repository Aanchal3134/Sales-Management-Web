

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models

# Users Table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Products Table
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.product_name}>'

# Sales Table
class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.Date, nullable=False, default=db.func.current_date())

    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
    user = db.relationship('User', backref=db.backref('sales', lazy=True))

    def __repr__(self):
        return f'<Sale {self.sale_id}>'

# Regions Table
class Region(db.Model):
    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Region {self.region_name}>'

# Teams Table
class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    manager = db.relationship('User', backref=db.backref('teams', lazy=True))

    def __repr__(self):
        return f'<Team {self.team_name}>'

# Routes

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist


# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

# Route to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='bcrypt')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"}), 201

# Route to get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'product_name': product.product_name, 'price': product.price, 'stock': product.stock} for product in products])

# Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(product_name=data['product_name'], category=data['category'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

# Route to add a new sale
@app.route('/sales', methods=['POST'])
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
        return jsonify({"message": "Sale added successfully!"}), 201
    return jsonify({"message": "Invalid product, user or region"}), 400

# Route to get all sales
@app.route('/sales', methods=['GET'])
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


if __name__ == "__main__":
    app.run(debug=True)

