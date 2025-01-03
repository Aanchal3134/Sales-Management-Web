from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from database import db
from routes.users import users_bp
from routes.products import products_bp
from routes.sales import sales_bp
from routes.regions import regions_bp
from routes.teams import teams_bp


# Initialize the Flask app
app = Flask(__name__)

# Configure the database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app) - not to be defined again as we defined it in database . define once import multiple times accordingly



db.init_app(app)


app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(sales_bp, url_prefix="/sales")
app.register_blueprint(regions_bp, url_prefix="/regions")
app.register_blueprint(teams_bp, url_prefix="/teams")

# Explicitly using app context for table creation
def create_tables():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

# Route to initialize the database (call this manually for the first time)
@app.route('/init-db', methods=['GET'])
def init_db():
    create_tables()
    return {"message": "Tables created successfully!"}, 200


@app.route('/')
def home():
    return "Welcome to the Sales Management System!"

if __name__ == "__main__":
    app.run(debug=True)
