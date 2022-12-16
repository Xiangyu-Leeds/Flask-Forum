import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel



# check the login
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message="Incorrect email format")])
    password = wtforms.StringField(validators=[length(min=5,max=20,message="Incorrect password format")])

# check the registration
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20,message="Incorrect username format")])
    email = wtforms.StringField(validators=[email(message="Incorrect email format")])
    captcha = wtforms.StringField(validators=[length(min=4, max=4, message="Incorrect captcha format")])
    password = wtforms.StringField(validators=[length(min=6,max=20,message="Incorrect password format")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # check the email exits
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model :
            raise wtforms.ValidationError("Email already exists！")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("Email verification code error!")


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])




class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])

