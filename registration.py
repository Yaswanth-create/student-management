from flask import Blueprint, request
import sqlite3

registration_bp = Blueprint("registration", __name__)


@registration_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]

        with sqlite3.connect("students.db") as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_no TEXT UNIQUE NOT NULL
                )
            """)

            con.execute(
                "INSERT INTO students (name, roll_no) VALUES (?, ?)",
                (name, roll_no)
            )

        return "Student registered successfully!"

    return """
        <h2>Student Registration</h2>
        <form method="post">
            <input name="name" placeholder="Student Name" required>
            <br><br>
            <input name="roll_no" placeholder="Roll Number" required>
            <br><br>
            <button type="submit">Register</button>
        </form>
    """