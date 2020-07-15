from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    review = TextAreaField("Review", validators=[DataRequired(), Length(max=600, message = "Enter up to 600 characters")])