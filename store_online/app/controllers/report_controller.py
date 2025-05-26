from flask import Blueprint, render_template, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app import db
from sqlalchemy import func
import csv
import io
from datetime import datetime, timedelta

report_bp = Blueprint('report', __name__)

@report_bp.route('/admin/reports')
@login_required
def admin_reports():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('home.index'))
    return render_template('admin/reports.html')

@report_bp.route('/admin/reports/top-products')
@login_required
def export_top_products():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('home.index'))
    
    # Lấy top sản phẩm bán chạy
    top_products = db.session.query(
        Product,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        Order.status == 'completed'
    ).group_by(Product.id).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(100).all()

    # Tạo file CSV trong bộ nhớ
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Viết header
    writer.writerow(['ID', 'Tên sản phẩm', 'Số lượng đã bán', 'Doanh thu', 'Giá hiện tại', 'Tồn kho'])
    
    # Viết dữ liệu
    for product, quantity, revenue in top_products:
        writer.writerow([
            product.id,
            product.name,
            quantity,
            f"{revenue:,.0f}đ",
            f"{product.price:,.0f}đ",
            product.stock
        ])
    
    # Tạo response với file CSV
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'top_products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@report_bp.route('/admin/reports/top-customers')
@login_required
def export_top_customers():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('home.index'))
    
    # Lấy top khách hàng mua nhiều
    top_customers = db.session.query(
        User,
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_amount).label('total_spent')
    ).join(Order).filter(
        Order.status == 'completed'
    ).group_by(User.id).order_by(
        func.sum(Order.total_amount).desc()
    ).limit(100).all()

    # Tạo file CSV trong bộ nhớ
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Viết header
    writer.writerow(['ID', 'Tên khách hàng', 'Email', 'Số đơn hàng', 'Tổng chi tiêu', 'Ngày tham gia'])
    
    # Viết dữ liệu
    for user, orders, spent in top_customers:
        writer.writerow([
            user.id,
            user.name,
            user.email,
            orders,
            f"{spent:,.0f}đ",
            user.created_at.strftime('%d/%m/%Y')
        ])
    
    # Tạo response với file CSV
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'top_customers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@report_bp.route('/admin/reports/sales-by-date')
@login_required
def export_sales_by_date():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('home.index'))
    
    # Lấy doanh số theo ngày
    sales_by_date = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_amount).label('total_revenue')
    ).filter(
        Order.status == 'completed'
    ).group_by(
        func.date(Order.created_at)
    ).order_by(
        func.date(Order.created_at).desc()
    ).all()

    # Tạo file CSV trong bộ nhớ
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Viết header
    writer.writerow(['Ngày', 'Số đơn hàng', 'Doanh thu'])
    
    # Viết dữ liệu
    for date, orders, revenue in sales_by_date:
        writer.writerow([
            date.strftime('%d/%m/%Y'),
            orders,
            f"{revenue:,.0f}đ"
        ])
    
    # Tạo response với file CSV
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'sales_by_date_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@report_bp.route('/admin/reports/sales')
@login_required
def sales_report():
    if not current_user.is_admin:
        return redirect(url_for('home.index'))
    
    # Lấy thời gian
    period = request.args.get('period', 'week')
    if period == 'week':
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    else:  # year
        start_date = datetime.utcnow() - timedelta(days=365)
    
    # Thống kê doanh thu theo thời gian
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('total')
    ).filter(
        Order.created_at >= start_date,
        Order.status != 'cancelled'
    ).group_by(
        func.date(Order.created_at)
    ).all()
    
    # Thống kê sản phẩm bán chạy
    top_products = db.session.query(
        Product,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(
        OrderItem, Product.id == OrderItem.product_id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Order.created_at >= start_date,
        Order.status != 'cancelled'
    ).group_by(
        Product.id
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(10).all()
    
    # Thống kê theo danh mục
    category_stats = db.session.query(
        Category,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(
        Product, Category.id == Product.category_id
    ).join(
        OrderItem, Product.id == OrderItem.product_id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Order.created_at >= start_date,
        Order.status != 'cancelled'
    ).group_by(
        Category.id
    ).all()
    
    return render_template('admin/reports/sales.html',
                         daily_sales=daily_sales,
                         top_products=top_products,
                         category_stats=category_stats,
                         period=period)

@report_bp.route('/admin/reports/inventory')
@login_required
def inventory_report():
    if not current_user.is_admin:
        return redirect(url_for('home.index'))
    
    # Sản phẩm sắp hết hàng (dưới 10 sản phẩm)
    low_stock_products = Product.query.filter(Product.stock < 10).all()
    
    # Sản phẩm không còn hàng
    out_of_stock_products = Product.query.filter(Product.stock == 0).all()
    
    # Thống kê tồn kho theo danh mục
    category_inventory = db.session.query(
        Category,
        func.count(Product.id).label('total_products'),
        func.sum(Product.stock).label('total_stock'),
        func.sum(Product.stock * Product.price).label('total_value')
    ).join(
        Product, Category.id == Product.category_id
    ).group_by(
        Category.id
    ).all()
    
    return render_template('admin/reports/inventory.html',
                         low_stock_products=low_stock_products,
                         out_of_stock_products=out_of_stock_products,
                         category_inventory=category_inventory) 