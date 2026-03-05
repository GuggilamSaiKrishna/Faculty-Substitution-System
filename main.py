from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load timetable
data = pd.read_excel("timetable.xlsx")

@app.route("/")
def index():
    faculty_list = list(data["Faculty"].unique())
    days = list(data["Day"].unique())
    return render_template("index.html", faculty=faculty_list, days=days)

@app.route("/substitute", methods=["POST"])
def substitute():

    absent = request.form["faculty"]
    day = request.form["day"]
    period = int(request.form["period"])

    # faculty busy at that time
    busy = data[
        (data["Day"] == day) &
        (data["Period"] == period)
    ]["Faculty"].tolist()

    all_faculty = list(data["Faculty"].unique())

    substitute_teacher = None

    for teacher in all_faculty:
        if teacher not in busy and teacher != absent:
            substitute_teacher = teacher
            break

    return render_template(
        "result.html",
        absent=absent,
        day=day,
        period=period,
        substitute=substitute_teacher
    )

if __name__ == "__main__":
    app.run(debug=True)
