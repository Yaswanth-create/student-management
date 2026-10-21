
from flask import Blueprint, request
import sqlite3
import html

registration_bp = Blueprint("registration", __name__)

DATABASE = "students.db"


def initialize_database():
    with sqlite3.connect(DATABASE) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT UNIQUE NOT NULL
            )
        """)


@registration_bp.route("/register", methods=["GET", "POST"])
def register():
    initialize_database()
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()

        if not name or not roll_no:
            message = "Please fill in all fields."
        else:
            try:
                with sqlite3.connect(DATABASE) as con:
                    con.execute(
                        "INSERT INTO students (name, roll_no) VALUES (?, ?)",
                        (name, roll_no)
                    )
                message = "Registration successful!"
            except sqlite3.IntegrityError:
                message = "This roll number is already registered."
            except sqlite3.Error:
                message = "A database error occurred. Please try again."

    safe_message = html.escape(message)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Registration | GITAM-Inspired</title>
        <style>
            * {{ box-sizing: border-box; }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f3f5f9;
                color: #222;
            }}

            header {{
                background: #7b1426;
                color: white;
                padding: 22px 8%;
                border-bottom: 4px solid #d8ad54;
            }}

            header h1 {{
                margin: 0;
                font-size: 26px;
            }}

            header p {{
                margin: 7px 0 0;
                font-size: 14px;
            }}

            .container {{
                max-width: 520px;
                margin: 45px auto;
                padding: 30px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 20px #00000012;
            }}

            h2 {{
                color: #7b1426;
                margin-top: 0;
            }}

            label {{
                display: block;
                margin: 18px 0 7px;
                font-weight: bold;
            }}

            input {{
                width: 100%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 15px;
            }}

            button {{
                width: 100%;
                margin-top: 24px;
                padding: 13px;
                background: #7b1426;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }}

            button:hover {{
                background: #59101d;
            }}

            .message {{
                padding: 12px;
                margin-top: 18px;
                background: #f8f0e5;
                border-radius: 5px;
            }}

            a {{ color: #7b1426; }}

            footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>GITAM</h1>
            <p>Student Information Management System</p>
        </header>

        <main class="container">
            <h2>Student Registration</h2>
            <p>Enter your details to register a student record.</p>

            <form method="POST">
                <label for="name">Student Name</label>
                <input id="name" name="name" type="text"
                       placeholder="Enter full name" required>

                <label for="roll_no">Roll Number</label>
                <input id="roll_no" name="roll_no" type="text"
                       placeholder="Enter roll number" required>

                <button type="submit">Register Student</button>
            </form>

            {"<div class='message'>" + safe_message + "</div>" if message else ""}

            <p><a href="/">Back to Home</a></p>
        </main>

        <footer>
            Student project demonstration · Not an official university portal
        </footer>
    </body>
    </html>
    """


initialize_database()
