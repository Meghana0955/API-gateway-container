from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def get_orders():
    dummy_orders = [
        {"id": 101, "item": "Laptop", "quantity": 1, "status": "Shipped"},
        {"id": 102, "item": "Wireless Mouse", "quantity": 2, "status": "Processing"}
    ]
    return jsonify({"orders": dummy_orders, "status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "order-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
