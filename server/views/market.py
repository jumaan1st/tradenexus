from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from services.market import scrape_market_data

market_bp = Blueprint('market', __name__)


@market_bp.route('/market-data-us', methods=['GET'])
@jwt_required()
def get_market_data_us():
    result = scrape_market_data('https://www.moneycontrol.com/us-markets', 'umdow', table_limit=2)
    if result is None:
        return jsonify({"error": "Failed to find market data"}), 500
    return jsonify(result), 200


@market_bp.route('/market-data-in', methods=['GET'])
@jwt_required()
def get_market_data_in():
    result = scrape_market_data('https://www.moneycontrol.com', 'inBN')
    if result is None:
        return jsonify({"error": "Failed to find market data"}), 500
    return jsonify(result), 200
