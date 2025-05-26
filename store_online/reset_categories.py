from app import create_app, db
from app.models.category import Category

def reset_categories():
    app = create_app()
    with app.app_context():
        # Xóa toàn bộ danh mục cũ
        Category.query.delete()
        db.session.commit()
        # Thêm lại các danh mục chuẩn
        categories = [
            {'name': 'Điện tử', 'description': 'Các sản phẩm điện tử, công nghệ.'},
            {'name': 'Quần áo', 'description': 'Thời trang, quần áo, phụ kiện.'},
            {'name': 'Nhà cửa & Vườn', 'description': 'Đồ gia dụng, trang trí nhà cửa, vườn.'},
            {'name': 'Sách', 'description': 'Sách, truyện, tài liệu.'},
            {'name': 'Khác', 'description': 'Danh mục khác.'},
        ]
        for cat in categories:
            db.session.add(Category(name=cat['name'], description=cat['description']))
        db.session.commit()
        print('Đã reset danh mục sản phẩm thành công!')

if __name__ == '__main__':
    reset_categories() 