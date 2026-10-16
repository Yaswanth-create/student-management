
from flask import Blueprint
import sqlite3

management_bp = Blueprint("management", __name__)


@management_bp.route("/students")
def students():
    with sqlite3.connect("students.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT UNIQUE NOT NULL
            )
        """)

        rows = con.execute(
            "SELECT id, name, roll_no FROM students"
        ).fetchall()

    html = "<h2>Student Information</h2><ul>"

    for student in rows:
        html += (
            f"<li>ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Roll No: {student[2]}</li>"
        )

    html += "</ul>"
    return html
