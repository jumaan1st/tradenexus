from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import traceback

from services.market import scrape_market_data

market_bp = Blueprint('market', __name__)


@market_bp.route('/market-data-us', methods=['GET'])
@jwt_required()
def get_market_data_us():
    try:
        result = scrape_market_data('https://www.moneycontrol.com/us-markets', 'umdow', table_limit=2)
        if result is None:
            return jsonify({"msg": "Failed to find US market data"}), 504
        return jsonify(result), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to fetch US market data", "details": str(e)}), 500


@market_bp.route('/market-data-in', methods=['GET'])
@jwt_required()
def get_market_data_in():
    try:
        result = scrape_market_data('https://www.moneycontrol.com', 'inBN')
        if result is None:
            return jsonify({"msg": "Failed to find Indian market data"}), 504
        return jsonify(result), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to fetch Indian market data", "details": str(e)}), 500
