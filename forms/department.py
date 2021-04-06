from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Departments Title', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
