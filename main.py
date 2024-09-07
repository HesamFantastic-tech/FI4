from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
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

        # Load existing data or create a new DataFrame
        try:
            df = pd.read_excel("smart_city_survey.xlsx")
        except FileNotFoundError:
            df = pd.DataFrame(columns=data.keys())

        # Append the new data and save to Excel
        df = df.append(data, ignore_index=True)
        df.to_excel("smart_city_survey.xlsx", index=False)

        return "اطلاعات شما با موفقیت ثبت شد!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5007)
