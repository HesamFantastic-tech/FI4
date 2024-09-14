import os
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'camera20'

# List of questions
questions_list = [
    "What is your name?",
    "What is your favorite color?",
    "What is your age?",
    # Add more questions as needed...
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
    choices = ["Option 1", "Option 2", "Option 3", "Option 4"]  # Example choices for each question
    
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
    app.run(debug=True, port=5022)
