from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    title = StringField('Tiêu đề sự kiện', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    image = FileField('Hình ảnh', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    is_active = BooleanField('Đang hoạt động')
    submit = SubmitField('Lưu') 