from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Capture the current time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n--- New Webhook Received at {now} ---")
    
    # 1. Log Headers
    print("Headers:")
    print(json.dumps(dict(request.headers), indent=2))
    
    # 2. Log Payload (handles JSON automatically)
    if request.is_json:
        payload = request.get_json()
        print("Payload (JSON):")
        print(json.dumps(payload, indent=2))
    else:
        print("Payload (Raw):")
        print(request.data.decode('utf-8'))

    # Return a 200 OK response to the sender
    return jsonify({"status": "success", "message": "Webhook received"}), 200

if __name__ == '__main__':
    # Running on port 5000 by default
    app.run(port=5000, debug=True)