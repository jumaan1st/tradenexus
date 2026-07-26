from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal
import traceback

from extensions import db
from models import UserStocks
from utils.search import get_ticker
from services.currency import get_stock_price_in_inr, convert_to_inr
import yfinance as yf

stock_bp = Blueprint('stock', __name__)


def _handle_error(e, message="Something went wrong"):
    traceback.print_exc()
    return {"error": message, "details": str(e)}


@stock_bp.route('/add-stock', methods=['POST'])
@jwt_required()
def add_stock():
    try:
        data = request.get_json()
        stock_name = data.get("name")
        quantity = int(data.get("quantity", 1))
        current_price_flag = data.get("currentPrice", True)
        user_purchase_price = data.get("purchasePrice", None)
        user_id = int(get_jwt_identity())

        stock_symbol = get_ticker(stock_name)
        price_inr, name = get_stock_price_in_inr(stock_symbol, current_price_flag, user_purchase_price)

        existing_stocks = UserStocks.query.filter_by(user_id=user_id, stock_symbol=stock_symbol).all()
        for stock in existing_stocks:
            old_price = Decimal(str(stock.purchase_price))
            if abs(old_price - price_inr) / old_price * 100 <= Decimal("0.5"):
                stock.quantity += quantity
                db.session.commit()
                return jsonify({
                    "msg": f"Stock {name} ({stock_symbol}) updated successfully",
                    "stock_info": {
                        "name": name,
                        "symbol": stock_symbol,
                        "price": float(price_inr),
                        "currency": "INR"
                    }
                }), 201

        count = UserStocks.query.filter_by(user_id=user_id, stock_symbol=stock_symbol).count()
        final_name = name if count == 0 else f"{name} {count + 1}"

        new_stock = UserStocks(
            user_id=user_id,
            stock_name=final_name,
            stock_symbol=stock_symbol,
            purchase_price=float(price_inr),
            quantity=quantity
        )
        db.session.add(new_stock)
        db.session.commit()

        return jsonify({
            "msg": f"Stock {name} ({stock_symbol}) added successfully",
            "stock_info": {
                "name": name,
                "symbol": stock_symbol,
                "price": float(price_inr),
                "currency": "INR"
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(_handle_error(e)), 500


@stock_bp.route('/get-stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    try:
        user_id = int(get_jwt_identity())
        stocks = UserStocks.query.filter_by(user_id=user_id).all()

        if not stocks:
            return jsonify({"msg": "No stocks found"}), 404

        stock_list = []
        for stock in stocks:
            stock_yf = yf.Ticker(stock.stock_symbol)
            info = stock_yf.info
            price = Decimal(str(info['currentPrice']))
            if info['currency'] != "INR":
                price = convert_to_inr(price, info['currency'])

            stock_list.append({
                "id": stock.id,
                "name": stock.stock_name,
                "ticker": stock.stock_symbol,
                "quantity": stock.quantity,
                "purchasePrice": float(stock.purchase_price),
                "currentPrice": float(price),
            })

        return jsonify(stock_list), 200

    except Exception as e:
        return jsonify(_handle_error(e)), 500


@stock_bp.route('/edit-stock/<int:stock_id>', methods=['PUT'])
@jwt_required()
def edit_stock(stock_id):
    try:
        data = request.get_json()
        new_quantity = data.get("quantity")
        new_price = data.get("purchasePrice")
        user_id = int(get_jwt_identity())

        stock = UserStocks.query.filter_by(id=stock_id, user_id=user_id).first()
        if not stock:
            return jsonify({"msg": "Stock not found"}), 404

        if new_quantity is not None:
            stock.quantity = int(new_quantity)
        if new_price is not None:
            stock.purchase_price = float(new_price)

        db.session.commit()
        return jsonify({"msg": "Stock updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(_handle_error(e, "Failed to update stock")), 500


@stock_bp.route('/delete-stock/<int:stock_id>', methods=['DELETE'])
@jwt_required()
def delete_stock(stock_id):
    try:
        user_id = int(get_jwt_identity())
        stock = UserStocks.query.filter_by(id=stock_id, user_id=user_id).first()
        if not stock:
            return jsonify({"msg": "Stock not found"}), 404

        db.session.delete(stock)
        db.session.commit()
        return jsonify({"msg": f"Stock with ID {stock_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(_handle_error(e, "Failed to delete stock")), 500
