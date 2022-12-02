from flask import Blueprint, render_template, request,redirect,url_for,jsonify,session,flash
from exts import db,mail
from flask_mail import Message
from models import UserModel,EmailCaptchaModel
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
           if request.form.get('technology') =="technology":
               space+="technology,"
           if request.form.get('education') =="education":
               space += "education,"
           if request.form.get('history') == "history":
               space += "history,"
           if request.form.get('game') == "game":
               space += "game,"
           if request.form.get('culture') == "culture":
               space += "culture,"
           if request.form.get('life') == "life":
               space += "life,"
           if request.form.get('emo') == "emo":
               space += "emo,"
           if request.form.get('entertainment') == "entertainment":
               space += "entertainment,"
           space = space[0:len(space)-1]
           # print(123)
           user = UserModel( username=username, password= generate_password_hash(password),email=email,Space = space)
           try:
               db.session.add(user)
               db.session.commit()

           except Exception as error:
               db.session.rollback()
           else:
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

@bp.route("/captcha",methods=['GET'])
def get_captcha():
    # GET,POST
    email = request.args.get("email")
    letters = string.ascii_letters+string.digits
    captcha = "".join(random.sample(letters,4))
    print(captcha)
    if email:
        message = Message(
            subject="Shen Sir register",
            recipients = [email],
            body=f"The CAPTCHA I gave you is：{captcha},I hope you don't tell anyone!",
            sender = "1534840095@qq.com"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model =EmailCaptchaModel(email=email,captcha=captcha)
            try:
                db.session.add(captcha_model)
                db.session.commit()
            except Exception as error:
                db.session.rollback()
        # code: 200, successful, normal request
        return jsonify({"code":200})
    else:
        # code: 400, client error
        return jsonify({"code":400,"message":"Please pass the email first!"})

@bp.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('auth.login'))

# memcached/redis/数据库中