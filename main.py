import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Print the data to the Railway logs
    data = request.get_json(silent=True) or request.form.to_dict() or request.data.decode()
    print(f"Received Webhook: {data}")
    
    return jsonify({"status": "received"}), 200

# Health check (important for many cloud providers to verify the app is alive)
@app.route('/', methods=['GET'])
def home():
    return "Webhook listener is active!", 200

if __name__ == '__main__':
    # Use the PORT variable provided by Railway, or 5000 as a backup
    port = int(os.environ.get("PORT", 8080))
    # host='0.0.0.0' tells Flask to listen to all public traffic
    app.run(host='0.0.0.0', port=port)