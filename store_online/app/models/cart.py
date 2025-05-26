from app import db


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product', backref='cart_items')

    def __repr__(self):
        return f'<CartItem {self.id}>'

    def get_total_price(self):
        return self.product.price * self.quantity