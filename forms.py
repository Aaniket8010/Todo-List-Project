from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Add Task')
