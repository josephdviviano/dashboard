from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, LOGSERVER
from flask_login import LoginManager
import os
app = Flask(__name__)
app.config.from_object('config')

#from app.database import db_session
db = SQLAlchemy(app)
lm = LoginManager(app)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler, SocketHandler, DEFAULT_TCP_LOGGING_PORT
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                                'no-reply@kimellab.ca',
                                ADMINS,
                                'Dashboard failure',
                                credentials)
    base_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.realpath(os.path.join(base_dir, '..'))

    file_handler = RotatingFileHandler(os.path.join(base_dir,
                                                    'logs/dashboard.log'),
                                       'a',
                                       1 * 1024 * 1024,
                                       10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    logserver_handler = SocketHandler(LOGSERVER, DEFAULT_TCP_LOGGING_PORT)

    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    logserver_handler.setLevel(logging.DEBUG)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    # app.logger.addHandler(file_handler)
    app.logger.addHandler(logserver_handler)
    app.logger.info('Dashboard startup')
else:
    app.config['SQLALCHEMY_ECHO'] = True

from dashboard import views, models
