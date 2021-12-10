from flask import Flask, render_template, request, flash, request, redirect, url_for, Blueprint, Response
from .models import User, db, bcrypt, Todo, Timer
import json
import jwt
import os
import re 
import time 
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_login import LoginManager
from .forms import UpdateUsernameForm, UpdateEmailForm, SupportForm, UpdatePreferences
from flask_mail import Message
from cryptography.fernet import Fernet
from .forms import AddTasksForm, AddTimerForm
from datetime import date

# new application blueprint for routes
routes = Blueprint('routes', __name__, template_folder='templates')

# app routes
@routes.route("/about")
def about():
    return render_template('home.html')

@routes.route("/dashboard", methods=['POST', 'GET'])
def dashboard():

    form = AddTasksForm(request.form)
    form1 = AddTimerForm(request.form)

    today = date.today()

    if current_user and current_user.is_authenticated:
        todo = Todo.query.filter_by(
            do=False, done=False, user_id=current_user.id).all()
        do = Todo.query.filter_by(
            do=True, done=False, user_id=current_user.id).all()
        done = Todo.query.filter_by(
            do=True, done=True, user_id=current_user.id).all()
        return render_template('dashboard.html', todos=todo, dos=do, dones=done, form=form, form1=form1, date=today)
    return render_template('home.html')

# games section
@routes.route("/games", methods=['POST', 'GET'])
def games():
    form = AddTasksForm(request.form)
    form1 = AddTimerForm(request.form)
        
    timer = Timer.query.filter_by(user_id=current_user.id)[-1]

    return render_template('games.html', form=form, form1=form1, rest=timer.rest)

# window section
@routes.route("/window", methods=['POST', 'GET'])
def window():
    form = AddTasksForm(request.form)
    form1 = AddTimerForm(request.form)

    timer = Timer.query.filter_by(user_id=current_user.id)[-1]

    return render_template('window.html', form=form, form1=form1, focus=timer.focus, rest=timer.rest)


# adding the timer
@routes.route("/add_timer", methods=['POST', 'GET'])
def add_timer():

    form = AddTimerForm(request.form)

    focus = form.focus.data
    rest = form.rest.data
    time = date.today()

    newTimer = Timer(focus=focus, rest=rest, user_id=current_user.id, time=time)
    db.session.add(newTimer)
    db.session.commit()  

    return redirect(url_for('routes.window'))

# the blank page redirects to dashboard if logged in
@routes.route("/", methods=['POST', 'GET'])
def blank():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    return render_template('home.html')


@routes.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# adding tasks
@routes.route("/add", methods=['POST', 'GET'])
@login_required
def add_todo():

    form = AddTasksForm(request.form)

    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data

        # checking if all entries are not empty to only then add the task
        # I could also do this using wtforms, but I was curious how to it using normal ones
        if title != '' and description != '' and deadline != '':
            todo = Todo(title=title, description=description,
                        deadline=deadline, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash(f'You created a new task ({todo.title})!', 'success')
        else:
            flash(f"Please fill out all of the fields!", "danger")
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for("routes.dashboard"))



# moving tasks to todo
@routes.route("/todo/<int:todo_id>", methods=['POST', 'GET'])
def todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = False
    todo.done = False
    db.session.commit()
    flash(f"You have a new to-do task ({todo.title})!", "success")
    return redirect(url_for('routes.dashboard'))

# moving tasks to doing
@routes.route("/do/<int:todo_id>", methods=['POST', 'GET'])
def do(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = True
    todo.done = False
    db.session.commit()
    flash(f"You are now doing the task ({todo.title})!", "success")
    return redirect(url_for('routes.dashboard'))

# moving tasks to done
@routes.route("/done/<int:todo_id>", methods=['POST', 'GET'])
def done(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = True
    todo.done = True
    db.session.commit()
    flash(f"You have done the task ({todo.title})!", "success")
    return redirect(url_for('routes.dashboard'))

# deleting tasks
@routes.route("/delete/<int:todo_id>", methods=['POST', 'GET'])
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"You deleted the task ({todo.title})!", "danger")
    return redirect(url_for('routes.dashboard'))