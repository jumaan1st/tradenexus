from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal, InvalidOperation
import traceback

from extensions import db
from models import UserStocks
from utils.search import get_ticker
from services.currency import get_stock_price_in_inr, convert_to_inr
from utils.validators import (
    ValidationError, required_fields, validate_stock_name,
    validate_quantity, validate_price, validate_stock_id
)
import yfinance as yf

stock_bp = Blueprint('stock', __name__)


@stock_bp.route('/add-stock', methods=['POST'])
@jwt_required()
def add_stock():
    try:
        data = request.get_json()
        required_fields(data, ["name"])

        stock_name = data["name"]
        validate_stock_name(stock_name)
        quantity = validate_quantity(data.get("quantity", 1))
        current_price_flag = data.get("currentPrice", True)
        user_purchase_price = validate_price(data.get("purchasePrice"), "purchasePrice")
        user_id = int(get_jwt_identity())

        stock_symbol = get_ticker(stock_name)
        if not stock_symbol:
            return jsonify({"msg": f"Could not find ticker for '{stock_name}'"}), 404

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

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"msg": "Failed to add stock", "details": str(e)}), 500


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
            try:
                stock_yf = yf.Ticker(stock.stock_symbol)
                info = stock_yf.info
                price = Decimal(str(info.get('currentPrice', stock.purchase_price)))
                currency = info.get('currency', 'INR')
                if currency != "INR":
                    price = convert_to_inr(price, currency)
            except Exception:
                price = Decimal(str(stock.purchase_price))

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
        traceback.print_exc()
        return jsonify({"msg": "Failed to fetch stocks", "details": str(e)}), 500


@stock_bp.route('/edit-stock/<int:stock_id>', methods=['PUT'])
@jwt_required()
def edit_stock(stock_id):
    try:
        validate_stock_id(stock_id)
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Request body is required"}), 400

        new_quantity = validate_quantity(data.get("quantity")) if "quantity" in data else None
        new_price = validate_price(data.get("purchasePrice"), "purchasePrice") if "purchasePrice" in data else None
        user_id = int(get_jwt_identity())

        stock = UserStocks.query.filter_by(id=stock_id, user_id=user_id).first()
        if not stock:
            return jsonify({"msg": "Stock not found"}), 404

        if new_quantity is not None:
            stock.quantity = new_quantity
        if new_price is not None:
            stock.purchase_price = new_price

        db.session.commit()
        return jsonify({"msg": "Stock updated successfully"}), 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"msg": "Failed to update stock", "details": str(e)}), 500


@stock_bp.route('/delete-stock/<int:stock_id>', methods=['DELETE'])
@jwt_required()
def delete_stock(stock_id):
    try:
        validate_stock_id(stock_id)
        user_id = int(get_jwt_identity())
        stock = UserStocks.query.filter_by(id=stock_id, user_id=user_id).first()
        if not stock:
            return jsonify({"msg": "Stock not found"}), 404

        db.session.delete(stock)
        db.session.commit()
        return jsonify({"msg": f"Stock with ID {stock_id} deleted successfully"}), 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"msg": "Failed to delete stock", "details": str(e)}), 500
