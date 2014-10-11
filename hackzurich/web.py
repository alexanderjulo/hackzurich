from flask import Blueprint, render_template


bp = Blueprint('web', __name__)


@bp.route('/')
def home():
    return render_template("home.html")


def setUp(app):
    app.register_blueprint(bp)
