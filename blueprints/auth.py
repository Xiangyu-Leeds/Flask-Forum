from flask import Blueprint, render_template

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


# /auth/login
@bp.route('/login')
def login():
    pass


@bp.route('/register')
def register():
    # return render_template("base.html")
    pass