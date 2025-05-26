from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.review import Review
from app.views.product_view import ProductForm, ReviewForm
from app import db
import os
import secrets
from PIL import Image

product_bp = Blueprint('product', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Resize ảnh
    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@product_bp.route('/')
def list_products():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')

    query = Product.query

    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    if category:
        query = query.filter_by(category=category)

    products = query.paginate(page=page, per_page=8)

    categories = db.session.query(Product.category.distinct()).all()
    categories = [c[0] for c in categories if c[0]]

    return render_template('product/list.html', products=products,
                           search_query=search_query, categories=categories)


@product_bp.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    product = Product.query.get_or_404(id)
    form = ReviewForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to login to submit a review', 'danger')
            return redirect(url_for('auth.login'))

        review = Review(
            user_id=current_user.id,
            product_id=product.id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('product.detail', id=product.id))

    reviews = product.reviews.order_by(Review.created_at.desc()).all()
    return render_template('product/detail.html', product=product,
                           form=form, reviews=reviews)


@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('home.index'))

    form = ProductForm()
    if form.validate_on_submit():
        # Xử lý upload ảnh
        image_file = None
        if form.image.data:
            image_file = save_picture(form.image.data)
        
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data,
            image=image_file
        )
        db.session.add(product)
        db.session.commit()
        flash('Product has been added!', 'success')
        return redirect(url_for('product.list_products'))

    return render_template('admin/add_product.html', title='Add Product', form=form)


@product_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('home.index'))

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # Xử lý upload ảnh
        if form.image.data:
            # Xóa ảnh cũ nếu có
            if product.image:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], product.image))
                except FileNotFoundError:
                    pass
            
            # Lưu ảnh mới
            image_file = save_picture(form.image.data)
            product.image = image_file
        
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category = form.category.data
        db.session.commit()
        flash('Product has been updated!', 'success')
        return redirect(url_for('product.detail', id=product.id))

    return render_template('admin/edit_product.html', title='Edit Product',
                           form=form, product=product)


@product_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('home.index'))

    product = Product.query.get_or_404(id)
    
    # Xóa ảnh nếu có
    if product.image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], product.image))
        except FileNotFoundError:
            pass
    
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!', 'success')
    return redirect(url_for('product.list_products'))

@product_bp.route('/admin')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)