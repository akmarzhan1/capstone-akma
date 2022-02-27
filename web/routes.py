from flask import Flask, render_template, request, flash, request, redirect, url_for, Blueprint, Response, jsonify
from .models import User, db, Timer, Tasks
import json
import jwt
import os
import re
import time
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_login import LoginManager
from .forms import AddToDoForm
from datetime import date, timedelta
from time import time

# new application blueprint for routes
routes = Blueprint('routes', __name__, template_folder='templates')

# app routes
@routes.route("/about")
def about():
    return render_template('home.html')

# timer route
@routes.route("/timer")
def timer():
    
    if current_user and current_user.is_authenticated:

        #checking game access (depending on the number of completed sessions and minutes)
        game_access = {}

        total_focus = 0
        completed_timers = 0

        timers = Timer.query.filter_by(
            user_id=current_user.id, completed=True).all()

        for timer in timers:
            total_focus += timer.focus_time

            if timer.attempted_time == timer.focus_time:
                completed_timers += 1

        if total_focus>=5 and completed_timers>=2:
            game1 = True
        else:
            game1 = False 

        if total_focus>=100 and completed_timers>=10:
            game2 = True
        else:
            game2= False 

        game_access = {'game1': game1, 'game2': game2}
        print(game_access)

        return render_template('timer.html', game_access=game_access)

    return redirect(url_for('routes.about'))

# tasks route
@routes.route("/tasks")
def tasks():

    form = AddToDoForm(request.form)

    if current_user and current_user.is_authenticated:
        tasks = Tasks.query.filter_by(
            user_id=current_user.id, doing=True).all()

        return render_template('tasks.html', tasks=tasks, form=form)

    return redirect(url_for('routes.about'))

#profile route
@routes.route("/profile")
def profile():

    if current_user and current_user.is_authenticated:

        #calculating various stats and returning for the graph
        total_focus = 0
        today_focus = 0
        completed_timers = 0

        timers = Timer.query.filter_by(
            user_id=current_user.id, completed=True).all()
        tasks = Tasks.query.filter_by(
            user_id=current_user.id, doing=False).all()

        time = datetime.strptime('00:00', '%H:%M').time()
        today = datetime.combine(date.today(), time)
        today_timers = Timer.query.filter(and_(
            Timer.user_id == current_user.id, Timer.completed == True, Timer.time_created >= today)).all()
        today_tasks = Tasks.query.filter(and_(
            Tasks.user_id == current_user.id, Tasks.doing == False, Tasks.time_created >= today)).all()

        for timer in timers:
            total_focus += timer.focus_time

            if timer.attempted_time == timer.focus_time:
                completed_timers += 1

        for timer in today_timers:
            today_focus += timer.focus_time

        total_sessions = len(timers)
        total_tasks = len(tasks)
        today_tasks = len(today_tasks)

        if total_sessions==0:
            completed_percentage = 0
        else:
            completed_percentage = int((completed_timers/total_sessions)*100)

        profile_data = {'total_focus': total_focus//60, 'today_focus': today_focus//60,
                        'total_tasks': total_tasks, 'today_tasks': today_tasks,
                        'total_sessions': total_sessions, 'completed_percentage': completed_percentage}

        # graph part
        timer_graph = []
        task_graph = []
        days = []

        for t in range(7):
            curr_day = today-timedelta(days=t)
            next_day = curr_day+timedelta(days=1)
            curr_focus = 0

            curr_timers = Timer.query.filter(and_(
            Timer.user_id == current_user.id, Timer.completed == True, Timer.time_created >= curr_day, Timer.time_created < next_day)).all()
            
            curr_tasks = Tasks.query.filter(and_(
            Tasks.user_id == current_user.id, Tasks.doing == False, Tasks.time_created >= curr_day, Tasks.time_created < next_day)).all()

            for timer in curr_timers:
                curr_focus += timer.focus_time

            task_graph.append(len(curr_tasks))
            timer_graph.append(curr_focus//60)
            days.append(curr_day.strftime("%m/%d"))
        
        for item in [timer_graph, task_graph, days]:
            item.reverse()

        week = "{},{},{},{},{},{},{}"
        labels = week.format(*days)
        
        return render_template('profile.html', profile_data=profile_data, labels=labels, tasks=task_graph, timers=timer_graph)

    return redirect(url_for('routes.about'))

# blank route
@routes.route("/", methods=['POST', 'GET'])
def blank():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('routes.tasks'))
    return render_template('home.html')

# add tasks 
@routes.route("/add_task", methods=['POST', 'GET'])
@login_required
def add_task():

    form = AddToDoForm(request.form)

    if form.validate_on_submit():

        title = form.title.data
        time_created = date.today()

        # checking if all entries are not empty to only then add the task
        # I could also do this using wtforms, but I was curious how to it using normal ones
        if title != '':
            task = Tasks(title=title, time_created=time_created,
                         user_id=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash(f'You created a new task ({task.title})!', 'success')
        else:
            flash(f"Please fill out all of the fields!", "danger")

        return redirect(url_for('routes.tasks'))
    return redirect(url_for("routes.tasks"))


# delete tasks in the bucket
@routes.route("/delete_all", methods=['POST', 'GET'])
def delete_all():
    tasks = Tasks.query.filter_by(user_id=current_user.id, doing=True)

    for task in tasks:
        db.session.delete(task)
        db.session.commit()

    flash(f"You deleted all tasks!", "danger")
    return redirect(url_for('routes.tasks'))

# complete tasks
@routes.route("/complete/<int:task_id>", methods=['POST', 'GET'])
def complete(task_id):
    task = Tasks.query.get_or_404(task_id)
    task.time_completed = date.today()
    task.doing = False
    db.session.commit()
    flash(f"You completed the task ({task.title})!", "success")
    return redirect(url_for('routes.tasks'))