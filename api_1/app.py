from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/write/', methods=['POST'], strict_slashes=False)
def write_file():
    # Get the text sent from the frontend text box
    os.makedirs("/data", exist_ok=True)
    
    with open("/data/memory.txt", "a") as f:
        f.write("Your data entry\n")
    return jsonify({"status": "saved"}), 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
