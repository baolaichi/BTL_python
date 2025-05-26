from app import create_app, db
from app.models.user import User

def reset_users_table():
    app = create_app()
    with app.app_context():
        # Xóa bảng users nếu tồn tại
        User.__table__.drop(db.engine, checkfirst=True)
        # Tạo lại bảng users
        User.__table__.create(db.engine)
        print("Đã tạo lại bảng users thành công!")

if __name__ == '__main__':
    reset_users_table() 