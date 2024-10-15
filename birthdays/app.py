import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

MONTH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MONTH_DAY = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" :
        if not request.form.get("name") or not request.form.get("month") or not request.form.get("day"):
            return render_template("failure.html")
        else:
            # Check if the month and date are valid
            if int(request.form.get("month")) >= 1 and int(request.form.get("month")) <= 12 and int(request.form.get("day")) >= 1 and int(request.form.get("day")) <= 32:
                # Declare variable to insert to DB
                person_name = request.form.get("name")
                person_month = request.form.get("month")
                person_day = request.form.get("day")

                # Insert to DB
                db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", person_name, person_month, person_day)
                return redirect("/")
            else:
                return render_template("failure.html")

    else:
        # Display Birthday if the request is not post
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays, month_day=MONTH_DAY, MONTH=MONTH)
