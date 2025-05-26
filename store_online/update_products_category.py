from app import create_app, db
from app.models.product import Product
from app.models.category import Category

def update_products_category():
    app = create_app()
    with app.app_context():
        # Tìm danh mục 'Điện tử'
        category = Category.query.filter_by(name='Điện tử').first()
        if not category:
            print("Không tìm thấy danh mục 'Điện tử'. Hãy chắc chắn danh mục này đã tồn tại!")
            return
        # Gán tất cả sản phẩm vào danh mục này
        products = Product.query.all()
        for p in products:
            p.category_id = category.id
        db.session.commit()
        print(f'Đã gán {len(products)} sản phẩm vào danh mục "Điện tử"!')

if __name__ == '__main__':
    update_products_category() 