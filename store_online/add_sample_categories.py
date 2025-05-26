from app import create_app, db
from app.models.category import Category

def add_sample_categories():
    app = create_app()
    with app.app_context():
        categories = [
            {'name': 'Điện thoại', 'description': 'Các loại điện thoại di động, smartphone.'},
            {'name': 'Laptop', 'description': 'Máy tính xách tay các loại.'},
            {'name': 'Phụ kiện', 'description': 'Phụ kiện cho điện thoại, laptop, máy tính.'},
            {'name': 'Thời trang', 'description': 'Quần áo, giày dép, phụ kiện thời trang.'},
            {'name': 'Gia dụng', 'description': 'Đồ dùng gia đình, nhà bếp, thiết bị điện.'},
        ]
        for cat in categories:
            if not Category.query.filter_by(name=cat['name']).first():
                db.session.add(Category(name=cat['name'], description=cat['description']))
        db.session.commit()
        print('Đã thêm các danh mục mẫu thành công!')

if __name__ == '__main__':
    add_sample_categories() 