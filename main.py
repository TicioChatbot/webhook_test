import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Print the data to the Railway logs
    data = request.get_json(silent=True) or request.form.to_dict() or request.data.decode()
    print(f"Received Webhook: {data}")
    
    # Extract process_id
    process_id = None
    if isinstance(data, dict):
        # Try direct access
        process_id = data.get('process_id')
        
        # Try accessing via content.meta_data (based on previous context)
        if not process_id and 'content' in data and 'meta_data' in data['content']:
            meta_data = data['content']['meta_data']
            if isinstance(meta_data, list):
                for item in meta_data:
                    if isinstance(item, dict) and 'process_id' in item:
                        process_id = item['process_id']
                        break
            elif isinstance(meta_data, dict):
                 process_id = meta_data.get('process_id')

    if process_id:
        print(f"Extracted process_id: {process_id}")
        forwarding_url = os.environ.get("FORWARDING_URL")
        
        if forwarding_url:
            try:
                # Send the extracted info using logic similar to test_webhook
                payload = {"process_id": process_id, "original_source": "webhook_forwarder"}
                print(f"Forwarding to {forwarding_url} with payload: {payload}")
                response = requests.post(forwarding_url, json=payload, headers={"Content-Type": "application/json"})
                print(f"Forwarding Status: {response.status_code}")
            except Exception as e:
                print(f"Error forwarding webhook: {e}")
        else:
             print("FORWARDING_URL not set in .env")
    else:
        print("Could not extract process_id from payload")

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