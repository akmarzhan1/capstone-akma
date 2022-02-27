from flask import Flask, render_template, request, flash, request, redirect, url_for, Blueprint, Response
from .models import User, db, bcrypt
import json
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_login import LoginManager
from .forms import UpdateUsernameForm, UpdateEmailForm, UpdatePasswordForm, DeleteAccountForm
from cryptography.fernet import Fernet

# new application blueprint for routes
settings_bp = Blueprint('settings', __name__, template_folder='templates')

def get_forms(request):
    return (
        UpdateUsernameForm(request.form), 
        UpdatePasswordForm(request.form), 
        UpdateEmailForm(request.form), 
        DeleteAccountForm(request.form)
    )

# settings route
@settings_bp.route("/settings", methods=['GET'])
def settings():
    
    form_update_username, form_update_password, form_update_email, form_delete_account = get_forms(request)
    if current_user and current_user.is_authenticated:
        return render_template(
            'settings.html', 
            form_update_username=form_update_username,
            form_update_password=form_update_password,
            form_update_email=form_update_email,
            form_delete_account=form_delete_account
        )
    # return user to home if not logged on
    return redirect(url_for('routes.dashboard'))

@settings_bp.route("/update_username", methods=['POST'])
def update_username():
    form_update_username, form_update_password, form_update_email, form_delete_account = get_forms(request)
        
    if current_user and current_user.is_authenticated:

        if form_update_username.validate_on_submit():
            # updating username if form validates
            user = User.query.filter_by(id=current_user.id).first()
            user.username = form_update_username.new_username.data
            db.session.add(user)
            db.session.commit()
            flash(f'Username updated to: {user.username}', 'success')
            return redirect(url_for('auth.login'))
        else:
            return render_template(
                'settings.html', 
                form_update_username=form_update_username,
                form_update_password=form_update_password,
                form_update_email=form_update_email,
                form_delete_account=form_delete_account
            )
    # return user to home if not logged on
    return redirect(url_for('settings.settings'))

@settings_bp.route("/update_email", methods=['POST'])
def update_email():
    form_update_username, form_update_password, form_update_email, form_delete_account = get_forms(request)
    
    if current_user and current_user.is_authenticated:

        if form_update_email.validate_on_submit():
            # updating email if form validates
            user = User.query.filter_by(id=current_user.id).first()
            user.email = form_update_email.new_email.data
            db.session.add(user)
            db.session.commit()
            flash(f'Email updated to: {user.email}', 'success')
            return redirect(url_for('auth.login'))
        else:
            return render_template(
                'settings.html', 
                form_update_username=form_update_username,
                form_update_password=form_update_password,
                form_update_email=form_update_email,
                form_delete_account=form_delete_account
            )
    # return user to home if not logged on
    return redirect(url_for('settings.settings'))

@settings_bp.route("/update_password", methods=['POST'])
def update_password():
    
    form_update_username, form_update_password, form_update_email, form_delete_account = get_forms(request)
    if current_user and current_user.is_authenticated:

        if form_update_password.validate_on_submit():
            # updating password if form validates
            user = User.query.filter_by(id=current_user.id).first()
            hashed_password = bcrypt.generate_password_hash(form_update_password.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            flash(f'Password updated', 'success')
            return redirect(url_for('auth.login'))
        else:
            return render_template(
                'settings.html', 
                form_update_username=form_update_username,
                form_update_password=form_update_password,
                form_update_email=form_update_email,
                form_delete_account=form_delete_account
            )
    # return user to home if not logged on
    return redirect(url_for('settings.settings'))


@settings_bp.route("/delete_account", methods=['POST'])
def delete_account():
    form_update_username, form_update_password, form_update_email, form_delete_account = get_forms(request)

    if current_user and current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()

        if user.username == form_delete_account.username.data:
            User.query.filter_by(id=current_user.id).delete()
            db.session.commit()
            flash(f'Account Deleted', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash(f'Wrong username')
            return redirect(url_for('settings.settings'))

    # return user to home if not logged on
    return redirect(url_for('settings.settings'))