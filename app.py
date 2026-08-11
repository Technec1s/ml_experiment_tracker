from flask import Flask, jsonify, request
import sqlite3, hashlib
import pandas as pd
import os

app = Flask(__name__)

DATABASE = "experiments.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS experiment (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            best_accuracy REAL,
            final_loss REAL
        )
    """)
    return conn

@app.route("/api/experiment")
def sample_experiment():
    experiment = {
        "name": "baseline_model",
        "status": "completed",
        "accuracy": 0.91
    }
    return jsonify(experiment)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO agent (username, password_hash) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "agent registered", "username": username}), 201

@app.route("/upload-experiment", methods=["POST"])
def upload_experiment():
    data = request.get_json()
    title = data.get("title")
    filename = data.get("filename")

    if not os.path.exists(filename):
        return jsonify({"error": "file not found"}), 400

    df = pd.read_csv(filename)
    best_accuracy = df["accuracy"].max()
    final_loss = df["loss"].iloc[-1]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO experiment (title, best_accuracy, final_loss) VALUES (?, ?, ?)",
        (title, best_accuracy, final_loss)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "title": title,
        "best_accuracy": best_accuracy,
        "final_loss": final_loss
    }), 201

if __name__ == "__main__":
    app.run(debug=True)