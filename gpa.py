from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from forms import CourseInputForm, LoginForm

class GpaCalculatorForm(FlaskForm):

   cgpa = StringField('Enter cumulative GPA', [validators.Length(min=1,max=5),validators.Optional()])
   creditearned = StringField('Enter total credits earned', [validators.Length(min=1,max=2),validators.Optional()])

   grade1 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit1 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade2 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit2 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade3 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit3 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade4 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit4 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])
   
   grade5 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit5 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade6 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit6 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade7 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit7 = IntegerField('Enter course credit', [validators.NumberRange(min=1,max=3),validators.Optional()])

   grade8 = StringField('Enter course grade', [validators.Length(max=1),validators.Optional()])
   credit8 = IntegerField('Enter course cocreditde', [validators.NumberRange(min=1,max=3),validators.Optional()])

   submit = SubmitField('Submit')

def convertgrade(i):
      switcher={
       'A+': 5,
       'a+': 5,
       'A': 5,
       'a': 5,
       'A-': 4.5,
       'a-': 4.5,
       'B+': 4,
       'b+': 4,
       'B': 3.5,
       'b': 3.5,
       'B-': 3,
       'b-': 3,
       'C+': 2.5,
       'c+': 2.5,
       'C': 1.5,
       'c': 1.5,
       'D': 1,
       'd': 1,
       'F': 0,
       'f': 0
      }
      return switcher.get(i,0)

class LoginForm(FlaskForm):
   username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   password = PasswordField('Password', validators=[DataRequired()])
   submit = SubmitField('Login')