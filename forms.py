from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from course_request import ScheduleCtr

class CourseInputForm(FlaskForm):
    courseCode1 = StringField('Enter course code', [validators.Length(min=6,max=6),validators.Optional()])
    courseCode2 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode3 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode4 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode5 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode6 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode7 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode8 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    courseCode9 = StringField('Enter course code', [validators.Length(max=6),validators.Optional()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username',[validators.Length(min=3, max=30)])
    password = PasswordField("Password",[
        validators.DataRequired()])
    submit = SubmitField('Login')