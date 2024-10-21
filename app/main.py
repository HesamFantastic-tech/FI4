# import os
# import pandas as pd
# import numpy as np
# import seaborn as sns
# from flask import Flask, render_template, request, session, redirect, url_for
# from collections import Counter
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from sqlalchemy import func
# import pymysql

# app = Flask(__name__)
# app.secret_key = 'camera20'
# pymysql.install_as_MySQLdb()

# # Fetch port and debug mode from environment variables
# port = int(os.environ.get('FLASK_PORT', 2118))  # Default to 5025 if not set
# debug_mode = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'


# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hesam:Camera20%21%21%40%40%23%23%24%24@localhost/survey_app'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# # Initialize the Database
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# # Models
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     phone_number = db.Column(db.String(20), nullable=False)
#     gmail_address = db.Column(db.String(100), nullable=False)
#     post = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     answers = db.relationship('Answer', backref='user', lazy=True)

# class Question(db.Model):
#     __tablename__ = 'questions'
#     id = db.Column(db.Integer, primary_key=True)
#     question_text = db.Column(db.Text, nullable=False)
#     answers = db.relationship('Answer', backref='question', lazy=True)

# class Answer(db.Model):
#     __tablename__ = 'answers'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
#     answer_text = db.Column(db.Text, nullable=False)
    

# # List of questions
# questions_list = [
#     "چگونه می‌توان برنامه‌ریزی منابع و فرآیندهای تولید فنی را به سطح هوشمند ارتقا داد؟",
#     "چه مراحلی برای رسیدن به یکپارچگی کامل در فرآیندهای کسب‌وکار پیشنهاد می‌شود؟",
#     "چه ابزارهایی برای بهینه‌سازی فرآیندهای چرخه عمر محصول در سطح هوشمند می‌توان به کار برد؟",
#     "چگونه می‌توان انعطاف‌پذیری تجهیزات و ماشین‌آلات را برای سازگاری با تغییرات افزایش داد؟",
#     "چه اقداماتی برای دستیابی به اتوماسیون کامل در فرآیندهای سازمانی لازم است؟",
#     "چگونه می‌توان بهره‌وری منابع را در سطح تطبیقی افزایش داد؟",
#     "چه استراتژی‌هایی برای اطمینان از امنیت شبکه‌های متصل پیشنهاد می‌شود؟",
#     "چگونه می‌توان شبکه‌های موجود را برای تغییرات آینده پیکربندی کرد؟",
#     "چه موانعی برای تبادل اطلاعات لحظه‌ای بین تجهیزات وجود دارد؟",
#     "چه مزایایی در استفاده از سیستم‌های تطبیقی در کارگاه‌ها وجود دارد؟",
#     "چگونه می‌توان سیستم‌های محاسباتی را به سطح تطبیقی ارتقا داد؟",
#     "چرا برخی سیستم‌ها قادر به پیش‌بینی انحرافات احتمالی نیستند؟",
#     "چگونه می‌توان برنامه‌های آموزشی را برای آینده‌نگری در مهارت‌ها به‌روز کرد؟",
#     "چه اقداماتی برای افزایش آگاهی مدیریت با مفاهیم جدید پیشنهاد می‌شود؟",
#     "چگونه می‌توان تعاملات تیم‌ها را به سطح یکپارچه ارتقا داد؟",
#     "چگونه می‌توان استراتژی‌های بلندمدت را برای تطابق با پیشرفت‌های فناوری به‌روز کرد؟"
# ]

