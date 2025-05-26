from app import create_app, db
from app.models.product import Product

def reset_products_table():
    app = create_app()
    with app.app_context():
        # Xóa bảng products nếu tồn tại
        Product.__table__.drop(db.engine, checkfirst=True)
        # Tạo lại bảng products
        Product.__table__.create(db.engine)
        print("Đã tạo lại bảng products thành công!")

if __name__ == '__main__':
    reset_products_table() 