import time
from flask import Blueprint, render_template, request, redirect, flash, url_for, g, session, Response
import os
from blueprints.forms import QuestionForm, AnswerForm
from models import UserModel, Space, QuestionModel, AnswerModel, LikeModel, RelationshipModel, FavourModel
from exts import db
from decorators import login_required
from flask_restful import Api, Resource
import logging
bp = Blueprint("qa", __name__, url_prefix="/")

api = Api(bp)


@api.representation('text/html')  # 当要返回的数据类型是这里定义的content-type的时候，会执行这里的函数
def output_html(data, code, headers):
    """ 在representation装饰的函数中，必须放回一个Response对象 """
    resp = Response(data)
    return resp


class Index(Resource):
    def get(self):
        spaces = Space.query.all()
        questions = QuestionModel.query.filter_by(is_delete=False).order_by(db.text("-create_time")).all()


        return render_template("index.html", spaces=spaces, questions=questions)


api.add_resource(Index, "/")


class Home(Resource):
    @login_required
    def get(self):
        user_id = session.get("user_id")
        questions = QuestionModel.query.filter_by(author_id=user_id,is_delete=False).order_by(db.text("-create_time")).all()
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("home.html", questions=questions, list=list)


api.add_resource(Home, "/qa/home")


class Add_space(Resource):
    def get(self):
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        space2 = "Technology,Education,History,Entertainment,Life,Game,Culture,Emo"
        list = []
        list1 = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        new_space1 = ""
        for y in space2:
            if y != ",":
                new_space1 += y
            else:
                list1.append(new_space1)
                new_space1 = ""
        list1.append(new_space1)
        List = []
        for i in list1:
            if i not in list:
                List.append(i)
        return render_template("add_space.html", List=List)


api.add_resource(Add_space, "/qa/add_space")


class Add_avatar(Resource):
    def get(self):
        return render_template("add_avatar.html")


api.add_resource(Add_avatar, "/qa/add_avatar")


class Check_follow(Resource):
    def get(self):
        follow = RelationshipModel.query.filter_by(fan_id=g.user.id).all()
        list = []
        for i in follow:
            list.append(i.follow_id)
        list1 = []
        count = 0
        fan = 0
        list2 = []
        for i in list:
            list1.append(UserModel.query.filter_by(id=i).first())
            count += 1
            fans = RelationshipModel.query.filter_by(follow_id=i).all()
            for j in fans:
                fan += 1
            list2.append(fan)
            fan = 0
        return render_template("check_follow.html", list=list1, count=count, fans=list2)


api.add_resource(Check_follow, "/qa/check_follow")


class Check_fan(Resource):
    def get(self):
        fan = RelationshipModel.query.filter_by(follow_id=g.user.id).all()
        list = []
        for i in fan:
            list.append(i.fan_id)
        list1 = []
        count = 0
        follow = 0
        list2 = []
        for i in list:
            list1.append(UserModel.query.filter_by(id=i).first())
            count += 1
            follows = RelationshipModel.query.filter_by(fan_id=i).all()
            for j in follows:
                follow += 1
            list2.append(follow)
            follow = 0
        return render_template("check_fan.html", list=list1, count=count)


api.add_resource(Check_fan, "/qa/check_fan")


class Avatar(Resource):
    def get(self):
        return render_template('add_avatar.html')

    def post(self):
        print("1234")
        user_id = session.get("user_id")
        img = request.files.get('avatar_upload')  # 从post请求中获取图片数据
        suffix = '.' + img.filename.split('.')[-1]  # 获取文件后缀名
        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件路径
        photo = '/../static/image/uploads/' + str(int(time.time())) + suffix  # 拼接相对路径
        img_path = basedir + photo  # 拼接图片完整保存路径,时间戳命名文件防止重复
        img.save(img_path)  # 保存图片
        print(img_path)
        # 这些值都可直接保存到数据库中
        photo1 = photo[1:]
        g.user.avatar_path = photo1
        db.session.commit()
        questions = QuestionModel.query.filter_by(author_id=user_id,is_delete=False).order_by(db.text("-create_time")).all()
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("home.html", questions=questions, list=list)


