from flask import Blueprint, render_template
from app.models.product import Product

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    featured_products = Product.query.order_by(Product.id.desc()).limit(4).all()
    return render_template('home.html', featured_products=featured_products)

@home_bp.route('/about')
def about():
    return render_template('about.html')