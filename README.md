# MedMe QUESTION BOOK
#### Video Demo: The demo have been removed from Youtube.
#### Description: Personal project, a Question Book for Biomedical students pears, University of Khartoum. 

# MedMe 

## CS50
>This was my final project to conclude the CS50's Introduction to Computer Sciense course.

>CS50 library for python, python, flask, flask web framework, bootstraps, web development, CS50
## Features

- [Sqlite3](https://www.sqlite.org/index.html)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Bootstraps](https://getbootstrap.com/)
- [Cs50 Docs](https://cs50.readthedocs.io/libraries/cs50/python/)

I've used Flask web framework based in Python for Back-ending
To manage data I used Sqlite3 for creating Database called University.db
I utilised Bootsraps open-source styling on my platform.
The CS50 library is used for interactions between the flask framework and Sqlite3.
I also used the pre-made template apology message from helpers.py from CS50 week 9 PSET.

## Explaining the project functionality and the database
My final project is a website that is directed to Biomedical students in Khartoum University. It is a Question Book application that provides the students with testing materials to go over and prepare from.

All of information associated with the students like usernames, Hash-passwords, number of correct answers, number of incorrect answers and the total questions completed are stored in a table called users in university.db database.

For question-related data, they are stored in a seperate table called questions in university.db, where the questions prompts, candidate answers, correct answer and explaination for each question are kept and passed from ayes
There is a hero for the weboste to go for doing questions or to look on the profile.
The websites gives a breif background about khartoum university.
Also a quick info about the developer.
And Finally, in the Home Page, a table shows some of the University Colleges.

### Retrieving questions from the database and thier corresponing answers and explaination.
The heading tag in the quize.html page is going to be a place holder for a certain question at a time based on the current value comming from the users table per the current occupied session of the user who logged-in.

The answers are going to be held in the select tag and written on the page using Djinja syntax one by one.

```python
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
```

### The logic to check the answer weather it is correct or not.

```python
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
                    b.execute("UPDATE users SET incorrect = 0 WHERE id = ?", session["user_id"])
                    db.execute("UPDATE users SET completed = 0 WHERE id = ?", session["user_id"])
                    return apology("you have completed the Question Book!")

```

## Pictures
- Login and Register pages

| Register | Login |
| :---: | :---: |
| <img src="Screenshots/Register.png" width="400">  | <img src="Screenshots/Login.png" width="400">|

- Homepage and University history show case

| Homepage - Hero |  University history |
| :---: | :---: |
| <img src="Screenshots/Home_page.png" width="400"> | <img src="Screenshots/University.png" width = "400">|

- About the Developer and Associated Colleges

| About the Developer |  Associated Colleges |
| :---: | :---: |
| <img src="Screenshots/About.png" width="400"> | <img src="Screenshots/Colleges.png" width = "400">|

- Questions

| Questions |
| :---: |
| <img src="Screenshots/Question.png" width="800"> |

- Correct and Incorrect navigation

| Correct | InCorrect |
| :---: |
| <img src="Screenshots/Correct.png" width="400"> | <img src="Screenshots/Incorrect.png" width="400"> |

- Profile Page

| Profile |
| :---: |
| <img src="Screenshots/Correct.png" width="800"> |


## Demonstration on youtube
For the CS50 final project you have to make a video showning your project,
[My Final Project presentation](https://www.youtube.com/watch?v=mzI3ixBM7uM)

## Documentation
https://www.sqlite.org/index.html

https://www.sqlite.org/index.html
https://flask.palletsprojects.com/en/1.1.x/
https://getbootstrap.com/
https://cs50.readthedocs.io/libraries/cs50/python/

## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/2020/
