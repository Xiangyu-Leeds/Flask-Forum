from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    space = db.Column(db.String(200), nullable=False)
    avatar_path = db.Column(db.String(200), nullable=False)
    jointime = db.Column(db.DateTime, default=datetime.now)


class Space(db.Model):
    __tablename__ = "space"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Space = db.Column(db.String(200), nullable=False)


# the email database
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable =False,unique=True)
    captcha = db.Column(db.String(10),nullable = False)
    create_time = db.Column(db.DateTime,default=datetime.now)

class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text,nullable = False)
    space = db.Column(db.String(200),nullable = False)
    is_delete = db.Column(db.Boolean,nullable = False, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    author = db.relationship("UserModel",backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable = False)
    total_like = db.Column(db.Integer)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel",backref=db.backref("answers",order_by = create_time.desc()))
    author = db.relationship("UserModel",backref="answers")

class LikeModel(db.Model):
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answer_id = db.Column(db.Integer,db.ForeignKey("answer.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)
    answer = db.relationship("AnswerModel",backref=db.backref("likes",order_by = create_time.desc()))
    author = db.relationship("UserModel",backref="likes")

class RelationshipModel(db.Model):
    __tablename__ = "relationship"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follow_id = db.Column(db.Integer)
    fan_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)
    author = db.relationship("UserModel",backref="relationships")

class FavourModel(db.Model):
    __tablename__ = "favour"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship("QuestionModel", backref=db.backref("favours", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="favours")