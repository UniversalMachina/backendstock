from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_folder='frontend/build')
CORS(app)

patterns = ["Ascending Triangle", "Descending Triangle", "Double Top", "Double Bottom", "Head and Shoulders"]
stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]

@app.route('/patterns', methods=['GET', 'POST', 'DELETE'])
def manage_patterns():
    global patterns
    if request.method == 'GET':
        return jsonify(patterns)
    elif request.method == 'POST':
        new_pattern = request.json.get('pattern')
        if new_pattern and new_pattern not in patterns:
            patterns.append(new_pattern)
        return jsonify(patterns)
    elif request.method == 'DELETE':
        pattern_to_remove = request.json.get('pattern')
        if pattern_to_remove in patterns:
            patterns.remove(pattern_to_remove)
        return jsonify(patterns)

@app.route('/stocks', methods=['GET', 'POST', 'DELETE'])
def manage_stocks():
    global stocks
    if request.method == 'GET':
        return jsonify(stocks)
    elif request.method == 'POST':
        new_stock = request.json.get('stock')
        if new_stock and new_stock not in stocks:
            stocks.append(new_stock)
        return jsonify(stocks)
    elif request.method == 'DELETE':
        stock_to_remove = request.json.get('stock')
        if stock_to_remove in stocks:
            stocks.remove(stock_to_remove)
        return jsonify(stocks)

def find_patterns(data):
    # Dummy pattern recognition logic for demonstration purposes
    patterns_found = []
    for i in range(len(data) - 1):
        if data[i]['Close'] < data[i+1]['Close']:  # Just an example pattern
            patterns_found.append({'date': data[i+1]['Date'], 'pattern': 'Example Pattern', 'price': data[i+1]['Close']})
    return patterns_found

@app.route('/simulate', methods=['POST'])
def simulate():
    results = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="1mo")
        data = hist.reset_index().to_dict(orient="records")

        actions = []
        for i in range(len(data)):
            if np.random.random() > 0.9:
                action = "buy" if np.random.random() > 0.5 else "sell"
                actions.append({"date": data[i]["Date"].strftime('%Y-%m-%d'), "action": action, "price": data[i]["Close"]})

        patterns_found = find_patterns(data)

        results[stock] = {
            "data": data,
            "actions": actions,
            "patterns": patterns_found,
            "performance": np.random.uniform(-10, 10)
        }

    return jsonify(results)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
