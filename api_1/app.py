from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# CHANGE THIS LINE:
from prometheus_flask_exporter import PrometheusMetrics  # <-- Added 's' at the end

app = Flask(__name__)
CORS(app)

metrics = PrometheusMetrics(app)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/write/', methods=['POST'], strict_slashes=False)
def write_file():
    os.makedirs("/data", exist_ok=True)
    data = request.get_json()
    
    # Update 'text' to 'text_entry' to match your frontend payload exactly!
    user_text = data.get('text_entry', 'No data provided') if data else 'No data provided'
    
    with open("/data/memory.txt", "a") as f:
        f.write(f"{user_text}\n")
        
    return jsonify({"status": "saved"}), 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
