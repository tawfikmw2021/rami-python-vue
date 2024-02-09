from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
from project import db

from .models import Round
@main.route('/')
def index():
    #ignored
    text = "\n".join(open("./dist/index.html").readlines())
    return render_template('index.html', test_html=text)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
