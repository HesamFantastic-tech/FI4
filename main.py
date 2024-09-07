import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

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

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5011)
