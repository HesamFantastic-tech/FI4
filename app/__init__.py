import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ایجاد نمونه‌های دیتابیس و Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # تنظیمات دیتابیس
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hesam:Camera20%21%21%40%40%23%23%24%24@localhost/survey_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # تنظیم SECRET_KEY
    app.config['SECRET_KEY'] = 'your-unique-secret-key'  # این کلید را به یک مقدار منحصر به فرد تغییر دهید

    # مقداردهی اولیه دیتابیس و Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes import home_blueprint, questions_blueprint, summary_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(questions_blueprint)
    app.register_blueprint(summary_blueprint)

    return app
