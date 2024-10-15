import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks_data = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
    user_data = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_data = usd(int(user_data[0]["cash"]))
    quote = []
    quote_data = []
    total_price = []
    for row in stocks_data:
        quote = lookup(row["company_id"])
        total_price.append(usd((int(quote["price"])) * int(row["shares"])))
        quote["price"] = usd(int(quote["price"]))
        quote_data.append(quote)

    return render_template("homepage.html", quote=quote_data, stocks=stocks_data, total=total_price, user=user_data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares") or not request.form.get("shares").isnumeric() or int(request.form.get("shares")) < 1:
            return apology("Input Correct symbol and/or share", 400)
        else:
            # Defining data from buy form
            num_share = request.form.get("shares")
            company_id = (request.form.get("symbol")).upper()
            quoted_data = lookup(company_id)
            # Getting current user data from DB
            user_data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            cash = user_data[0]["cash"]
            if quoted_data:
                if not int(quoted_data["price"]) * int(num_share) > int(cash):
                    new_cash_value = int(cash) - (int(quoted_data["price"]) * int(num_share))
                    existing_stock = db.execute(
                        "SELECT * FROM stocks WHERE user_id = ? AND company_id = ?", session["user_id"], company_id)
                    if not existing_stock:
                        db.execute("INSERT INTO stocks (user_id, company_name, shares, company_id) VALUES (?, ?, ?, ?)",
                                   session["user_id"], quoted_data["name"], int(num_share), company_id)
                    else:
                        db.execute("UPDATE stocks SET shares = shares + ? WHERE user_id = ? AND company_id = ?",
                                   int(num_share), session["user_id"], company_id)
                    db.execute("UPDATE users SET cash = ? WHERE id = ?",
                               new_cash_value, session["user_id"])

                    # Insert transaction into history (transactions table)
                    db.execute("INSERT INTO transactions (company_id, user_id, status, num_shares, price_per_share) VALUES (?, ?, 'bought', ?, ?)",
                               company_id, session["user_id"], num_share, quoted_data["price"])

                    return redirect("/")

                else:
                    return apology("Insufficient Cash... ", 403)
            else:
                return apology("Company's not found... ", 400)

    return render_template("buy_form.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Fetch transaction history from the database for the logged-in user
    transactions = db.execute("""
        SELECT transactions.id, transactions.company_id, transactions.status, transactions.num_shares, transactions.time,
               transactions.price_per_share
        FROM transactions
        WHERE user_id = ?
        ORDER BY time DESC
    """, session["user_id"])

    # Calculate the total money spent or gained for each transaction
    for transaction in transactions:
        # Check if price_per_share and num_shares are not None
        price_per_share = transaction["price_per_share"]
        num_shares = transaction["num_shares"]

        if price_per_share is not None and num_shares is not None:
            # Use float for calculations to support decimal values
            transaction["total_amount"] = usd(float(price_per_share) * float(num_shares))
        else:
            # Set total_amount to a default value if any of the required fields are None
            # or you can set it to 0 or any other appropriate value
            transaction["total_amount"] = "N/A"

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if lookup(request.form.get("symbol")):
            if not request.form.get("symbol"):
                return apology("Input Symbol", 400)
            else:
                quoted_data = lookup(request.form.get("symbol"))
                quoted_data["price"] = usd(quoted_data["price"])
                return render_template("quoted.html", quote=quoted_data)
        else:
            return apology("Company's not found...", 400)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Hash the password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert the new user into the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       request.form.get("username"), hashed_password)
        except:
            return apology("username already exists", 400)

        # Redirect to login page after successful registration
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks_data = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
    user_data = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_data1 = usd(int(user_data[0]["cash"]))
    quote = []
    quote_data = []
    total_price = []
    for row in stocks_data:
        quote = lookup(row["company_id"])
        total_price.append(usd((int(quote["price"])) * int(row["shares"])))
        quote["price"] = usd(int(quote["price"]))
        quote_data.append(quote)
    if request.method == "POST":
        if not request.form.get("symbol") and not request.form.get("shares"):
            return apology("Company and/or stock not found", 400)
        else:
            # Check if the input are valid
            shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND company_id = ?", int(
                session["user_id"]), request.form.get("symbol"))
            if shares and int(request.form.get("shares")) <= int(shares[0]["shares"]) and int(request.form.get("shares")) >= 1:
                # Declare variable to insert to DB
                current_stock_price = lookup(request.form.get("symbol"))
                # Insert to DB
                new_cash_value = int(
                    user_data[0]["cash"]) + (int(current_stock_price["price"]) * int(request.form.get("shares")))
                new_stock_owned = db.execute(
                    "SELECT shares FROM stocks WHERE user_id = ? AND company_id = ?", session["user_id"], request.form.get("symbol"))
                new_stock_owned = int(new_stock_owned[0]["shares"]) - \
                    int(request.form.get("shares"))

                # After successful stock sale
                db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND company_id = ?",
                           new_stock_owned, session["user_id"], request.form.get("symbol"))
                db.execute("UPDATE users SET cash = ? WHERE id = ?",
                           new_cash_value, session["user_id"])

                # Insert transaction into history (transactions table)
                db.execute("INSERT INTO transactions (company_id, user_id, status, num_shares, price_per_share) VALUES (?, ?, 'sold', ?, ?)",
                           request.form.get("symbol"), session["user_id"], request.form.get("shares"), current_stock_price["price"])

                return redirect("/sell")

            else:
                return apology("Failed to sell stocks...", 400)

    return render_template("sell_form.html", quote=quote_data, stocks=stocks_data, total=total_price, user=user_data1)
