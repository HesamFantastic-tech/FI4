import os
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'camera20'

# List of questions
questions_list = [
    "چگونه می‌توان برنامه‌ریزی منابع و فرآیندهای تولید فنی را به سطح هوشمند ارتقا داد؟",
    "چه مراحلی برای رسیدن به یکپارچگی کامل در فرآیندهای کسب‌وکار پیشنهاد می‌شود؟",
    "چه ابزارهایی برای بهینه‌سازی فرآیندهای چرخه عمر محصول در سطح هوشمند می‌توان به کار برد؟",
    "چگونه می‌توان انعطاف‌پذیری تجهیزات و ماشین‌آلات را برای سازگاری با تغییرات افزایش داد؟",
    "چه اقداماتی برای دستیابی به اتوماسیون کامل در فرآیندهای سازمانی لازم است؟",
    "چگونه می‌توان بهره‌وری منابع را در سطح تطبیقی افزایش داد؟",
    "چه استراتژی‌هایی برای اطمینان از امنیت شبکه‌های متصل پیشنهاد می‌شود؟",
    "چگونه می‌توان شبکه‌های موجود را برای تغییرات آینده پیکربندی کرد؟",
    "چه موانعی برای تبادل اطلاعات لحظه‌ای بین تجهیزات وجود دارد؟",
    "چه مزایایی در استفاده از سیستم‌های تطبیقی در کارگاه‌ها وجود دارد؟",
    "چگونه می‌توان سیستم‌های محاسباتی را به سطح تطبیقی ارتقا داد؟",
    "چرا برخی سیستم‌ها قادر به پیش‌بینی انحرافات احتمالی نیستند؟",
    "چگونه می‌توان برنامه‌های آموزشی را برای آینده‌نگری در مهارت‌ها به‌روز کرد؟",
    "چه اقداماتی برای افزایش آگاهی مدیریت با مفاهیم جدید پیشنهاد می‌شود؟",
    "چگونه می‌توان تعاملات تیم‌ها را به سطح یکپارچه ارتقا داد؟",
    "چگونه می‌توان استراتژی‌های بلندمدت را برای تطابق با پیشرفت‌های فناوری به‌روز کرد؟"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect form data and store in session
        session['user_info'] = {
            'نام': request.form.get("first_name"),
            'نام خانوادگی': request.form.get("last_name"),
            'شماره تلفن': request.form.get("phone_number"),
            'آدرس جیمیل': request.form.get("gmail_address"),
        }
        # Redirect to the first question
        return redirect(url_for('questions', question_number=1))
    
    # For GET requests, render the form
    return render_template("index.html")

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    # Handle POST request to save the answer and move to the next question
    if request.method == 'POST':
        answer = request.form.get("answer")
        if answer:
            session[f'answer_{question_number}'] = answer
        return redirect(url_for('questions', question_number=question_number + 1))

    # If question number exceeds the number of questions, redirect to the summary page
    if question_number > len(questions_list):
        return redirect(url_for('summary'))
    
    # Get the current question
    current_question = questions_list[question_number - 1]
#     choice = {"q1":[
#         ""برنامه‌ریزي منابع‌ و فرآیندهاي تولید فنی‌ در واحدهاي جداگانه‌ بر اساس روشهاي غیر رسمی‌ و ابتکاري مدیریت‌ و اجرا می‌شوند."",
#         ""برنامه‌ریزي منابع‌ و فرآیندهاي تولید فنی‌ در واحدهاي با استفاده از فناوري عملیاتی‌ و سیستم‌هاي فناوري اطلاعات مدیریت‌ و اجرامی‌شوند."",
#         ""برنامه‌ریزي منابع‌ و فرآیندهاي تولید فنی‌ در واحدهاي با استفاده از فناوري عملیاتی‌ و سیستم‌هاي فناوري اطلاعات مدیریت‌ و اجرامی‌شوند."",
#         ""سیستم‌هاي فناوري عملیاتی‌ و فناوري اطلاعات برنامه‌ریزي منابع‌ و فرآیندهاي تولید فنی‌ که‌ به‌ صورت رسمی‌ یکپارچه‌ شده اند رامدیریت‌ می‌کنند. اما تبادل اطلاعات و داده ها از روش هاي از پیش‌ تعیین‌ شده توسط‌ انسان مدیریت‌ می‌شود."",
#         ""سیستم‌هاي فناوري عملیاتی‌ و فناوري اطلاعات برنامه‌ریزي منابع‌ و فرآیندهاي تولید فنی‌ که‌ به‌ صورت رسمی‌ یکپارچه‌ شده اند رامدیریت‌ می‌کنند. اما تبادل اطلاعات و داده ها از روش هاي از پیش‌ تعیین‌ شده توسط‌ انسان مدیریت‌ می‌شود."",
#         ""سیستم‌هاي فناوري اطلاعات و عملیاتی‌ به‌ صورت یکپارچه‌ در آمده و از طریق‌ بینش‌ حاصل‌ از تحلیل‌ دادهها فرآیندها بهینه‌ سازيمی‌شوند.""
# ],
#                "q2":[
#         ""فرآیندهای کسب و کار در واحدهای جداگانه بر اساس روشهای غیر رسمی و ابتکاری مدیریت واجرا میشوند."",
#         ""فرآ یندهای کسب و کار در واحدهای جداگانه بر اساس مجموعه ای از دستورالعملهای رسمی تعریف شده مدیریت و اجرا میشوند."",
#         ""فرآیندهای کسب و کار در واحدهای جداگانه به وسیله ی سیستمهای فناوری اطلاعا ت مدیریت و اجرا میشوند."",
#         ""سیستمهای فناوری اطلاعات فرآ یندهای کسب و کار را که به صورت رسمی متصل هستند مدیریت و اجرا میکنند. اما تبادل داده و اطلاعات بین بخشهای مختلف از طریق روشهای مشخص به وسیله ی انسان انجام میشود."",
#         ""سیستمهای فناوری اطلاعات فرآ یندهای کسب و کار را که به صورت رسمی متصل هستند مدیریت و اجرا میکنند. اما تبادل داده و اطلاعات بین بخشهای مختلف از طریق روشهای مشخص به وسیله ی رایانه انجام میشود."",
#         ""سیستمهای فناوری اطلاعا ت به صورت یکپارچه فرآ یندها را مدیریت و به وسیله ی نگرش حاصل از تحلیل داده بهینه سازی میکنند.""
# ],
#                "q3":[],
#                "q4":[],
#                "q5":[],
#                "q6":[],
#                "q7":[],
#                "q8":[],
#                "q9":[],
#                "q10":[],
#                "q11":[],
#                "q12":[],
#                "q13":[],
#                "q14":[],
#                "q15":[],
#                "q16":[]
#                }
#     for i in range(1,17)
#         for i in choice["q"]
    choices = ["0-", "1-", "2-", "3-", "4-", "5-"]  # Example choices for each question
    
    return render_template('questions.html', question=current_question, question_number=question_number, choices=choices)

@app.route("/summary")
def summary():
    # Retrieve user information from the session
    user_info = session.get('user_info', {})
    
    # Retrieve answers from the session
    answers = {f'سوال {i}': session.get(f'answer_{i}', '') for i in range(1, len(questions_list) + 1)}
    
    # Combine user info and answers
    data = {**user_info, **answers}
    
    # Convert the data to a DataFrame
    new_data_df = pd.DataFrame([data])  # Wrap data in a list to ensure it's a DataFrame

    # Path to the Excel file
    file_path = "smart_city_survey.xlsx"

    # Check if the file exists
    if not os.path.exists(file_path):
        # If it doesn't exist, create a new DataFrame with the new data
        df = new_data_df
    else:
        try:
            # Load the existing Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception as e:
            return f"Error reading Excel file: {str(e)}"

        # Use pd.concat to append the new data
        new_data_df = pd.DataFrame([data])
        df = pd.concat([df, new_data_df], ignore_index=True)

    # Save the updated DataFrame to Excel
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as e:
        return f"Error saving Excel file: {str(e)}"

    # Optionally, clear the session data
    session.pop('user_info', None)
    for i in range(1, len(questions_list) + 1):
        session.pop(f'answer_{i}', None)
    
    return render_template("summary.html", data=data, answers=answers)

if __name__ == "__main__":
    app.run(debug=True, port=5026)
