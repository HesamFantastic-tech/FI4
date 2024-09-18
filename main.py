import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, session, redirect, url_for, send_file
from datetime import datetime

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

# Choices for each question
choices_dict = {
    1: [
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "یکپارچه‌سازی سیستم‌ها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "ارتقای سیستم‌ها با هوش مصنوعی"],
    2: ["اتصال سیستم‌ها",
        "یکپارچه‌سازی کامل",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "مدیریت هوشمند فرآیندها",
        "استفاده از داده‌های تحلیلی"],
    3: ["تحلیل داده‌ها",
        "استفاده از ابزارهای هوشمند",
        "بهینه‌سازی فرآیندها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "یکپارچه‌سازی فناوری"],
    4: ["افزایش انعطاف‌پذیری",
        "ارتقای تجهیزات",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "استفاده از فناوری‌های جدید", "مدیریت تطبیقی"],
    5: ["اتوماسیون کامل",
        "استفاده از روبات‌ها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "یکپارچه‌سازی فرآیندها",
        "بهره‌وری منابع"],
    6: ["تحلیل هوشمند منابع",
        "بهینه‌سازی مصرف منابع",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "افزایش کارایی", "ارتقای سطح تطبیق"],
    7: ["استراتژی‌های امنیتی",
        "شبکه‌های هوشمند",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "پیکربندی تطبیقی",
        "مدیریت ایمن اطلاعات"],
    8: ["پیکربندی انعطاف‌پذیر",
        "استفاده از داده‌ها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "تحلیل تغییرات",
        "ارتقای فناوری"],
    9: ["موانع فناوری",
        "نیاز به ارتباطات هوشمند",
        "شبکه‌های لحظه‌ای",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "مدیریت ارتباطات"],
    10: ["کارگاه‌های هوشمند",
        "تطبیق فناوری",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "ارتقای فرآیندها",
        "بهینه‌سازی تولید"],
    11: ["تطبیق محاسباتی", "افزایش دقت",
        "پیش‌بینی انحرافات",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "استفاده از تحلیل داده"],
    12: ["پیش‌بینی انحرافات",
        "ارتقای سیستم‌ها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "تحلیل داده‌های هوشمند",
        "یکپارچه‌سازی فناوری"],
    13: ["آموزش‌های هوشمند",
        "مهارت‌های آینده",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "برنامه‌ریزی آموزشی",
        "تحلیل نیازهای آتی"],
    14: ["آگاهی مدیریتی",
        "استفاده از تحلیل داده",
        "مدیریت تغییرات",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "ارتقای مهارت‌ها"],
    15: ["ارتقای تعاملات تیمی",
        "یکپارچه‌سازی تیم‌ها",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "مدیریت تیم‌ها",
        "استفاده از فناوری هوشمند"],
    16: ["استراتژی‌های فناوری",
        "تطبیق با فناوری‌های جدید",
        "برنامه‌ریزی منابع به شیوه قدیمی",
        "استفاده از فناوری‌های جدید",
        "ارتقای استراتژی‌ها",
        "مدیریت تغییرات"]
}

# Define file paths for the charts
chart1_path = "static/chart1.png"
chart2_path = "static/chart2.png"
chart3_path = "static/chart3.png"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session['user_info'] = {
            'نام': request.form.get("first_name"),
            'نام خانوادگی': request.form.get("last_name"),
            'شماره تلفن': request.form.get("phone_number"),
            'آدرس جیمیل': request.form.get("gmail_address"),
            'سمت': request.form.get("Post")
        }
        return redirect(url_for('questions', question_number=0))
    return render_template("index.html")


@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    if request.method == 'POST':
        answer = request.form.get("answer")
        if answer:
            session[f'answer_{question_number}'] = answer
        return redirect(url_for('questions', question_number=question_number + 1))

    if question_number > len(questions_list):
        return redirect(url_for('summary'))

    current_question = questions_list[question_number - 1]
    h = "\u200c"
    choices = [f"{idx}-{option.replace(h, '')}" for idx, option in enumerate(choices_dict[question_number])]
    
    return render_template('questions.html', question=current_question, question_number=question_number, choices=choices)


@app.route("/summary_with_charts")
def summary():
    # Load survey data from Excel
    file_path = "smart_city_survey.xlsx"
    df = pd.read_excel(file_path, engine='openpyxl')

    # Create charts based on the data
    create_charts(df)

    # Retrieve user info from session
    user_info = session.get('user_info', {})
    answers = {f'سوال {i}': session.get(f'answer_{i}', '') for i in range(1, len(questions_list) + 1)}

    data = {**user_info, **answers}

    # Render summary page with the charts
    return render_template("summary_with_charts.html", data=data)


def create_charts(df):
    
    # Bar Chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, sorted_choices, color='skyblue')
    plt.title('User Choices Distribution (Bar Chart)')
    plt.savefig('static/bar_chart.png')

    # Pie Chart
    plt.figure(figsize=(8, 6))
    plt.pie(sorted_choices, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('User Choices Distribution (Pie Chart)')
    plt.savefig('static/pie_chart.png')

    # Line Chart
    plt.figure(figsize=(8, 6))
    plt.plot(labels, sorted_choices, marker='o', color='green')
    plt.title('User Choices Trend (Line Chart)')
    plt.savefig('static/line_chart.png')

    plt.show()


if __name__ == "__main__":
    app.run(debug=True, port=5004)