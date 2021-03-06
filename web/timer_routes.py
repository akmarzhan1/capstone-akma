from flask import Flask, render_template, request, flash, request, redirect, url_for, Blueprint, Response
from .models import User, db, bcrypt, Timer
import json
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, timedelta
from flask_login import LoginManager
from cryptography.fernet import Fernet
from flask_wtf.csrf import CSRFProtect

# new application blueprint for routes
timer_bp = Blueprint('timer', __name__, template_folder='templates')

# deleting tasks
csrf = CSRFProtect()

#calculating the focus time
def time_calc(attempted, remaining):

    """
    Function for calculating the total focus time. 
    """

    try:
        string = attempted*60-(int(float(remaining[0]))*60+int(float(remaining[1])))
    except:
        string = 0

    if string<0:
        string = (attempted+1)*60-(int(float(remaining[0]))*60+int(float(remaining[1])))

    return string

@csrf.exempt #ajax support
@timer_bp.route("/reset_round", methods=['GET', 'POST'])
def reset_round():
    
    """
    Function for resetting the round and collecting the focus time. 
    """
        
    timer = Timer.query.filter_by(user_id=current_user.id)[-1]

    if timer.completed == False:

        time_remaining = request.get_json(force=True)['time_remaining'].split(':')
        timer.focus_time = time_calc(timer.attempted_time, time_remaining)

        timer.completed = True

        db.session.commit()

        return {}
    
    else:
        return {}


@csrf.exempt
@timer_bp.route("/switch_focus", methods=['GET', 'POST'])
def switch_focus():

    """
    Function for switching the time to focus. 
    """
    
    #switching the deep focus mode
    new_state = request.get_json(force=True)['new_state']

    user = User.query.filter_by(id=current_user.id).first()
    user.block = bool(new_state)
    
    db.session.commit()

    return redirect(url_for('routes.timer'))

@csrf.exempt
@timer_bp.route("/finish_timer", methods=['GET', 'POST'])
def finish_timer():
    
    """
    Function for finishing the timer and collecting the total focus time. 
    """

    try:
        timer = Timer.query.filter_by(user_id=current_user.id)[-1]
    except:
        return {}

    time_remaining = request.get_json(force=True)['time_remaining']
    print('yo', time_remaining)

    if timer.completed==False:

        if timer.attempted_time==0:
            db.session.delete(timer)
            db.session.commit()

        else:
            if time_remaining=='completed' or time_remaining=="00:00":
                timer.focus_time = timer.attempted_time
                print('hello', time_remaining)
            else:
                timer.focus_time = time_calc(timer.attempted_time, time_remaining)
                
            timer.completed = True

            db.session.commit()

    return {}

@csrf.exempt
@timer_bp.route("/update_timer", methods=['GET', 'POST'])
def update_timer():

    """
    Function for creating or updating a timer whenever necessary.
    """
    
    time_remaining = request.get_json(force=True)['time_remaining'].split(':')

    try:
        timer = Timer.query.filter_by(user_id=current_user.id)[-1]
    except:
        timer = None

    if timer==None or timer.completed==True:

        time_created = date.today()

        newTimer = Timer(focus_time=0, time_created=time_created, attempted_time=int(time_remaining[0]), user_id=current_user.id)

        db.session.add(newTimer)
        db.session.commit()

    else:

        timer.focus_time = time_calc(timer.attempted_time, time_remaining)
        db.session.commit()

    return {}

