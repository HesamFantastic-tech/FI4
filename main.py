import os
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'camera20'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect form data
        data = {
            'نام': request.form.get("first_name"),
            'نام خانوادگی': request.form.get("last_name"),
            'شماره تلفن': request.form.get("phone_number"),
            'آدرس جیمیل': request.form.get("gmail_address"),
            'سوال 1': request.form.get("question1"),
            'سوال 2': request.form.get("question2"),
            'سوال 3': request.form.get("question3"),
            'سوال 4': request.form.get("question4"),
            # Add more questions as needed
        }

        # Path to the Excel file
        file_path = "smart_city_survey.xlsx"

        # Check if the file exists
        if not os.path.exists(file_path):
            # Create a new DataFrame with the data
            df = pd.DataFrame(columns=data.keys())
        else:
            try:
                # Load the existing Excel file
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                return f"Error reading Excel file: {str(e)}"

        # Append the new data
        df = df.append(data, ignore_index=True)

        # Save the updated DataFrame to Excel
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
        except Exception as e:
            return f"Error saving Excel file: {str(e)}"

        return "اطلاعات شما با موفقیت ثبت شد!"
    
    # For GET requests, render the form
    return render_template("index.html")

question_list = [
    {"question": "سوال 1: زیرساخت‌های فناوری اطلاعات در صنعت شما کافی است؟", "choices": ["خیلی زیاد", "زیاد", "کم", "خیلی کم"]},
    {"question": "سوال 2: چه فناوری‌هایی در بهبود کیفیت زندگی صنعتگران موثر هستند؟", "choices": ["فناوری 1", "فناوری 2", "فناوری 3", "فناوری 4"]},
    # Add remaining 14 questions here
]

@app.route("/questions/<int:question_number>", methods=["GET", "POST"])
def questions(question_number):
    if request.method == "POST":
        # Store the answer
        answer = request.form.get("answer")
        session[f"answer_{question_number}"] = answer
        
        # Redirect to next question or summary
        if question_number < len(question_list):
            return redirect(url_for('questions', question_number=question_number + 1))
        else:
            return redirect(url_for('summary'))
    
    # Fetch the question data
    question_data = question_list[question_number - 1]  # Updated to use the renamed variable
    return render_template("question.html", question=question_data['question'], choices=question_data['choices'], question_number=question_number)


@app.route("/summary")
def summary():
    # Retrieve user information from the session
    user_info = session.get('user_info', {})
    
    # Retrieve answers from the session
    answers = {f'سوال {i}': session.get(f'answer_{i}', '') for i in range(1, len(questions) + 1)}
    
    # Combine user info and answers
    data = {**user_info, **answers}
    
    # Path to the Excel file
    file_path = "smart_city_survey.xlsx"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a new DataFrame with the data
        df = pd.DataFrame(columns=data.keys())
    else:
        try:
            # Load the existing Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception as e:
            return f"Error reading Excel file: {str(e)}"

    # Append the new data
    df = df.append(data, ignore_index=True)

    # Save the updated DataFrame to Excel
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as e:
        return f"Error saving Excel file: {str(e)}"

    # Optionally, clear the session data
    session.pop('user_info', None)
    for i in range(1, len(questions) + 1):
        session.pop(f'answer_{i}', None)
    
    return render_template("summary.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5007)