from flask import Flask, render_template, redirect, flash
from flask_admin import Admin
# from flask_login.login_manager import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_admin.contrib.sqla import ModelView
# from flask_login import UserMixin
from flask.globals import request
from flask.helpers import url_for
# from flask_sqlalchemy.model import Model
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

from course_request import ScheduleCtr
from gpa import convertgrade, GpaCalculatorForm
from forms import CourseInputForm, LoginForm
from decimal import Decimal
from database_request import *

app = Flask(__name__)
Bootstrap(app)
DBNAME = r"ASE_Project.db"

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
'''
db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class AdminModelView(ModelView):
    def is_accessible(self):
        return super().is_accessible()

admin = Admin(app, name='All-In-One University', template_mode='bootstrap3')
admin.add_view(AdminModelView(User,db.session))
'''


###############################################################################################
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    # email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errflag = False
    if form.validate_on_submit():
        conn, cursor = create_connection(DBNAME)
        matric_id = form.username.data
        password = form.password.data
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        result_dict = get_credentials(cursor, matric_id)
        print(result_dict)
        print(result_dict["password"] + "\n")
        print(password + "\n")
        if (check_password_hash(result_dict["password"], form.password.data)):
            close_connection(conn)
            return redirect(url_for('homepage2'))
        else:
            errflag = True

        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('newlogin.html', form=form, errflag=errflag)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        conn, cursor = create_connection(DBNAME)

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        matric_id = form.username.data
        save_credentials(conn, cursor, matric_id, hashed_password)

        close_connection(conn)
        return redirect(url_for('login'))
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    ###############################################################


@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template("home.html")


@app.route('/home', methods=["GET", "POST"])
def homepage2():
    return render_template("home2.html")


@app.route('/planner', methods=["GET", "POST"])
def planner():
    form = CourseInputForm()
    htmlFile = ''
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                codeList = []
                for key, value in form.data.items():
                    if (isinstance(value, str) and value != '' and len(value) == 6):
                        codeList.append(value)
                cl = ScheduleCtr(codeList)
                htmlFile = ''
                if cl[-1] == 'exam_crash':
                    htmlFile = f"<h1>Exam crash betwen {cl[0][0]} and {cl[0][1]}</h1>"
                elif cl == []:
                    htmlFile = '<h1> No match </h1>'
                else:
                    for idx,cs in enumerate(cl):
                    htmlFile = htmlFile + cs.calendarToHtml()
                    htmlFile = htmlFile + f"<br>{idx+1}\n"
                #else:
                 #   cl_html = [cs.calendarToHtml() for idx, cs in enumerate(cl)]
                  #  print(cl_html)
                   # htmlFile = "<h1>Developing..</h1>"
                redirect(url_for("planner"))
            except:
                redirect(url_for("planner"))
        else:
            flash('Invalid Input')
    return render_template("planner.html", form=form, table=htmlFile)


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     return render_template("newlogin.html",form = form)

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     form = LoginForm()
#     return render_template("register.html",form = form)

@app.route('/gpa', methods=["GET", "POST"])
def gpa():
    form = GpaCalculatorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # declare all the values
                grade = []
                credit = []
                semestergrade = 0
                currentcredit = 0
                currentgrade = 0
                semestergpa = 0
                cumulativegpa = 0

                # to retrieve all the form data from user input
                for key, value in form.data.items():
                    if (key != 'cgpa' and key != 'creditearned'):
                        if ('grade' in key):
                            if (isinstance(value, str) and value != '' and len(value) <= 2):
                                grade.append(convertgrade(value))
                            else:
                                grade.append(0)
                        if ('credit' in key):
                            if (value != '' and value != None):
                                credit.append(value)
                            else:
                                credit.append(0)
                # to get current cumulative gpa and credit earned
                cgpa = request.form.get('cgpa')
                creditearned = request.form.get('creditearned')
                # to calculate semester grade and current credit
                for x in range(len(grade)):
                    if (grade[x] != 0):  # to prevent calculating wrong invalid grade
                        semestergrade += grade[x] * credit[x]
                        currentcredit += credit[x]
                # to get current grade
                currentgrade = Decimal(cgpa) * int(creditearned)

                # to get the new semester gpa and new cumulative gpa
                semestergpa = semestergrade / currentcredit
                cumulativegpa = (Decimal(semestergrade) + currentgrade) / (int(creditearned) + currentcredit)
                # to print the gpa
                return render_template("gparesult_new.html", sgpa=semestergpa, cgpa=cumulativegpa)
            except:
                redirect(url_for("gpa"))
        else:
            flash('Please check your input and only enter valid data')
    return render_template("gpa_new.html", form=form)


@app.route('/partner', methods=["GET", "POST"])
def partner():
    return render_template("partner.html")


if __name__ == '__main__':
    app.run(debug=True)