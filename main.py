from flask import Flask, render_template, redirect, flash
from flask_admin import Admin
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask.globals import request
from flask.helpers import url_for
from flask_sqlalchemy.model import Model
from flask_bootstrap import Bootstrap

from course_request import ScheduleCtr

from forms import CourseInputForm, LoginForm

app = Flask(__name__)
Bootstrap(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'

db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))

class AdminModelView(ModelView):
    def is_accessible(self):
        return super().is_accessible()

admin = Admin(app, name='All-In-One University', template_mode='bootstrap3')
admin.add_view(AdminModelView(User,db.session))

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
                if cl[-1]=='exam_crash':
                    htmlFile = f"<h1>Exam crash betwen {cl[0][0]} and {cl[0][1]}</h1>"
                elif cl == []:
                    htmlFile = '<h1> No match </h1>'
               # else:
                    #for idx,cs in enumerate(cl):
                        #htmlFile = htmlFile + cs.calendarToHtml()
                        #htmlFile = htmlFile + f"<br>{idx+1}\n"
                else:
                    cl_html = [cs.calendarToHtml() for idx,cs in enumerate(cl)]
                    print(cl_html)
                    htmlFile = "<h1>Developing..</h1>"
                redirect(url_for("planner"))    
            except:
                redirect(url_for("planner"))
        else:
            flash('Invalid Input')
    return render_template("planner.html", form = form, table = htmlFile)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html",form = form)

@app.route('/gpa', methods=["GET", "POST"])
def gpa():
    return render_template("gpa.html")

@app.route('/partner', methods=["GET", "POST"])
def partner():
    return render_template("partner.html")



if __name__ == '__main__':
    app.run(debug=True)
