from app import db
from datetime import datetime
import os
from config import Config
from flask import url_for

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', back_populates='products')
    cart_items = db.relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', back_populates='product', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='product', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', back_populates='product', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_discounted_price(self):
        """Lấy giá sau khi áp dụng giảm giá từ sự kiện"""
        if self.category and self.category.events:
            active_event = next(
                (event for event in self.category.events if event.is_active),
                None
            )
            if active_event and active_event.discount_percent > 0:
                return self.price * (1 - active_event.discount_percent / 100)
        return self.price
    
    def get_average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def image_url(self):
        if self.image:
            return url_for('static', filename=f'images/products/{self.image}')
        return url_for('static', filename='images/default_product.jpg')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'discounted_price': self.get_discounted_price(),
            'stock': self.stock,
            'image_url': self.image_url(),
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'average_rating': self.get_average_rating()
        }