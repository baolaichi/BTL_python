from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.views.order_view import CheckoutForm
from app import db

order_bp = Blueprint('order', __name__)

# Customer routes
@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.view_cart'))

    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            flash(f'Sorry, {item.product.name} only has {item.product.stock} items left in stock', 'danger')
            return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()

    if form.validate_on_submit():
        # Create order
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address=form.shipping_address.data,
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.commit()

        # Create order items and update product stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)

            # Update product stock
            product = Product.query.get(item.product_id)
            product.stock -= item.quantity

        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('order.order_detail', order_id=order.id))

    # Pre-fill form if user has previous orders
    last_order = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).first()
    if last_order:
        form.shipping_address.data = last_order.shipping_address

    total = sum(item.get_total_price() for item in cart_items)
    return render_template('order/checkout.html', form=form, total=total)

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
    
    status = request.args.get('status', 'all')
    query = Order.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders, status=status)

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
        order.payment_method = request.form.get('payment_method')
        
        try:
            db.session.commit()
            flash('Cập nhật đơn hàng thành công', 'success')
            return redirect(url_for('order.admin_orders'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật đơn hàng', 'danger')
    
    return render_template('admin/edit_order.html', order=order)

@order_bp.route('/admin/order/<int:order_id>/delete', methods=['POST'])
@login_required
def admin_delete_order(order_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    order = Order.query.get_or_404(order_id)
    
    try:
        db.session.delete(order)
        db.session.commit()
        flash('Xóa đơn hàng thành công', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi xóa đơn hàng', 'danger')
    
    return redirect(url_for('order.admin_orders'))