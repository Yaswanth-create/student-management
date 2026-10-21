from flask import Blueprint, request
import sqlite3
import html

login_bp = Blueprint("login", __name__)

DATABASE = "students.db"


@login_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()

        if not roll_no or not name:
            return "<h2>Please enter both Roll Number and Name.</h2>"

        try:
            with sqlite3.connect(DATABASE) as con:
                student = con.execute(
                    """
                    SELECT name
                    FROM students
                    WHERE roll_no = ? AND name = ?
                    """,
                    (roll_no, name)
                ).fetchone()

            if student:
                safe_name = html.escape(student[0])
                return f"""
                <h2>Login Successful!</h2>
                <h3>Welcome, {safe_name}!</h3>
                <a href="/">Back to Home</a>
                """

            return """
            <h2>Invalid Roll Number or Student Name.</h2>
            <a href="/login">Try Again</a>
            """

        except sqlite3.Error as error:
            return f"""
            <h2>Database Error</h2>
            <p>Please check that the students table exists.</p>
            <a href="/">Back to Home</a>
            """, 500

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Login</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                text-align: center;
                padding-top: 80px;
            }

            .login-box {
                background: white;
                padding: 30px;
                width: 350px;
                margin: auto;
                border-radius: 10px;
                box-shadow: 0 0 10px #ccc;
            }

            input {
                width: 90%;
                padding: 10px;
                margin: 10px;
            }

            button {
                background-color: #007bff;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>

    <body>
        <div class="login-box">
            <h2>Student Login</h2>

            <form method="POST">
                <label>Roll Number</label><br>
                <input type="text" name="roll_no" required>

                <br>

                <label>Student Name</label><br>
                <input type="text" name="name" required>

                <br><br>

                <button type="submit">Login</button>
            </form>

            <br>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    """