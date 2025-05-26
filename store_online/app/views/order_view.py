from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery')
    ], validators=[DataRequired()])
    submit = SubmitField('Place Order')