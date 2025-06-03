from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create Flask app instance
app = Flask(__name__)

# Get Shopify credentials from environment
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD =os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")

# Route to fetch orders
@app.route('/orders') # type: ignore
def get_orders():
    url = f"https://{SHOP_NAME}/admin/api/2023-07/orders.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_API_KEY,
        "Content-Type": "application/json"

    }
    
    try:
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500 
    
    # Start the Flask server
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)
    

                      