# app/routes/home.py
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import User, db

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            phone_number=request.form.get('phone_number'),
            gmail_address=request.form.get('gmail_address'),
            post=request.form.get('Post')
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('questions.show_question', question_number=1))
    return render_template('index.html')
