from flask import Flask, render_template, request
import pickle
import sqlite3
import os

app = Flask(__name__)

# Load ML model
model = pickle.load(open("salary_model.pkl", "rb"))

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            experience REAL,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Login page
@app.route("/")
def home():
    return render_template("login.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    email = request.form.get("email")
    experience = float(request.form.get("experience"))

    prediction = model.predict([[experience]])
    salary = round(prediction[0], 2)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (email, experience, salary) VALUES (?, ?, ?)",
        (email, experience, salary)
    )
    conn.commit()
    conn.close()

    return render_template("predict.html", result=salary)

# Admin panel
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT email, experience, salary FROM users")
    data = c.fetchall()
    conn.close()
    return render_template("admin.html", data=data)

# IMPORTANT for deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
