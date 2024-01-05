import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
import datetime

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///university.db")



@app.route("/")
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")


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
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/register", methods = ["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password do not match")

        try:
            new_user = db.execute("INSERT INTO users (name, hash) VALUES(?, ?)",
                    request.form.get("username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("user already exists")

        session["user_id"] = new_user

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Show portfolio of stocks"""
     # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quize", methods=["POST", "GET"])
@login_required
def quize():
    """Show portfolio of stocks"""
    if request.method == "GET":


        current_question_id = db.execute("SELECT current FROM users WHERE id = ?", session["user_id"])[0]["current"]

        try:
            question = db.execute("SELECT * FROM questions WHERE id = ?", current_question_id)
            answer1 = question[0]["answer1"]
            answer2 = question[0]["answer2"]
            answer3 = question[0]["answer3"]
            answer4 = question[0]["answer4"]
            answer_correct = question[0]["correct"]
            answers = [answer1, answer2, answer3, answer4]

            return render_template("quize.html", question=question[0]["question"], answers=answers, number=current_question_id)



        except:
            db.execute("UPDATE users SET current = 1 WHERE id = ?", session["user_id"])
            return apology("you have completed the Question Book!")

    else:
        if not session["user_id"]:
            redirect("/login")

        current_question_id = db.execute("SELECT current FROM users WHERE id = ?", session["user_id"])[0]["current"]
        question = db.execute("SELECT * FROM questions WHERE id = ?", current_question_id)
        answer_correct = question[0]["correct"]

        selected_answer = request.form.get("answer")
        correct = db.execute("SELECT correct FROM users WHERE id = ?", session["user_id"])[0]["correct"]
        incorrect = db.execute("SELECT incorrect FROM users WHERE id = ?", session["user_id"])[0]["incorrect"]
        total_questions = current_question_id

        if selected_answer == answer_correct:
            correct = correct + 1
            try:
                db.execute("UPDATE users SET correct = ? WHERE id = ?", correct, session["user_id"])
                db.execute("UPDATE users SET completed = ? WHERE id = ?", total_questions, session["user_id"])
                return redirect("/correct")

            except:
                db.execute("UPDATE users SET current = 1 WHERE id = ?", session["user_id"])
                db.execute("UPDATE users SET correct = 0 WHERE id = ?", session["user_id"])
                b.execute("UPDATE users SET incorrect = 0 WHERE id = ?", session["user_id"])
                db.execute("UPDATE users SET completed = 0 WHERE id = ?", session["user_id"])
                return apology("you have completed the Question Book!")

        else:
            incorrect = incorrect + 1
            global wrong_answer
            wrong_answer = selected_answer
            try:
                db.execute("UPDATE users SET incorrect = ? WHERE id = ?", incorrect, session["user_id"])
                db.execute("UPDATE users SET completed = ? WHERE id = ?", total_questions, session["user_id"])
                return redirect("/incorrect")

            except:
                    db.execute("UPDATE users SET current = 1 WHERE id = ?", session["user_id"])
                    db.execute("UPDATE users SET correct = 0 WHERE id = ?", session["user_id"])
                    db.execute("UPDATE users SET incorrect = 0 WHERE id = ?", session["user_id"])
                    db.execute("UPDATE users SET completed = 0 WHERE id = ?", session["user_id"])
                    return render_template("erase.html")


@app.route("/correct", methods=["POST", "GET"])
@login_required
def correct():
    if request.method == "GET":
        try:
            current_question_id = db.execute("SELECT current FROM users WHERE id = ?", session["user_id"])[0]["current"]
            question = db.execute("SELECT * FROM questions WHERE id = ?", current_question_id)
            explaination = question[0]["explaination"]
            answer_correct = question[0]["correct"]

            current_question_id = current_question_id + 1

            db.execute("UPDATE users SET current = ? WHERE id = ?", current_question_id, session["user_id"])

        except:
                db.execute("UPDATE users SET current = 1 WHERE id = ?", session["user_id"])
                return apology("you have completed the Question Book!")

        return render_template("correct.html", explaination=explaination, answer=answer_correct, question=current_question_id)


    else:
        return redirect("/quize")

@app.route("/incorrect", methods=["POST", "GET"])
@login_required
def incorrect():
    if request.method == "GET":
        try:
            current_question_id = db.execute("SELECT current FROM users WHERE id = ?", session["user_id"])[0]["current"]
            question = db.execute("SELECT * FROM questions WHERE id = ?", current_question_id)
            explaination = question[0]["explaination"]
            answer_correct = question[0]["correct"]

            current_question_id = current_question_id + 1

            db.execute("UPDATE users SET current = ? WHERE id = ?", current_question_id, session["user_id"])

        except:
                db.execute("UPDATE users SET current = 1 WHERE id = ?", session["user_id"])
                return apology("you have completed the Question Book!")

        return render_template("incorrect.html", explaination=explaination, answer=answer_correct, question=current_question_id)


    else:
        return redirect("/quize")


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    if request.method == "GET":
        correct = db.execute("SELECT correct FROM users WHERE id =?",  session["user_id"])[0]["correct"]
        incorrect = db.execute("SELECT incorrect FROM users WHERE id =?",  session["user_id"])[0]["incorrect"]
        total_questions = db.execute("SELECT current FROM users WHERE id =?",  session["user_id"])[0]["current"]
        name = db.execute("SELECT name FROM users WHERE id =?",  session["user_id"])[0]["name"]

        correct_precentage = int(correct)
        incorrect_precentage = int(incorrect)


        return render_template("profile.html", correct=correct_precentage, incorrect=incorrect_precentage, total_questions=total_questions, name=name)
