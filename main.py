import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, session, redirect, url_for
from collections import Counter
import numpy as np


app = Flask(__name__)
app.secret_key = 'camera20'

# Fetch port and debug mode from environment variables
port = int(os.environ.get('FLASK_PORT', 2120))  # Default to 5025 if not set
debug_mode = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'


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
        return redirect(url_for('questions', question_number=1))  # Start from first question
    return render_template("index.html")


@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    if request.method == 'POST':
        answer = request.form.get("answer")
        if answer:
            session[f'answer_{question_number}'] = answer
        if question_number < len(questions_list):
            return redirect(url_for('questions', question_number=question_number + 1))
        else:
            return redirect(url_for('summary'))  # Go to summary after the last question

    current_question = questions_list[question_number - 1]
    choices = choices_dict[question_number]

    return render_template('questions.html', question=current_question, question_number=question_number, choices=choices)

def generate_charts(summary_data):
    labels = [item['question'] for item in summary_data]
    sizes = [sum(item['choices'].values()) for item in summary_data]

    # Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.savefig('static/pie_chart.png')
    plt.close()

    # Bar Chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color='skyblue')
    plt.xlabel('Questions')
    plt.ylabel('Counts')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/bar_chart.png')
    plt.close()

    # Line Chart
    x = np.arange(len(summary_data))
    plt.figure(figsize=(8, 6))
    plt.plot(x, sizes, marker='o', color='green')
    plt.xlabel('Questions')
    plt.ylabel('Counts')
    plt.savefig('static/line_chart.png')
    plt.close()

# Example route to display summary page
@app.route('/summary')
def summary():
    # Simulated data (replace with actual data from your application)
    summary_data = [
        {
            'question': 'سوال ۱',
            'choices': {
                'گزینه ۱': 10,
                'گزینه ۲': 20,
                'گزینه ۳': 30,
                'گزینه ۴': 5,
                'گزینه ۵': 15,
                'گزینه ۶': 8
            }
        },
        {
            'question': 'سوال ۲',
            'choices': {
                'گزینه ۱': 15,
                'گزینه ۲': 25,
                'گزینه ۳': 10,
                'گزینه ۴': 20,
                'گزینه ۵': 5,
                'گزینه ۶': 12
            }
        },
        {
            'question': 'سوال ۳',
            'choices': {
                'گزینه ۱': 22,
                'گزینه ۲': 18,
                'گزینه ۳': 25,
                'گزینه ۴': 7,
                'گزینه ۵': 14,
                'گزینه ۶': 9
            }
        },
        {
            'question': 'سوال ۴',
            'choices': {
                'گزینه ۱': 30,
                'گزینه ۲': 12,
                'گزینه ۳': 15,
                'گزینه ۴': 8,
                'گزینه ۵': 6,
                'گزینه ۶': 11
            }
        },
        {
            'question': 'سوال ۵',
            'choices': {
                'گزینه ۱': 11,
                'گزینه ۲': 21,
                'گزینه ۳': 19,
                'گزینه ۴': 10,
                'گزینه ۵': 13,
                'گزینه ۶': 5
            }
        },
        {
            'question': 'سوال ۶',
            'choices': {
                'گزینه ۱': 9,
                'گزینه ۲': 16,
                'گزینه ۳': 22,
                'گزینه ۴': 14,
                'گزینه ۵': 7,
                'گزینه ۶': 3
            }
        },
        {
            'question': 'سوال ۷',
            'choices': {
                'گزینه ۱': 17,
                'گزینه ۲': 25,
                'گزینه ۳': 5,
                'گزینه ۴': 11,
                'گزینه ۵': 8,
                'گزینه ۶': 2
            }
        },
        {
            'question': 'سوال ۸',
            'choices': {
                'گزینه ۱': 20,
                'گزینه ۲': 10,
                'گزینه ۳': 15,
                'گزینه ۴': 12,
                'گزینه ۵': 4,
                'گزینه ۶': 18
            }
        },
        {
            'question': 'سوال ۹',
            'choices': {
                'گزینه ۱': 14,
                'گزینه ۲': 22,
                'گزینه ۳': 9,
                'گزینه ۴': 18,
                'گزینه ۵': 16,
                'گزینه ۶': 3
            }
        },
        {
            'question': 'سوال ۱۰',
            'choices': {
                'گزینه ۱': 12,
                'گزینه ۲': 20,
                'گزینه ۳': 6,
                'گزینه ۴': 14,
                'گزینه ۵': 22,
                'گزینه ۶': 8
            }
        },
        {
            'question': 'سوال ۱۱',
            'choices': {
                'گزینه ۱': 11,
                'گزینه ۲': 17,
                'گزینه ۳': 20,
                'گزینه ۴': 10,
                'گزینه ۵': 15,
                'گزینه ۶': 13
            }
        },
        {
            'question': 'سوال ۱۲',
            'choices': {
                'گزینه ۱': 24,
                'گزینه ۲': 8,
                'گزینه ۳': 15,
                'گزینه ۴': 6,
                'گزینه ۵': 10,
                'گزینه ۶': 5
            }
        },
        {
            'question': 'سوال ۱۳',
            'choices': {
                'گزینه ۱': 18,
                'گزینه ۲': 16,
                'گزینه ۳': 14,
                'گزینه ۴': 12,
                'گزینه ۵': 20,
                'گزینه ۶': 10
            }
        },
        {
            'question': 'سوال ۱۴',
            'choices': {
                'گزینه ۱': 21,
                'گزینه ۲': 11,
                'گزینه ۳': 9,
                'گزینه ۴': 5,
                'گزینه ۵': 12,
                'گزینه ۶': 7
            }
        },
        {
            'question': 'سوال ۱۵',
            'choices': {
                'گزینه ۱': 10,
                'گزینه ۲': 12,
                'گزینه ۳': 19,
                'گزینه ۴': 15,
                'گزینه ۵': 20,
                'گزینه ۶': 11
            }
        },
        {
            'question': 'سوال ۱۶',
            'choices': {
                'گزینه ۱': 18,
                'گزینه ۲': 20,
                'گزینه ۳': 15,
                'گزینه ۴': 22,
                'گزینه ۵': 7,
                'گزینه ۶': 9
            }
        }
    ]
    # Collect answers from session and count occurrences
    for i in range(1, len(questions_list) + 1):
        question_answers = session.get(f'answer_{i}', None)
        if question_answers:
            # Count choices (you need to define how to count choices)
            choice_counts = Counter(question_answers)
            summary_data.append({
                'question': questions_list[i - 1],
                'choices': dict(choice_counts)
            })

    generate_charts(summary_data)  # Generate charts based on actual answers
    return render_template('summary_with_charts.html', summary_data=summary_data)

if __name__ == "__main__":
    app.run(debug=debug_mode, port=port)