# app/routes/summary.py
from flask import Blueprint, render_template, session
from app.models import Answer, Question

summary_blueprint = Blueprint('summary', __name__)

@summary_blueprint.route('/summary')
def show_summary():
    user_id = session.get('user_id')
    user_answers = Answer.query.filter_by(user_id=user_id).all()

    summary_data = {}
    for answer in user_answers:
        question = Question.query.get(answer.question_id)
        summary_data.setdefault(question.question_text, {})
        summary_data[question.question_text][answer.answer_text] = (
            summary_data[question.question_text].get(answer.answer_text, 0) + 1
        )

    return render_template('templates/summary_with_charts.html', summary_data=summary_data)
