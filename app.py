from flask import Flask, jsonify, request, render_template
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask (__name__)

# Shopify credentials from environment
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")


# Fetch Shopify orders
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
    return "Welcome to Sales Info! Visit /orders or /api/orders"

# HTML page
@app.route("/orders")
def orders_page():
    orders = fetch_orders()
    return render_template("orders.html", orders=orders)

# JSON API
@app.route("/api/orders")
def orders_api():
    try:
        orders = fetch_orders()
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========== Import AI Logic ++++++++++
from house_predicts_fixed.ai_dev.forecast import run_sales_forecast
from house_predicts_fixed.ai_dev.segment import segment_customers
from house_predicts_fixed.ai_dev.recommend import recommend_products
from house_predicts_fixed.ai_dev.search import smart_search
from house_predicts_fixed.ai_dev.assistant import answer_question

# API route for chatbot
@ app.route("/api/ask", methods=["POST"])
def ask_api ():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    try:
        response = answer_question(question)
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chatbot UI
@app.route("/ask", methods=["GET", "POST"]) # type: ignore
def ask_ui():
    answer = None
    question = None
    if request.method == "POST":
        data = request.form
        question = data.get("question", "")
        answer = answer_question(question) # Your Python functionin assistant.py
        return render_template("ask.html", answer=answer, question=question)
    
    