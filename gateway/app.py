from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

# Service registry mapping service paths to target URLs
SERVICES = {
    "user": "http://localhost:5001",
    "order": "http://localhost:5002"
}

@app.route("/health", methods=['GET'])
def health():
    return jsonify(status="ok", message="Gateway is healthy"), 200

@app.route("/<service_name>", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route("/<service_name>/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(service_name, path=""):
    if service_name not in SERVICES:
        return jsonify(error="Service not found", status=404), 404

    # Construct the target URL
    target_url = f"{SERVICES[service_name]}/{path}"

    try:
        # Forward the incoming request to the target microservice
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        # Forward the response back to the client
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response

    except requests.exceptions.RequestException as e:
        return jsonify(error=f"Error connecting to target service: {str(e)}", status=502), 502

# Fallback for root or unmatched routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path == "health":
        return health()
    return jsonify(error="Invalid route. Ensure you use /user/* or /order/*", status=404), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
