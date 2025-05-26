from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired

class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Địa chỉ giao hàng', validators=[DataRequired()])
    payment_method = RadioField('Phương thức thanh toán', choices=[
        ('credit_card', 'Thẻ tín dụng'),
        ('paypal', 'PayPal'),
        ('cod', 'Thanh toán khi nhận hàng')
    ], validators=[DataRequired()])
    submit = SubmitField('Đặt hàng')