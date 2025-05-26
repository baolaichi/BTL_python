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
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', back_populates='product')
    ratings = db.relationship('Rating', back_populates='product', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(r.rating for r in self.ratings) / len(self.ratings)
    
    def image_url(self):
        if self.image:
            return f'/static/images/products/{self.image}'
        return '/static/images/no-image.jpg'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image': self.image_url(),
            'average_rating': self.get_average_rating(),
            'category': self.category
        }