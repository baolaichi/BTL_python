from app import create_app, db
from app.models.user import User

def create_admin():
    app = create_app()
    with app.app_context():
        # Kiểm tra xem đã có tài khoản admin chưa
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print('Tài khoản admin đã tồn tại!')
            return

        # Tạo tài khoản admin mới
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')  # Mật khẩu mặc định: admin123
        
        db.session.add(admin)
        db.session.commit()
        print('Đã tạo tài khoản admin thành công!')
        print('Email: admin@example.com')
        print('Mật khẩu: admin123')

if __name__ == '__main__':
    create_admin() 