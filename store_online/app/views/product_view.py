from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app.models.category import Category

class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired()])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    price = DecimalField('Giá', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Số lượng', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    image = FileField('Hình ảnh sản phẩm', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Lưu')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(0, 'Chọn danh mục')] + [(c.id, c.name) for c in Category.query.all()]

class ReviewForm(FlaskForm):
    rating = SelectField('Xếp hạng', choices=[
        (5, '5 sao'),
        (4, '4 sao'),
        (3, '3 sao'),
        (2, '2 sao'),
        (1, '1 sao')
    ], validators=[DataRequired()], coerce=int)
    comment = TextAreaField('Nhận xét')
    submit = SubmitField('Gửi đánh giá')