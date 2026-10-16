
from flask import Flask
from registration import registration_bp
from login import login_bp
from management import management_bp

app = Flask(__name__)

app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(management_bp)


@app.route("/")
def home():
    return """
    <h1>Student Information Management System</h1>
    <p><a href="/register">Student Registration</a></p>
    <p><a href="/login">Student Login</a></p>
    <p><a href="/students">View Student Information</a></p>
    """


if __name__ == "__main__":
    app.run(debug=True)
