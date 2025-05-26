from app import create_app, db
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.category import Category
from app.models.event import Event
from app.models.review import Review

def reset_tables():
    app = create_app()
    with app.app_context():
        # Xóa các bảng theo thứ tự để tránh lỗi foreign key
        tables = [
            CartItem, Cart,
            OrderItem, Order,
            Review,
            Product,
            Category,
            Event,
            User
        ]
        
        for table in tables:
            table.__table__.drop(db.engine, checkfirst=True)
            print(f"Đã xóa bảng {table.__tablename__}")
        
        # Tạo lại các bảng theo thứ tự ngược lại
        for table in reversed(tables):
            table.__table__.create(db.engine)
            print(f"Đã tạo lại bảng {table.__tablename__}")
        
        print("\nĐã reset tất cả các bảng thành công!")

if __name__ == '__main__':
    reset_tables() 