from app import db
from datetime import datetime
from flask import url_for

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    discount_percent = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    category = db.relationship('Category', back_populates='events')

    def __init__(self, title, description, image=None, start_date=None, end_date=None, status='active', discount_percent=0, category_id=None):
        self.title = title
        self.description = description
        self.image = image
        self.start_date = start_date or datetime.utcnow()
        self.end_date = end_date
        self.status = status
        self.discount_percent = discount_percent
        self.category_id = category_id

    def __repr__(self):
        return f'<Event {self.title}>'
    
    @property
    def is_active(self):
        """Kiểm tra xem sự kiện có đang diễn ra không"""
        now = datetime.utcnow()
        return (
            self.status == 'active' and
            self.start_date <= now and
            (self.end_date is None or self.end_date >= now)
        )
    
    def image_url(self):
        if self.image:
            return url_for('static', filename=f'images/events/{self.image}')
        return url_for('static', filename='images/default_event.jpg')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url(),
            'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': self.end_date.strftime('%Y-%m-%d %H:%M:%S') if self.end_date else None,
            'status': self.status,
            'discount_percent': self.discount_percent,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        } 