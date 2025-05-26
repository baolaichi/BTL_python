from app import db
from datetime import datetime
import os
from config import Config
from flask import url_for

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))
    stock = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(50))
    
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_average_rating(self):
        if self.reviews.count() == 0:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / self.reviews.count(), 1)
    
    def image_url(self):
        if self.image:
            return url_for('static', filename=f'images/products/{self.image}')
        return url_for('static', filename='images/placeholder.png')