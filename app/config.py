# app/config.py
import os

class Config:
    SECRET_KEY = 'camera20'
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://hesam:Camera20%21%21%40%40%23%23%24%24@localhost/survey_app'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 2118))
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'