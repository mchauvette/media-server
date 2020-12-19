#
#  Taken from the tutorial at: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
#
from flask import Blueprint, render_template, send_file
from flask_login import login_required, current_user
from . import db
import os
from .media import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
