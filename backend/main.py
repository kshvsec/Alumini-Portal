from flask import Flask, request, jsonify
import os

app = Flask(__name__)

CREDENTIALS_FILE = "credentials.txt"

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "r") as file:
        credentials = {}
        for line in file:
            username, password = line.strip().split(",")
            credentials[username] = password
        return credentials

@app.route("/login", methods=["POST","GET"])
def login():
    credentials = load_credentials()
    
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if username in credentials and credentials[username] == password:
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data["username"]
    password = data["password"]

if __name__ == "__main__":
    app.run(debug=True)
