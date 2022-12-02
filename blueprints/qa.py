from flask import Blueprint, render_template, request, redirect, flash, url_for,g

from blueprints.forms import QuestionForm
from models import UserModel,Space,QuestionModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    spaces = Space.query.all()
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    return render_template("index.html",spaces = spaces,questions=questions)




@bp.route("/qa/public",methods=['GET','POST'])
@login_required
def public_question():
    # 判断是否登录，如果没有登录，跳转到登录页面
    if request.method=='GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            print(123)
            title = form.title.data
            content = form.content.data
            space = ""
            if request.form.get('technology') == "on":
                space += "technology,"
            if request.form.get('education') == "on":
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
            space = space[0:len(space) - 1]
            question = QuestionModel(title=title,content=content,author=g.user,space=space)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误")
            return redirect(url_for("qa.public_question"))

