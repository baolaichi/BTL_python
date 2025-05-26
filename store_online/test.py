from app import create_app
from app.models.user import User
from app import db

app = create_app()
with app.app_context():
    # Tạo user admin
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")