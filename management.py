
from flask import Blueprint, request
import sqlite3
import html

management_bp = Blueprint("management", __name__)

DATABASE = "students.db"


def get_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con


@management_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        department = request.form.get("department", "").strip()
        marks = request.form.get("marks", "").strip()

        if not name or not roll_no or not department or not marks:
            return "<h3>All fields are required.</h3><a href='/students'>Go Back</a>"

        try:
            marks_value = float(marks)

            if not 0 <= marks_value <= 100:
                return "<h3>Marks must be between 0 and 100.</h3><a href='/students'>Go Back</a>"

            with get_connection() as con:
                con.execute(
                    """
                    INSERT INTO students (name, roll_no, department, marks)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, roll_no, department, marks_value)
                )

            return """
                <h3>Student added successfully!</h3>
                <a href="/students">View Students</a>
            """

        except ValueError:
            return "<h3>Marks must be a number.</h3><a href='/students'>Go Back</a>"
        except sqlite3.IntegrityError:
            return "<h3>Roll number already exists.</h3><a href='/students'>Go Back</a>"
        except sqlite3.Error:
            return "<h3>Database error. Check your students table.</h3>", 500

    try:
        with get_connection() as con:
            records = con.execute(
                "SELECT id, name, roll_no, department, marks FROM students ORDER BY id"
            ).fetchall()

        rows = ""

        for student in records:
            rows += f"""
                <tr>
                    <td>{student['id']}</td>
                    <td>{html.escape(str(student['name']))}</td>
                    <td>{html.escape(str(student['roll_no']))}</td>
                    <td>{html.escape(str(student['department']))}</td>
                    <td>{student['marks']}</td>
                    <td>
                        <form action="/students/delete/{student['id']}"
                              method="post"
                              onsubmit="return confirm('Delete this student?');">
                            <button type="submit">Delete</button>
                        </form>
                    </td>
                </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Student Management</title>
            <style>
                body {{ font-family: Arial; margin: 30px; background: #f4f6f9; }}
                .container {{ background: white; padding: 20px; border-radius: 10px; }}
                input {{ padding: 8px; margin: 6px; }}
                button {{ padding: 8px 14px; cursor: pointer; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
                th {{ background: #e8eefc; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Student Information Management</h1>

                <h2>Add Student</h2>
                <form method="POST" action="/students">
                    <input name="name" placeholder="Student Name" required>
                    <input name="roll_no" placeholder="Roll Number" required>
                    <input name="department" placeholder="Department" required>
                    <input name="marks" type="number" min="0" max="100"
                           step="any" placeholder="Marks" required>
                    <button type="submit">Add Student</button>
                </form>

                <h2>Student Records</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Roll Number</th>
                        <th>Department</th>
                        <th>Marks</th>
                        <th>Action</th>
                    </tr>
                    {rows if rows else '<tr><td colspan="6">No student records found.</td></tr>'}
                </table>

                <p><a href="/">Back to Home</a></p>
            </div>
        </body>
        </html>
        """

    except sqlite3.Error:
        return "<h3>Database error. Check your students table.</h3>", 500


@management_bp.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        with get_connection() as con:
            cursor = con.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )

            if cursor.rowcount == 0:
                return "<h3>Student not found.</h3><a href='/students'>Back</a>", 404

        return """
            <h3>Student deleted successfully!</h3>
            <a href="/students">Back to Student Records</a>
        """

    except sqlite3.Error:
        return "<h3>Database error while deleting student.</h3>", 500
