from flask import Flask, jsonify, render_template
import os
import requests

app = Flask (__name__)

# Load Shopify credentials from environment
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")

# Shared function to fetch Shopify orders
def fetch_orders():
    url = f"https://{SHOP_NAME}/admin/api/2023-07/orders.json"
    headers = {
        "X-Shopify-Access_Token": SHOPIFY_API_KEY,
        "Content_Type": "application/json"
    }
    try:
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("orders" , [])
    except Exception as e:
        print(f"Erronr: {e}")
        return []
    
# Home page
@app.route ("/")
def home():
    return "Welcome to Sales Info! Visit /orders for the dashboard or /api/orders for raw data."

# HTML page
@app.route("/orders")
def orders_page():
    orders = fetch_orders()
    return render_template("orders.html", orders=orders)

# JSON API
@app.route("/api/orders")
def orders_api():
    orders = fetch_orders()
    return jsonify(orders)

if __name__ == "__main__":
    app.run(debug=True)


        