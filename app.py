from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Function to generate hash
def generate_hash(algorithm, text):
    try:
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    except ValueError:
        return None

# Create POST endpoints for different hashing algorithms
@app.route('/hash/md5', methods=['POST'])
def hash_md5():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "md5", "hash": generate_hash("md5", message)})

@app.route('/hash/sha1', methods=['POST'])
def hash_sha1():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "sha1", "hash": generate_hash("sha1", message)})

@app.route('/hash/sha256', methods=['POST'])
def hash_sha256():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "sha256", "hash": generate_hash("sha256", message)})

@app.route('/hash/sha512', methods=['POST'])
def hash_sha512():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "sha512", "hash": generate_hash("sha512", message)})

@app.route('/hash/blake2b', methods=['POST'])
def hash_blake2b():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "blake2b", "hash": generate_hash("blake2b", message)})

@app.route('/hash/blake2s', methods=['POST'])
def hash_blake2s():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"algorithm": "blake2s", "hash": generate_hash("blake2s", message)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
