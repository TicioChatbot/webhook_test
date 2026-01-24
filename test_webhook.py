import argparse
import requests
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Send a test webhook to a URL.")
    parser.add_argument("url", help="The URL to send the webhook to.")
    parser.add_argument("--payload", help="JSON string payload. If not provided, a default test payload is used.")
    
    args = parser.parse_args()
    
    if args.payload:
        try:
            payload = json.loads(args.payload)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON payload: {e}")
            sys.exit(1)
    else:
        payload = {
            "test": True,
            "message": "This is a test webhook.",
            "status": "success"
        }
    
    print(f"Sending webhook to {args.url} with payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(args.url, json=payload, headers={"Content-Type": "application/json"})
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except requests.RequestException as e:
        print(f"\nError sending request: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
