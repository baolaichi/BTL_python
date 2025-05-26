from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', choices=[
        ('', 'Select a category'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home & Garden'),
        ('books', 'Books'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Save')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '5 Stars'),
        (4, '4 Stars'),
        (3, '3 Stars'),
        (2, '2 Stars'),
        (1, '1 Star')
    ], validators=[DataRequired()], coerce=int)
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')