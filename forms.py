from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, TimeField



class CreateToDoForm(FlaskForm):
    task_name = StringField("Task", validators=[DataRequired()])
    description = StringField("Task Description", validators=[DataRequired()])
    date = DateField("Task Date", validators=[DataRequired()])
    time = TimeField("Task Time", validators=[DataRequired()])
    submit = SubmitField("Add")
