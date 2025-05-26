from flask import Blueprint, render_template
from app.models.event import Event
from app.models.product import Product
from datetime import datetime

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Lấy danh sách sự kiện đang hoạt động
    events = Event.query.filter(
        Event.is_active == True,
        Event.start_date <= datetime.utcnow(),
        Event.end_date >= datetime.utcnow()
    ).order_by(Event.start_date.desc()).all()
    
    # Lấy danh sách sản phẩm nổi bật (4 sản phẩm mới nhất)
    featured_products = Product.query.order_by(Product.id.desc()).limit(4).all()
    
    return render_template('home.html', events=events, featured_products=featured_products)

@home_bp.route('/about')
def about():
    return render_template('about.html')