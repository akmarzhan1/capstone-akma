from flask import Flask, render_template, request, flash, request, redirect, url_for, Blueprint, Response
from .models import User, Category, db, bcrypt
import json
import jwt
import os
import re 
import time 
from .getdata import getTrends, create_figure
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from .mail import mail
from flask_login import LoginManager
from .forms import UpdateUsernameForm, UpdateEmailForm, SupportForm, UpdatePreferences
from flask_mail import Message
from cryptography.fernet import Fernet

# new application blueprint for routes
routes = Blueprint('routes', __name__, template_folder='templates')

# app routes
@routes.route("/about")
def about():
    return render_template('home.html')

@routes.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html')


@routes.route("/games", methods=['POST', 'GET'])
def games():
    return render_template('games.html')

@routes.route("/", methods=['POST', 'GET'])
def blank():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    return render_template('home.html')


@routes.route("/support", methods=['POST', 'GET'])
def support():
    form = SupportForm(request.form)

    if request.method == 'GET':
        if current_user and current_user.is_authenticated:
            return render_template('support.html', form=form)
        return render_template('home.html')
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            msg = Message(
            subject=form.topic.data, 
            sender=user.email, 
            recipients=[os.getenv('MAIL_USERNAME')]
            )
            msg.html = render_template("email_templates/support_email.html", username=user.username, description=form.description.data)
            mail.send(msg)
            flash('Thanks for entering in contact with our Support, we will reply soon!', 'success')
            return redirect(url_for('routes.support'))
        else:
            print("Support form errors:", form.errors.items())
            return render_template('support.html', form=form)


@routes.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@routes.route("/trend_over_time", methods=['GET', 'POST'])
def show_trends():
    if request.method == 'POST':
        kw = request.form['trend_for']
        create_figure(kw)
        return render_template("trends.html", trends=kw)
