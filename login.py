
from flask import Blueprint, request
import sqlite3

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        roll_no = request.form["roll_no"]
        name = request.form["name"]

        with sqlite3.connect("students.db") as con:
            student = con.execute(
                "SELECT name FROM students WHERE roll_no = ? AND name = ?",
                (roll_no, name)
            ).fetchone()

        if student:
            return f"<h2>Welcome, {student[0]}!</h2>"

        return "<h2>Invalid student details.</h2>"

    return """
    <h2>Student Login</h2>
    <form method="post">
        <label>Roll Number:</label>
        <input type="text" name="roll_no" required>
        <br><br>

        <label>Student Name:</label>
        <input type="text" name="name" required>
        <br><br>

        <button type="submit">Login</button>
    </form>
    """
