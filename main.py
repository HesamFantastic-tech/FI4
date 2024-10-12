import os
import pandas as pd
import seaborn as sns
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
from collections import Counter
import numpy as np
import logging
import pymysql
from collections import defaultdict
import bcrypt
from datetime import timedelta
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'default_user'),
            password=os.environ.get('DB_PASSWORD', ''),
            db=os.environ.get('DB_NAME', 'FI4'),
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        logging.error(f"Database connection failed: {e}")
        return None




app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config.update(
    SESSION_COOKIE_SECURE=True,   # Only transmit cookies over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # JavaScript can't access the cookie
    SESSION_COOKIE_SAMESITE='Lax'  # Prevents CSRF by restricting cross-site access
)



@app.before_request
def make_session_permanent():
    session.permanent = True

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout to 30 minutes


# Configure logging
logging.basicConfig(level=logging.INFO)

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

@app.route('/logout')
def logout():
    session.clear()  # Clear the entire session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Gather user information from the form
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        gmail_address = request.form.get("gmail_address")
        post = request.form.get("Post")
        
        # Save the user data into the 'users' table
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (first_name, last_name, phone_number, gmail_address, post) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (first_name, last_name, phone_number, gmail_address, post))
            user_id = cursor.lastrowid  # Get the ID of the inserted user
        connection.commit()
        connection.close()

        # Store user info and user_id in session
        session['user_info'] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'gmail_address': gmail_address,
            'post': post,
            'user_id': user_id  # Store user_id for later use
        }

        return redirect(url_for('questions', question_number=1))  # Start from first question
    return render_template("index.html")


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Example usage when creating a new user:
hashed_password = hash_password('plain_text_password')


def get_user_by_credentials(username, password):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Query to find the user by username
        cursor.execute("""
            SELECT id, username, password 
            FROM users 
            WHERE username = %s
        """, (username,))
        
        user = cursor.fetchone()
    
    connection.close()
    
    # If user exists and the password matches, return the user
    if user and check_password(user['password'], password):
        return user
    return None

def check_password(stored_password, provided_password):
    # stored_password is hashed, provided_password is plain text
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if any field is missing
        if not username or not password or not email:
            flash("All fields are required.", "error")
            return redirect(url_for('register'))

        # Password validation: minimum 8 characters
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for('register'))

        # Check complexity (at least one letter, one number, and one special character)
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            flash("Password must contain at least one letter, one number, and one special character.", "error")
            return redirect(url_for('register'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Get database connection
        connection = get_db_connection()
        if not connection:
            flash("Database connection failed.", "error")
            return redirect(url_for('register'))

        try:
            with connection.cursor() as cursor:
                # Check if the username or email already exists
                cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash("Username or email already in use.", "error")
                    return redirect(url_for('register'))

                # Insert the new user into the users table
                cursor.execute(
                    "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                    (username, hashed_password, email)
                )
                connection.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('register'))

        finally:
            connection.close()

    # If GET request, render the registration form
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username or password is missing
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        # Get the database connection
        connection = get_db_connection()
        if not connection:
            flash("Database connection failed.", "error")
            return redirect(url_for('login'))

        try:
            with connection.cursor() as cursor:
                # Retrieve the user from the database
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                # Check if user exists and password matches
                if user and check_password_hash(user['password'], password):
                    session['user_info'] = {
                        'user_id': user['id'],
                        'username': user['username']
                    }
                    flash("Login successful!", "success")
                    return redirect(url_for('questions', question_number=0))
                else:
                    flash("Invalid username or password.", "error")
                    return redirect(url_for('login'))
        
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('login'))

        finally:
            # Close the connection after the operation
            connection.close()

    # If GET request, render the login page
    return render_template('login.html')



@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    # Check if user_info exists in the session
    if 'user_info' not in session:
        flash("You must be logged in to access this page", "warning")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_info']['user_id']

    # Validate question_number
    if question_number >= len(questions_list):
        flash("This question does not exist.", "error")
        return redirect(url_for('questions', question_number=0))

    question = questions_list[question_number]
    choices = choices_dict.get(question_number, ["No choices available for this question"])

    # Handle form submission
    if request.method == 'POST':
        choice = request.form['choice']
        save_response(user_id, question_number, choice)
        flash("Your response has been saved!", "success")

        # Redirect to next question or summary
        if question_number + 1 < len(questions_list):
            return redirect(url_for('questions', question_number=question_number + 1))
        else:
            return redirect(url_for('summary'))  # Redirect to summary after the last question

    # Render the question page
    return render_template('question_page.html', question=question, choices=choices)


# Helper function to save responses (you can adjust this according to your needs)
def save_response(user_id, question_number, choice):
    connection = get_db_connection()
    if not connection:
        logging.error("Database connection failed.")
        return
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO responses (user_id, question_number, choice)
            VALUES (%s, %s, %s)
        """, (user_id, question_number, choice))
    connection.commit()
    connection.close()

def calculate_average(session):
    total_value = 0
    num_valid_answers = 0
    num_questions = len(questions_list)
    
    for i in range(1, num_questions + 1):
        answer = session.get(f'answer_{i}')
        if answer and answer.isdigit():
            total_value += int(answer)
            num_valid_answers += 1

    return total_value / num_valid_answers if num_valid_answers else 0



@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.json  # Assuming data is being sent as JSON
    user_id = data['user_id']
    question_number = data['question_number']
    choice = data['choice']

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO responses (user_id, question_number, choice) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, question_number, choice))
    connection.commit()
    connection.close()

    return jsonify({"message": "Response submitted successfully"}), 201


@app.route('/get_chart_data')
def get_chart_data():
    if 'user_info' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_info']['user_id']
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT question_id, choice, COUNT(*) as count
            FROM responses
            WHERE user_id = %s
            GROUP BY question_id, choice
        """, (user_id,))
        raw_data = cursor.fetchall()
    
    connection.close()

    # Organize data in a dictionary grouped by question_id
    chart_data = defaultdict(lambda: {"choices": {}})
    
    for row in raw_data:
        question_id = row["question_id"]
        choice = row["choice"]
        count = row["count"]
        chart_data[question_id]["choices"][choice] = count
    
    # Convert the defaultdict back to a regular dict for JSON serialization
    chart_data = dict(chart_data)
    
    return jsonify(chart_data)


@app.route('/summary')
def summary():
    user_id = session['user_info']['user_id']
    
    # Fetch the user's responses and summary data
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Get user info
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()

        # Get user responses
        cursor.execute("SELECT r.question_number, r.choice, q.question_text FROM responses r JOIN questions q ON r.question_number = q.id WHERE r.user_id = %s", (user_id,))
        user_responses = cursor.fetchall()

    connection.close()

    # Prepare data for chart generation
    summary_data = []
    for response in user_responses:
        summary_data.append({
            'question': response['question_text'],
            'answer': response['choice']
        })

    return render_template('summary_with_charts.html', 
                           summary_data=summary_data, 
                           user_info=user_info)


if __name__ == "__main__":
    app.run(debug=debug_mode, port=1119)