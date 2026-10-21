
from flask import Flask
from registration import registration_bp
from login import login_bp
from importlib import import_module

management_bp = import_module("management").management_bp

app = Flask(__name__)

# Secret key for session support, if needed
app.secret_key = "student-management-secret-key"

# Register blueprints
app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(management_bp)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Information Management System</title>
    </head>
    <body>
        <h1>Student Information Management System</h1>
        <ul>
            <li><a href="/register">Student Registration</a></li>
            <li><a href="/login">Student Login</a></li>
            <li><a href="/students">Student Information Management</a></li>
        </ul>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
