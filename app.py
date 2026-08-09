from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/api/experiment")
def sample_experiment():
    experiment = {
        "name": "baseline_model",
        "status": "completed",
        "accuracy": 0.91
    }
    return jsonify(experiment)

if __name__ == "__main__":
    app.run(debug=True)