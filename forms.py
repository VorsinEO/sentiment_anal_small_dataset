from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    review = TextAreaField("Review", validators=[DataRequired(), Length(max=2000, message = "Enter up to 2000 characters")])