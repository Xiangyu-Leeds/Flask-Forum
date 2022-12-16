from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, g, Response
from exts import db, mail
from flask_mail import Message
from models import UserModel, EmailCaptchaModel, QuestionModel
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")

api = Api(bp)
@api.representation('text/html')  # 当要返回的数据类型是这里定义的content-type的时候，会执行这里的函数
def output_html(data, code, headers):
    """ 在representation装饰的函数中，必须放回一个Response对象 """
    resp = Response(data)
    return resp


class Register1(Resource):
    def get(self):
        # return to register
        return render_template("register.html")

api.add_resource(Register1, "/register1")


class Login1(Resource):
    def get(self):
        # return to register
        return render_template("login.html")
api.add_resource(Login1, "/login1")



def process(errors):
    string = ""
    for i in errors:
        if i != "{" or "'" or "[" or "]" or "}" or " ":
            string+=i
    string1 = ""
    print(errors[string])
    for i in errors[string]:
        if i !="[" or "]" or "'":
            string1+=i
    return string1

class Register(Resource):
    def get(self):
        return render_template("register.html")
    def post(self):
        # check whether it is correct
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            space = ""
            if request.form.get('technology') == "technology":
                space += "Technology,"
            if request.form.get('education') == "education":
                space += "Education,"
            if request.form.get('history') == "history":
                space += "History,"
            if request.form.get('game') == "game":
                space += "Game,"
            if request.form.get('culture') == "culture":
                space += "Culture,"
            if request.form.get('life') == "life":
                space += "Life,"
            if request.form.get('emo') == "emo":
                space += "Emo,"
            if request.form.get('entertainment') == "entertainment":
                space += "Entertainment,"
            space = space[0:len(space) - 1]
            avatar_path = "../static/image/uploads/1670392532.jpeg"
            user = UserModel(username=username, password=generate_password_hash(password), email=email, space=space,
                             avatar_path=avatar_path)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login1"))
        else:
            flash(process(form.errors))
            # flash(process(form.errors))
            # flash("Incorrect email or username or password format!")
            return redirect(url_for("auth.register"))
api.add_resource(Register, "/register")


class Login(Resource):
    def get(self):
        return render_template("login.html")
    def post(self):
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
                    return redirect(url_for("qa.home"))
                else:
                    flash("The account does not match the password")
                    return redirect(url_for("auth.login"))
        else:
            flash(process(form.errors))
            # flash("Incorrect email or password format!")
            return redirect(url_for("auth.login"))
api.add_resource(Login, "/login")


class Captcha(Resource):
    def get(self):
        email = request.args.get("email")
        letters = string.ascii_letters + string.digits
        captcha = "".join(random.sample(letters, 4))
        print(captcha)
        if email:
            message = Message(
                subject="Shen Sir register",
                recipients=[email],
                body=f"The CAPTCHA I gave you is：{captcha},I hope you don't tell anyone!",
                sender="1534840095@qq.com"
            )
            mail.send(message)
            captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.captcha = captcha
                captcha_model.create_time = datetime.now()
                db.session.commit()
            else:
                captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
                try:
                    db.session.add(captcha_model)
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
            # code: 200, successful, normal request
            return jsonify({"code": 200})
        else:
            # code: 400, client error
            return jsonify({"code": 400, "message": "Please pass the email first!"})
api.add_resource(Captcha, "/captcha")


class Logout(Resource):
    def get(self):
        # 清除session中所有的数据
        session.clear()
        return redirect(url_for('auth.login'))
api.add_resource(Logout, "/logout")


class Change_password(Resource):
    def get(self):
        user = UserModel.query.filter_by(id=g.user.id).first()
        return render_template("change_password.html", user=user)
api.add_resource(Change_password, "/change_password")


class New_password(Resource):
    def get(self):
        return render_template("public_question.html")
    def post(self):
        questions = QuestionModel.query.filter_by(author_id=g.user.id).order_by(db.text("-create_time")).all()
        user = UserModel.query.filter_by(id=g.user.id).first()
        user.password = generate_password_hash(request.form.get("password"))
        db.session.commit()
        new_space = ""
        list = []
        new_space = ""
        for x in user.space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("home.html", questions=questions, list=list)
api.add_resource(New_password, "/new_password")

