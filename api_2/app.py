from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/read/', methods=['GET'])
def read_file():
    os.makedirs("/data", exist_ok=True) # Prevent crashes if file doesn't exist yet
    
    if os.path.exists("/data/memory.txt"):
        with open("/data/memory.txt", "r") as f:
            entries = f.readlines()
        return jsonify({"entries": [e.strip() for e in entries]})
    return jsonify({"entries": []})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
