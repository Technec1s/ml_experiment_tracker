from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("experiments.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
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

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO agent (username, password_hash) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "agent registered", "username": username}), 201

if __name__ == "__main__":
    app.run(debug=True)