api.add_resource(Avatar, "/qa/avatar")


class Add_space1(Resource):
    def get(self):
        return render_template("public_question.html")

    def post(self):
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        questions = QuestionModel.query.filter_by(author_id=user_id,is_delete=False).order_by(db.text("-create_time")).all()
        if request.form.get('Technology') == "on":
            user.space += ",Technology"
        if request.form.get('Education') == "on":
            user.space += ",Education"
        if request.form.get('History') == "on":
            user.space += ",History"
        if request.form.get('Game') == "on":
            user.space += ",Game"
        if request.form.get('Culture') == "on":
            user.space += ",Culture"
        if request.form.get('Life') == "on":
            user.space += ",Life"
        if request.form.get('Emo') == "on":
            user.space += ",Emo"
        if request.form.get('Entertainment') == "on":
            user.space += ",Entertainment"
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


api.add_resource(Add_space1, "/qa/add_space1")


class Public_question1(Resource):
    @login_required
    def get(self):
        # return to register
        # user = UserModel.query.order_by(db.text("-create_time")).all()
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("public_question.html", list=list)


api.add_resource(Public_question1, "/qa/public1")


class Answer1(Resource):
    @login_required
    def get(self):
        # return to register
        # user = UserModel.query.order_by(db.text("-create_time")).all()
        favour = FavourModel.query.filter_by(author_id=g.user.id).all()
        questions1 = QuestionModel.query.filter_by(is_delete=False).order_by(db.text("-create_time")).all()
        list1 = []
        for i in favour:
            list1.append(i.question_id)
        list2 = []
        for i in questions1:
            if i.id not in list1:
                list2.append(i.id)
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        List = []
        for i in list:
            questions = QuestionModel.query.filter(QuestionModel.space.contains(i)).filter_by(is_delete=False).all()
            for q in questions:
                if q not in List:
                    List.append(q)

        return render_template("answer.html", list=list, List=List, list1=list1, list2=list2)


api.add_resource(Answer1, "/qa/answer1")


class Public_question(Resource):
    @login_required
    def get(self):
        return render_template("public_question.html")

    def post(self):
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            space = ""
            if request.form.get('Technology') == "on":
                space += "Technology,"
            if request.form.get('Education') == "on":
                space += "Education,"
            if request.form.get('History') == "on":
                space += "History,"
            if request.form.get('Game') == "on":
                space += "Game,"
            if request.form.get('Culture') == "on":
                space += "Culture,"
            if request.form.get('Life') == "on":
                space += "Life,"
            if request.form.get('Emo') == "on":
                space += "Emo,"
            if request.form.get('Entertainment') == "on":
                space += "Entertainment,"

            space = space[0:len(space) - 1]
            question = QuestionModel(title=title, content=content, author=g.user, space=space,is_delete = False)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误")
            return redirect(url_for("qa.public_question"))


api.add_resource(Public_question, "/qa/public")


class Like(Resource):
    @login_required
    def get(self, answer_id, user_id, question_id):
        answer_id = answer_id
        Answer = AnswerModel.query.filter_by(id=answer_id).first()
        user_id = user_id
        Like = LikeModel.query.filter_by(answer_id=answer_id, author_id=user_id).first()
        if Like:
            LikeModel.query.filter_by(answer_id=answer_id, author_id=user_id).delete()
            Answer.total_like = Answer.total_like - 1
            db.session.commit()
            return redirect(url_for("qa.question_detail", question_id=question_id))
        else:
            like = LikeModel(answer_id=answer_id, author_id=user_id, author=g.user)
            db.session.add(like)
            Answer.total_like = Answer.total_like + 1
            db.session.commit()
            return redirect(url_for("qa.question_detail", question_id=question_id))
api.add_resource(Like, "/qa/like/<int:answer_id>,<int:user_id>,<int:question_id>")



class Question_detail(Resource):
    @login_required
    def get(self, question_id):
        Like = LikeModel.query.filter_by(author_id=g.user.id).all()
        list = []
        for i in Like:
            list.append(i.answer_id)
        question = QuestionModel.query.get(question_id)
        answers = AnswerModel.query.all()
        list1 = []
        for i in answers:
            if i.id not in list:
                list1.append(i.id)
        return render_template("detail.html", question=question, list=list, list1=list1)
