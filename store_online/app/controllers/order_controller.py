from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.views.order_view import CheckoutForm
from app import db

order_bp = Blueprint('order', __name__)

# Customer routes
@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if request.method == 'POST':
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart or not cart.items:
            flash('Giỏ hàng trống', 'warning')
            return redirect(url_for('cart.view_cart'))
        
        # Tạo đơn hàng mới
        order = Order(
            user_id=current_user.id,
            total_amount=cart.get_total(),
            shipping_address=request.form.get('shipping_address'),
            payment_method=request.form.get('payment_method', 'cod')
        )
        db.session.add(order)
        
        # Chuyển sản phẩm từ giỏ hàng sang đơn hàng
        for item in cart.items:
            order_item = OrderItem(
                order=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.get_discounted_price()
            )
            db.session.add(order_item)
            
            # Cập nhật số lượng sản phẩm
            item.product.stock -= item.quantity
        
        # Xóa giỏ hàng
        db.session.delete(cart)
        db.session.commit()
        
        flash('Đặt hàng thành công!', 'success')
        return redirect(url_for('order.order_detail', order_id=order.id))
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash('Giỏ hàng trống', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    total = cart.get_total()
    return render_template('order/checkout.html', cart=cart, form=form, total=total)

@order_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order/orders.html', orders=orders)

@order_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền xem đơn hàng này', 'danger')
        return redirect(url_for('order.orders'))
    return render_template('order/order_detail.html', order=order)

# Admin routes
@order_bp.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    status = request.args.get('status')
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@order_bp.route('/admin/order/<int:order_id>')
@login_required
def admin_view_order(order_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@order_bp.route('/admin/order/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_order(order_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        order.status = request.form.get('status')
        order.shipping_address = request.form.get('shipping_address')
        db.session.commit()
        flash('Cập nhật đơn hàng thành công!', 'success')
        return redirect(url_for('order.admin_view_order', order_id=order.id))
    
    return render_template('admin/edit_order.html', order=order)

@order_bp.route('/admin/order/<int:order_id>/delete', methods=['POST'])
@login_required
def admin_delete_order(order_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Xóa đơn hàng thành công!', 'success')
    return redirect(url_for('order.admin_orders'))