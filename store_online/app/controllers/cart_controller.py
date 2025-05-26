from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.cart import CartItem, Cart
from app.models.product import Product
from app import db

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_items = cart.items
    total = sum(item.get_total_price() for item in cart_items)
    return render_template('cart/view.html', cart_items=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash('This product is out of stock', 'danger')
        return redirect(url_for('product.detail', id=product_id))

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if cart_item:
        if cart_item.quantity >= product.stock:
            flash('Cannot add more than available stock', 'danger')
            return redirect(url_for('product.detail', id=product_id))
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} has been added to your cart!', 'success')
    return redirect(url_for('product.detail', id=product_id))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    cart = Cart.query.get_or_404(cart_item.cart_id)

    if cart.user_id != current_user.id:
        flash('You do not have permission to do that', 'danger')
        return redirect(url_for('cart.view_cart'))

    action = request.form.get('action')

    if action == 'increase':
        if cart_item.quantity >= cart_item.product.stock:
            flash('Cannot add more than available stock', 'danger')
        else:
            cart_item.quantity += 1
            db.session.commit()
            flash('Item quantity updated', 'success')
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
            flash('Item quantity updated', 'success')
        else:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Item removed from cart', 'info')
    elif action == 'remove':
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart', 'info')

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/api/update/<int:item_id>', methods=['POST'])
@login_required
def api_update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    cart = Cart.query.get_or_404(cart_item.cart_id)

    if cart.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    action = request.json.get('action')
    response_data = {'success': True}

    if action == 'increase':
        if cart_item.quantity >= cart_item.product.stock:
            response_data = {
                'success': False,
                'message': 'Cannot add more than available stock'
            }
        else:
            cart_item.quantity += 1
            db.session.commit()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
        else:
            db.session.delete(cart_item)
            db.session.commit()
            response_data['removed'] = True
    elif action == 'remove':
        db.session.delete(cart_item)
        db.session.commit()
        response_data['removed'] = True

    if response_data.get('success', False):
        cart_items = cart.items
        total = sum(item.get_total_price() for item in cart_items)
        response_data.update({
            'quantity': cart_item.quantity if not response_data.get('removed') else 0,
            'item_total': cart_item.get_total_price() if not response_data.get('removed') else 0,
            'cart_total': total,
            'cart_count': len(cart_items)
        })

    return jsonify(response_data)