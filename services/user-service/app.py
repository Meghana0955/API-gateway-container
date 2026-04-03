from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    dummy_users = [
        {"id": 1, "name": "Alice Wonderland", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Builder", "email": "bob@example.com"}
    ]
    return jsonify({"users": dummy_users, "status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "user-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
