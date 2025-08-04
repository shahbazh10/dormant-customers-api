from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Upload a CSV file to /upload endpoint."})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        df = pd.read_csv(file)
        df['Dormancy Date'] = pd.to_datetime(df['Dormancy Date'])
        df['Date of VAS Subscription'] = pd.to_datetime(df['Date of VAS Subscription'])
        df['Dormancy Period'] = (df['Dormancy Date'] - df['Date of VAS Subscription']).dt.days
        dormant_customers = df[df['Dormancy Period'] >= 90]
        return jsonify({"dormant_customers_count": len(dormant_customers)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
