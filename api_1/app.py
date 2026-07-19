from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/write/', methods=['POST'], strict_slashes=False)
def write_file():
    # Get the text sent from the frontend text box
    data = request.json.get('text_entry')
    
    if data:
        with open("memory.txt", "a") as f:
            f.write(data + "\n")
        return jsonify({"message": "Saved successfully!"}), 201
    return jsonify({"error": "No text provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