api.add_resource(Question_detail, "/detail/<int:question_id>")




class Check_information(Resource):
    @login_required
    def get(self):
        user = UserModel.query.filter_by(id=request.args.get("id")).first()
        relation = RelationshipModel.query.filter_by(fan_id=g.user.id).all()
        list = []
        for i in relation:
            list.append(i.follow_id)
        users = UserModel.query.all()
        list1 = []
        for i in users:
            if i.id not in list:
                list1.append(i.id)
        return render_template("check_information.html", user=user, list=list, list1=list1)
api.add_resource(Check_information, "/qa/check_information")


class Follow(Resource):
    @login_required
    def get(self,follow_id, fan_id):
        # 判断是否登录，如果没有登录，跳转到登录页面
        follow_id = follow_id
        fan_id = fan_id
        user = UserModel.query.filter_by(id=follow_id).first()
        relationship = RelationshipModel.query.filter_by(follow_id=follow_id, fan_id=fan_id).first()
        if relationship:
            RelationshipModel.query.filter_by(follow_id=follow_id, fan_id=fan_id).delete()
            db.session.commit()
            return "已取关"
        else:
            relationship1 = RelationshipModel(follow_id=follow_id, fan_id=fan_id)
            db.session.add(relationship1)
            db.session.commit()
            return "成功关注"
api.add_resource(Follow, "/qa/follow/<int:follow_id>,<int:fan_id>")


class Every_space(Resource):
    @login_required
    def get(self,question_space):
        spaces = Space.query.all()
        questions = QuestionModel.query.filter(QuestionModel.space.contains(question_space)).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        return render_template("index.html", questions=questions, spaces=spaces)
api.add_resource(Every_space, "/every_space/<string:question_space>")


class Answer(Resource):
    @login_required
    def post(self,question_id):
        form = AnswerForm(request.form)
        if form.validate():
            content = form.content.data
            # question_id = form.question_id.data
            answer_model = AnswerModel(content=content, author=g.user, question_id=question_id, total_like=0)
            db.session.add(answer_model)
            db.session.commit()
            return redirect(url_for("qa.question_detail", question_id=question_id))
        else:
            flash("表单验证失败")
            return redirect(url_for("qa.question_detail", question_id=question_id))

api.add_resource(Answer, "/qa/answer/<int:question_id>")


class Delete(Resource):
    def get(self):
        # delete a task
        ques = QuestionModel.query.filter_by(id=request.args.get("id")).first()
        print(ques.is_delete)
        ques.is_delete = True
        ques.space = "Emo"
        print(ques.is_delete)
        print(ques.space)
        db.session.commit()
        return redirect(url_for("qa.home"))

api.add_resource(Delete, "/delete")

class Cancel(Resource):
    def get(self):
        # delete a task
        FavourModel.query.filter_by(question_id=request.args.get("id")).delete()
        db.session.commit()
        return "1"
api.add_resource(Cancel, "/cancel")


class Favour(Resource):
    def get(self):
        favour_model = FavourModel(question_id=request.args.get("id"), author_id=g.user.id)
        db.session.add(favour_model)
        db.session.commit()
        return "1"
api.add_resource(Favour, "/favour")


class Get_favour(Resource):
    def get(self):
        favour = FavourModel.query.filter_by(author_id=g.user.id).all()
        list1 = []
        list2 = []
        for i in favour:
            list1.append(i.question_id)
        for i in list1:
            list2.append(QuestionModel.query.filter_by(id=i,is_delete=False).first())
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("favour.html", questions=list2, list=list)
api.add_resource(Get_favour, "/get_favour")


class Research(Resource):
    def get(self):
        spaces = Space.query.all()
        info = request.args.get('info')
        events = QuestionModel.query.filter(QuestionModel.title.contains(info)).filter_by(is_delete=False).order_by(db.text("-create_time")).all()
        events2 = QuestionModel.query.filter(QuestionModel.content.contains(info)).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        events3 = QuestionModel.query.filter(QuestionModel.space.contains(info)).filter_by(is_delete=False).order_by(db.text("-create_time")).all()

        for event in events2:
            if event not in events:
                events.append(event)
        for event in events3:
            if event not in events:
                events.append(event)
        #         return to search
        return render_template("search.html", questions=events, spaces=spaces)

