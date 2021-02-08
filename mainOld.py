from flask import Flask, render_template, redirect, flash
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask.globals import request
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
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


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////account.db'

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(30))

admin = Admin(app, name='All-In-One University', template_mode='bootstrap3')

@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template("homepage.html")


@app.route('/planner', methods=["GET", "POST"])
def planner():
    form = CourseInputForm()   
    htmlFile = ''    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                codeList = []
                for key,value in form.data.items():
                    if(isinstance(value,str) and value != '' and len(value)==6):
                        codeList.append(value)
                cl = ScheduleCtr(codeList)
                htmlFile = ''
                if cl == []:
                    htmlFile = '<h1> No match </h1>'
                else:
                    for idx,cs in enumerate(cl):
                        htmlFile = htmlFile + cs.calendarToHtml()
                        htmlFile = htmlFile + f"<br>{idx+1}\n"
                redirect(url_for("planner"))    
            except:
                redirect(url_for("planner"))
        else:
            flash('Invalid Input')
    return render_template("planner.html", form = form, table = htmlFile)

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route('/gpa', methods=["GET", "POST"])
def gpa():
    return render_template("gpa.html")

@app.route('/partner', methods=["GET", "POST"])
def partner():
    return render_template("partner.html")


if __name__ == '__main__':
    app.run(debug=True)
