from flask import Flask ,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)



@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # Bind g to a variable called user whose value is the variable user

            g.user = user
        except:
            g.user =None

#The request is coming -> before_request -> view function -> Template returned from view function -> context_processor

@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run()