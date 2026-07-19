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
    data = request.get_json()
    
    # 2. Extract the text field (adjust 'text' to match whatever key your frontend sends, e.g., 'entry' or 'input')
    # If it's missing, we fall back to a safer default
    user_text = data.get('text', 'No data provided') if data else 'No data provided'
    
    # 3. Write the actual user text to the shared Filestore disk
    with open("/data/memory.txt", "a") as f:
        f.write(f"{user_text}\n")
        
    return jsonify({"status": "saved"}), 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
