from flask import Flask, render_template, request, jsonify, redirect, session, send_file
from datetime import datetime
from security import encrypt_data, decrypt_data
from users import USERS
import csv, os

app = Flask(__name__)
app.secret_key = "demo_secret_key"

LOG_FILE = "keystrokes.enc"

# ---------------- LOGIN ---------------- #

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if USERS.get(u) == p:
            session["user"] = u
            return redirect("/logger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- LOGGER ---------------- #

@app.route("/logger")
def logger():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log_key():
    if "user" not in session:
        return jsonify({"status": "unauthorized"})

    data = request.json
    key = data["key"]
    ip = request.remote_addr
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"{time},{session['user']},{ip},{key}\n"
    encrypted = encrypt_data(entry)

    with open(LOG_FILE, "ab") as f:
        f.write(encrypted + b"\n")

    return jsonify({"status": "logged"})

# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/export")
def export_csv():
    if "user" not in session:
        return redirect("/")

    rows = []
    with open(LOG_FILE, "rb") as f:
        for line in f:
            rows.append(decrypt_data(line.strip()).split(","))

    with open("export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "User", "IP", "Key"])
        writer.writerows(rows)

    return send_file("export.csv", as_attachment=True)

if __name__ == "__main__":
    app.run()
