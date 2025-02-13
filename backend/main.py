from flask import Flask, request, jsonify, send_from_directory
import os
app = Flask(__name__, static_folder="C:/Users/kusha/Desktop/alumni/Alumini-Portal/FrontendSrc")

#frontend folder path
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "C:/Users/kusha/Desktop/alumni/Alumini-Portal/FrontendSrc")
CREDENTIALS_FILE = "credentials.txt"

#load credentials
def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "r") as file:
        credentials = {}
        for line in file:
            username, password = line.strip().split(",")
            credentials[username] = password
        return credentials
        
def search_user(filename, username):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split(" | ")                 
                if data[0].lower() == username.lower():         
                    return f"User Found: {line.strip()}"
        return "User not found."
    except FileNotFoundError:
        return "Database file not found."

#save credentials
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "a") as file:
        file.write(f"{username},{password}\n")
        
#endpoints
@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "About us.html")

@app.route("/login")
def login_page():
    return send_from_directory(FRONTEND_FOLDER, "Login.html")

@app.route("/register")
def register_page():
    return send_from_directory(FRONTEND_FOLDER, "Register.html")

@app.route("/portal")
def portal_page():
    return send_from_directory(FRONTEND_FOLDER, "portal.html")

@app.route("/alumni")
def alumni_page():
    return send_from_directory(FRONTEND_FOLDER, "alumni.html")

@app.route("/login", methods=["POST"])
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
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400
    credentials = load_credentials()
    if username in credentials:
        return jsonify({"error": "Username already exists."}), 409
    save_credentials(username, password)
    return jsonify({"message": "Registration successful."}), 201

if __name__ == "__main__":
    app.run(debug=True)
