from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.order import Order
from app.models.product import Product
from app.models.event import Event
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bạn không có quyền truy cập trang này.', 'danger')
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Thống kê tổng quan
    total_users = User.query.filter_by(is_admin=False).count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_events = Event.query.count()
    
    # Doanh thu trong 30 ngày gần nhất
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_revenue = db.session.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.created_at >= thirty_days_ago,
        Order.status == 'completed'
    ).scalar() or 0
    
    # Đơn hàng gần đây
    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(5).all()
    
    # Sản phẩm sắp hết hàng
    low_stock_products = Product.query.filter(
        Product.stock < 10
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_events=total_events,
                         recent_revenue=recent_revenue,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)

@admin_bp.route('/customers')
@login_required
@admin_required
def list_customers():
    customers = User.query.filter_by(is_admin=False).all()
    return render_template('admin/customers.html', customers=customers)

@admin_bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_customer():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại.', 'danger')
            return redirect(url_for('admin.add_customer'))

        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại.', 'danger')
            return redirect(url_for('admin.add_customer'))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

        flash('Thêm khách hàng thành công.', 'success')
        return redirect(url_for('admin.list_customers'))

    return render_template('admin/add_customer.html')

@admin_bp.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_customer(id):
    customer = User.query.get_or_404(id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra username đã tồn tại chưa (trừ user hiện tại)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != id:
            flash('Tên đăng nhập đã tồn tại.', 'danger')
            return redirect(url_for('admin.edit_customer', id=id))

        # Kiểm tra email đã tồn tại chưa (trừ user hiện tại)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != id:
            flash('Email đã tồn tại.', 'danger')
            return redirect(url_for('admin.edit_customer', id=id))

        customer.username = username
        customer.email = email
        if password:  # Chỉ cập nhật mật khẩu nếu có nhập mới
            customer.password = generate_password_hash(password)

        db.session.commit()
        flash('Cập nhật thông tin khách hàng thành công.', 'success')
        return redirect(url_for('admin.list_customers'))

    return render_template('admin/edit_customer.html', customer=customer)

@admin_bp.route('/customers/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_customer(id):
    customer = User.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Xóa khách hàng thành công.', 'success')
    return redirect(url_for('admin.list_customers')) 