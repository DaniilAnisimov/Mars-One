from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    id = StringField('Team Leader id', validators=[DataRequired()])
    size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField("is job finished")
    submit = SubmitField('Submit')
