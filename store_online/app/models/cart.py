from app import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cart {self.id}>'
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total()
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<CartItem {self.id}>'
    
    def get_subtotal(self):
        return self.quantity * self.product.price

    def get_total_price(self):
        # Nếu sản phẩm có giảm giá, dùng giá đã giảm
        if hasattr(self.product, 'get_discounted_price'):
            return self.quantity * self.product.get_discounted_price()
        return self.get_subtotal()
    
    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict(),
            'subtotal': self.get_subtotal()
        }