api.add_resource(Research, "/research")


class Modify(Resource):
    def get(self):
        # return to midify
        question = QuestionModel.query.filter_by(id=request.args.get("id"),is_delete=False)[0]
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        space = user.space
        new_space = ""
        list = []
        new_space = ""
        for x in space:
            if x != ",":
                new_space += x
            else:
                list.append(new_space)
                new_space = ""
        list.append(new_space)
        return render_template("modify.html", question=question, list=list)
api.add_resource(Modify, "/modify")



class Modified(Resource):
    @login_required
    def get(self):
        return redirect(url_for("qa.home"))
    def post(self):
        m = QuestionModel.query.filter_by(id=request.args.get("id"),is_delete=False).first()
        form = QuestionForm(request.form)
        # check the modification is correct
        if form.validate():
            m.title = form.title.data
            m.content = form.content.data
            space = ""
            if request.form.get('Technology') == "on":
                space += "Technology,"
            if request.form.get('Education') == "on":
                space += "Education,"
            if request.form.get('History') == "on":
                space += "History,"
            if request.form.get('Game') == "on":
                space += "Game,"
            if request.form.get('Culture') == "on":
                space += "Culture,"
            if request.form.get('Life') == "on":
                space += "Life,"
            if request.form.get('Emo') == "on":
                space += "Emo,"
            if request.form.get('Entertainment') == "on":
                space += "Entertainment,"
            space = space[0:len(space) - 1]
            m.space = space
            # commit the database
            try:
                # add the new task to database
                # commit the new database
                db.session.commit()
            except Exception as error:
                # the rollback of the database
                db.session.rollback()
            return redirect(url_for("qa.home"))

            # db.session.commit()
            # print(789)

api.add_resource(Modified, "/modified")

class Echarts(Resource):
    def get(self):
        # show these two charts
        Education = []
        Technology = []
        History = []
        Emo = []
        Life = []
        Entertainment = []
        Game = []
        Culture = []
        questions1 = QuestionModel.query.filter(QuestionModel.space.contains("Education")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question1 in questions1:
            Education.append(question1)
        #     the length of uncompleted tasks
        a = len(Education)
        questions2 = QuestionModel.query.filter(QuestionModel.space.contains("Technology")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question2 in questions2:
            Technology.append(question2)
        #     the length of uncompleted tasks
        b = len(Technology)
        questions3 = QuestionModel.query.filter(QuestionModel.space.contains("History")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question3 in questions3:
            History.append(question3)
        #     the length of uncompleted tasks
        c = len(History)
        questions4 = QuestionModel.query.filter(QuestionModel.space.contains("Emo")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question4 in questions4:
            Emo.append(question4)
        #     the length of uncompleted tasks
        d = len(Emo)
        questions5 = QuestionModel.query.filter(QuestionModel.space.contains("Life")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question5 in questions5:
            Life.append(question5)
        #     the length of uncompleted tasks
        e = len(Life)
        questions6 = QuestionModel.query.filter(QuestionModel.space.contains("Entertainment")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question6 in questions6:
            Entertainment.append(question6)
        #     the length of uncompleted tasks
        f = len(Entertainment)
        questions7 = QuestionModel.query.filter(QuestionModel.space.contains("Game")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question7 in questions7:
            Game.append(question7)
        #     the length of uncompleted tasks
        g = len(Game)
        questions8 = QuestionModel.query.filter(QuestionModel.space.contains("Culture")).filter_by(is_delete=False).order_by(
            db.text("-create_time")).all()
        for question8 in questions8:
            Culture.append(question8)
        #     the length of uncompleted tasks
        h = len(Culture)

        return render_template("echarts.html", a=a, b=b, c=c, d=d, e=e, f=f, g=g, h=h)


api.add_resource(Echarts, "/echarts")
