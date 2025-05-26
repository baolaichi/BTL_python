from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)

    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'