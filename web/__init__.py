from web import routes
import os
from flask import Flask, render_template, url_for, flash, redirect
from .models import db, User
from .auth import auth, login_manager
from flask_migrate import Migrate
import datetime
from .routes import routes
from .settings_routes import settings_bp
from .config import config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .timer_routes import csrf, timer_bp

login_manager.login_message_category = "info"

app = Flask(__name__)

# registering routes
app.register_blueprint(routes)
app.register_blueprint(auth)
app.register_blueprint(settings_bp)
app.register_blueprint(timer_bp)


# updating configs 
app.config.from_object(config[os.getenv('FLASK_ENV')])

migrate = Migrate()

# connecting DB, flask-migrate, login manager, and flask mail to current app
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)
csrf.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()