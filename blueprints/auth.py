from flask import Blueprint, render_template, request,redirect,url_for,jsonify,session,flash
from exts import db
from flask_mail import Message
from models import UserModel
import string
import random
from datetime import datetime
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


# /auth/login


@bp.route("/register1")
def register1():
    # return to register
    return render_template("register.html")

@bp.route("/login1")
def login1():
    # return to register
    return render_template("login.html")
@bp.route("/register",methods=['GET','POST'])
def register():
   #  register a account
   if request.method=="GET":
    return render_template("register.html")
   else:
       # check whether it is correct
       form = RegisterForm(request.form)
       if form.validate():
           email = form.email.data
           username = form.username.data
           password = form.password.data

           space = ""
           # print(request.form.get('technology'))
           if request.form.get('technology') =="on":
               space+="technology,"
           if request.form.get('education') =="on":
               space += "education,"
           if request.form.get('history') == "on":
               space += "history,"
           if request.form.get('game') == "on":
               space += "game,"
           if request.form.get('culture') == "on":
               space += "culture,"
           if request.form.get('life') == "on":
               space += "life,"
           if request.form.get('emo') == "on":
               space += "emo,"
           if request.form.get('entertainment') == "on":
               space += "entertainment,"
           space = space[0:len(space)-1]
           print(space)
           # print(123)
           user = UserModel( username=username, password= generate_password_hash(password),email=email,Space = space)
           try:
               db.session.add(user)
               db.session.commit()

           except Exception as error:
               db.session.rollback()
           else:
               print(123)
               return redirect(url_for("auth.login"))
       else:
           flash("Incorrect email or username or password format!")
           return redirect(url_for("auth.register"))

@bp.route("/login",methods=['GET','POST'])
def login():
    # login a account
    if request.method=='GET':
        return render_template("login.html")
    else:
        # check whether it is correct
        form = LoginForm(request.form)
        if form.validate():
            form = LoginForm(request.form)
            if form.validate():
                email = form.email.data
                password = form.password.data
                user = UserModel.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    return redirect(url_for("qa.index"))
                else:
                    flash("The email address and password do not match")
                    return redirect(url_for("auth.login"))
        else:
                flash("Incorrect email or password format!")
                return redirect(url_for("auth.login"))
