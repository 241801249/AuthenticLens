from uuid import uuid4

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.product_analysis import analyze_product
from services.analysis_repository import save_analysis_result


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():

    return jsonify({
        "message": "AuthenticLens API is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    product = request.json

    result = analyze_product(product)

    analysis_id = str(uuid4())

    save_analysis_result(
        result=result,
        analysis_id=analysis_id,
    )

    result["analysis_id"] = analysis_id

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )