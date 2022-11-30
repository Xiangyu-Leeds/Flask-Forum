import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import UserModel




# check the login
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[length(min=5,max=20,message="密码格式错误")])

# check the registration
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20,message="用户名格式错误")])
    email = wtforms.StringField(validators=[email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[length(min=6,max=20,message="密码格式错误")])


    # check the email exits
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model :
            raise wtforms.ValidationError("Email already exists！")