# # Choices for each question
# choices_dict = {
#     1: [
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "یکپارچه‌سازی سیستم‌ها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "ارتقای سیستم‌ها با هوش مصنوعی"],
#     2: ["اتصال سیستم‌ها",
#         "یکپارچه‌سازی کامل",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "مدیریت هوشمند فرآیندها",
#         "استفاده از داده‌های تحلیلی"],
#     3: ["تحلیل داده‌ها",
#         "استفاده از ابزارهای هوشمند",
#         "بهینه‌سازی فرآیندها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "یکپارچه‌سازی فناوری"],
#     4: ["افزایش انعطاف‌پذیری",
#         "ارتقای تجهیزات",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "استفاده از فناوری‌های جدید", "مدیریت تطبیقی"],
#     5: ["اتوماسیون کامل",
#         "استفاده از روبات‌ها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "یکپارچه‌سازی فرآیندها",
#         "بهره‌وری منابع"],
#     6: ["تحلیل هوشمند منابع",
#         "بهینه‌سازی مصرف منابع",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "افزایش کارایی", "ارتقای سطح تطبیق"],
#     7: ["استراتژی‌های امنیتی",
#         "شبکه‌های هوشمند",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "پیکربندی تطبیقی",
#         "مدیریت ایمن اطلاعات"],
#     8: ["پیکربندی انعطاف‌پذیر",
#         "استفاده از داده‌ها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "تحلیل تغییرات",
#         "ارتقای فناوری"],
#     9: ["موانع فناوری",
#         "نیاز به ارتباطات هوشمند",
#         "شبکه‌های لحظه‌ای",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "مدیریت ارتباطات"],
#     10: ["کارگاه‌های هوشمند",
#         "تطبیق فناوری",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "ارتقای فرآیندها",
#         "بهینه‌سازی تولید"],
#     11: ["تطبیق محاسباتی", "افزایش دقت",
#         "پیش‌بینی انحرافات",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "استفاده از تحلیل داده"],
#     12: ["پیش‌بینی انحرافات",
#         "ارتقای سیستم‌ها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "تحلیل داده‌های هوشمند",
#         "یکپارچه‌سازی فناوری"],
#     13: ["آموزش‌های هوشمند",
#         "مهارت‌های آینده",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "برنامه‌ریزی آموزشی",
#         "تحلیل نیازهای آتی"],
#     14: ["آگاهی مدیریتی",
#         "استفاده از تحلیل داده",
#         "مدیریت تغییرات",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "ارتقای مهارت‌ها"],
#     15: ["ارتقای تعاملات تیمی",
#         "یکپارچه‌سازی تیم‌ها",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "مدیریت تیم‌ها",
#         "استفاده از فناوری هوشمند"],
#     16: ["استراتژی‌های فناوری",
#         "تطبیق با فناوری‌های جدید",
#         "برنامه‌ریزی منابع به شیوه قدیمی",
#         "استفاده از فناوری‌های جدید",
#         "ارتقای استراتژی‌ها",
#         "مدیریت تغییرات"]
# }

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         first_name = request.form.get("first_name")
#         last_name = request.form.get("last_name")
#         phone_number = request.form.get("phone_number")
#         gmail_address = request.form.get("gmail_address")
#         post = request.form.get("Post")

#         # Create a new user object
#         new_user = User(first_name=first_name, last_name=last_name, phone_number=phone_number, 
#                         gmail_address=gmail_address, post=post)

#         # Add the user to the session and commit to the database
#         db.session.add(new_user)
#         db.session.commit()

#         # Store the user_id in session for later use
#         session['user_id'] = new_user.id

#         return redirect(url_for('questions', question_number=1))
#     return render_template("index.html")



# @app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
# def questions(question_number):
#     if request.method == 'POST':
#         answer = request.form.get("choice")  # Use 'choice' to match the form

#         user_id = session.get('user_id')  # Retrieve the user ID from session

#         if answer:
#             new_answer = Answer(user_id=user_id, question_id=question_number, answer_text=answer)
#             try:
#                 db.session.add(new_answer)
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 print(f"Error: {e}")
#                 return "An error occurred while saving your answer."

#         if question_number < len(questions_list):
#             return redirect(url_for('questions', question_number=question_number + 1))
#         else:
#             return redirect(url_for('summary'))

#     current_question = questions_list[question_number - 1]
#     choices = choices_dict.get(question_number, [])

#     return render_template('questions.html', question=current_question, question_number=question_number, choices=choices)




# @app.route('/summary')
# def summary():
#     user_id = session.get('user_id')

#     # Query user answers and related questions
#     user_answers = db.session.query(Answer).filter_by(user_id=user_id).all()

#     summary_data = []

#     # Prepare data for chart generation
#     question_summary = {}
#     for answer in user_answers:
#         question = Question.query.get(answer.question_id)
        
#         if question.question_text not in question_summary:
#             question_summary[question.question_text] = {}

#         if answer.answer_text in question_summary[question.question_text]:
#             question_summary[question.question_text][answer.answer_text] += 1
#         else:
#             question_summary[question.question_text][answer.answer_text] = 1

#     for question, choices in question_summary.items():
#         summary_data.append({
#             'question': question,
#             'choices': choices
#         })

#     # Render template with data
#     return render_template('summary_with_charts.html', summary_data=summary_data)



# if __name__ == "__main__":
#     app.run(debug=debug_mode, port=2121)





# main.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config['FLASK_DEBUG'], port=app.config['FLASK_PORT'])
