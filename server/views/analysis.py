from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import traceback

from services.ai import get_ai_client
from services.stock import analyze_stock
from utils.prompts import personal_stocks, prediction_prompt
from utils.validators import ValidationError, required_fields, validate_company_name, validate_analysis_params

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analysis', methods=['POST'])
@jwt_required()
def get_personal_stocks():
    try:
        data = request.get_json()
        required_fields(data, ["Amount", "term", "risk", "frequency"])
        validate_analysis_params(data)

        prompt, output_format = personal_stocks(
            data['Amount'], data['term'], data['risk'], data['frequency']
        )
        ai = get_ai_client()
        generated_json = ai.generate(prompt, system=None, output_format=output_format)
        return generated_json, 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to generate analysis", "details": str(e)}), 500


@analysis_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    try:
        data = request.get_json()
        required_fields(data, ["company"])
        validate_company_name(data["company"])

        stock_data = analyze_stock(data["company"])
        prompt, output_format = prediction_prompt(stock_data)
        ai = get_ai_client()
        result = ai.generate(prompt, system=None, output_format=output_format)
        return jsonify({"result": result, "raw_data": stock_data}), 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to analyze stock", "details": str(e)}), 500
