from app import create_app, db
from app.models.event import Event

def reset_events_table():
    app = create_app()
    with app.app_context():
        # Xóa bảng events nếu tồn tại
        Event.__table__.drop(db.engine, checkfirst=True)
        
        # Tạo lại bảng events
        Event.__table__.create(db.engine)
        
        print("Đã tạo lại bảng events thành công!")

if __name__ == '__main__':
    reset_events_table() 