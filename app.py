from flask import Flask, render_template,session, request, redirect, jsonify
from helpers import query_db, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG



app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


  



secret_key = secrets.token_hex(16)
app.secret_key = 'd127b18e-6524-4e9f-a65c-9c7d83d02a80'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def home():
    return render_template('index.html')


@app.route("/arrivalReport")
def arrivalReport():
    return render_template('arrivalHistory.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    try:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            logging.debug(f"The type of 'userId' is {request}")
            # Ensure username was submitted
            if not request.form.get("username"):
                return jsonify({"error": "Must provide username."}), 400

            # Ensure password was submitted
            elif not request.form.get("password"):
                return jsonify({"error": "Must provide password."}), 400

            # Query database for username
            rows = query_db(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")
            ):
                return jsonify({"error": "Invalid username or password."}), 400

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("login.html")

    except Exception as e:
        # Handle the exception and return an error response
        return render_template("error.html", message=str(e))


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        try:
            userName = request.form.get("username")
            password = request.form.get("password")
            confirmPassword = request.form.get("confirmation")
            
            # Ensure username was submitted
            if not userName:
                return jsonify({"error": "Invalid username."}), 400
            # Ensure password was submitted
            elif not password:
                return jsonify({"error": "Invalid password."}), 400
            # Ensure password and confirmation match
            elif password != confirmPassword:
                return jsonify({"error": "Password and confirm password do not match."}), 400

            # Query database for username
            rows = query_db("SELECT * FROM users WHERE username = ?", userName)

            # Ensure username does not exist already
            if len(rows) > 0:
                return jsonify({"error": "Username already exists."}), 400
            hashedPassword = generate_password_hash(password, method="pbkdf2", salt_length=16)
            print('user' + userName)

            print('hash' + hashedPassword)
            query_db("INSERT INTO users (username, hash) VALUES (?, ?)", userName, hashedPassword)

            return render_template("login.html")
         
        except Exception as e:
              
            logging.debug(f"error is {e}")
            return jsonify({"error": str(e)}), 500

    else:
        return render_template("register.html")