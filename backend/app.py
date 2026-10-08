from flask import Flask, request, jsonify
from flask_cors import CORS

from services.product_analysis import analyze_product


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():

    return jsonify({
        "message": "Counterfeit Detection API is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    product = request.json

    result = analyze_product(product)

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )