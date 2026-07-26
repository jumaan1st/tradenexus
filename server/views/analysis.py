from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import traceback

from services.ai import get_ai_client
from services.stock import analyze_stock
from utils.prompts import personal_stocks, prediction_prompt

analysis_bp = Blueprint('analysis', __name__)


def _handle_error(e, message="Something went wrong"):
    traceback.print_exc()
    return {"error": message, "details": str(e)}


@analysis_bp.route('/analysis', methods=['POST'])
@jwt_required()
def get_personal_stocks():
    data = request.get_json()
    amount = data.get('Amount', '100000')
    term = data.get('term', 'medium-term')
    risk = data.get('risk', 'medium')
    frequency = data.get('frequency', 'SIP')

    try:
        prompt = personal_stocks(amount, term, risk, frequency)
        ai = get_ai_client()
        result = ai.generate_json(prompt)
        return jsonify(result), 200
    except Exception as e:
        return jsonify(_handle_error(e, "Failed to generate content")), 500


@analysis_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    data = request.get_json()
    company = data.get('company', '')

    if not company:
        return jsonify({"error": "Missing 'company' field"}), 400

    try:
        stock_data = analyze_stock(company)
        prompt = prediction_prompt(stock_data)
        ai = get_ai_client()
        result = ai.generate_json(prompt)
        return jsonify({"result": result, "raw_data": stock_data}), 200
    except Exception as e:
        return jsonify(_handle_error(e, "Failed to analyze stock")), 500
