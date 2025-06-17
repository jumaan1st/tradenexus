from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import yfinance as yf
import requests
from decimal import Decimal, ROUND_HALF_UP, getcontext
from sqlalchemy import and_
import traceback
from typing import Dict, Any, List, Tuple
from bs4 import BeautifulSoup
import pandas as pd
import ollama  # Import the Ollama client

# Import custom modules 
from api import generate_content
from prompts import personal_stocks, predictionPrompt, system_prompt
from get_symbol import get_ticker
from stock_analysis import analyze_stock

# Set decimal precision
getcontext().prec = 6

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    JWT_TOKEN_LOCATION=['cookies'],
    JWT_COOKIE_SECURE=False,  # Set to True in production
    JWT_COOKIE_SAMESITE='Lax',
    JWT_ACCESS_COOKIE_NAME='access_token',
    JWT_COOKIE_CSRF_PROTECT=False
)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

# Models
class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UserStocks(db.Model):
    __tablename__ = 'user_stocks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
    stock_name = db.Column(db.String(150), nullable=False)
    stock_symbol = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

# Utility functions
def get_stock_price_in_inr(symbol: str, use_current_price: bool, user_price: float = None) -> Tuple[Decimal, str]:
    """Fetch stock price and convert to INR if necessary."""
    stock = yf.Ticker(symbol)
    info = stock.info

    if use_current_price:
        price = Decimal(str(info['regularMarketPrice']))
        currency = info['currency']
        if currency != "INR":
            response = requests.get(f"https://api.frankfurter.app/latest?amount={price}&from={currency}&to=INR")
            fx_data = response.json()
            if 'rates' not in fx_data:
                raise ValueError("Currency conversion failed")
            price = Decimal(str(fx_data['rates']['INR'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        if user_price is None:
            raise ValueError("Purchase price required when currentPrice is False")
        price = Decimal(str(user_price))

    return price, info['shortName']

def handle_error(e: Exception, message: str = "Something went wrong") -> Dict[str, Any]:
    """Standardize error response."""
    traceback.print_exc()
    return {"error": message, "details": str(e)}

# Routes
@app.route('/bot', methods=['POST'])
def bot():
    """Handle chatbot requests using Ollama's LLaMA 3 model."""
    try:
        data = request.get_json()
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        # Format the conversation history for Ollama
        conversation = []
        for msg in messages:
            if 'user' in msg:
                conversation.append({"role": "user", "content": msg['user']})
            if 'bot' in msg:
                conversation.append({"role": "assistant", "content": msg['bot']})

        # Add a system prompt to set the bot's behavior
        conversation.insert(0, {
            "role": "system",
            "content": system_prompt
        })

        # Call the Ollama API with LLaMA 3
        response = ollama.chat(
            model='llama3',
            messages=conversation
        )

        # Extract the bot's response
        bot_response = response['message']['content']

        return jsonify({"response": bot_response}), 200

    except Exception as e:
        return jsonify(handle_error(e, "Failed to process chatbot request")), 500

@app.route('/analysis', methods=['POST'])
@jwt_required()
def get_personal_stocks():
    """Generate personalized stock recommendations."""
    data = request.get_json()
    amount = data.get('Amount', '100000')
    term = data.get('term', 'medium-term')
    risk = data.get('risk', 'medium')
    frequency = data.get('frequency', 'SIP')
    
    try:
        prompt = personal_stocks(amount, term, risk, frequency)
        generated_json = generate_content(prompt)
        return jsonify(json.loads(generated_json)), 200
    except Exception as e:
        return jsonify(handle_error(e, "Failed to generate content")), 500

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    required_fields = ["full_name", "username", "password", "email"]
    
    if not all(data.get(field) for field in required_fields):
        return jsonify({"msg": "All fields are required"}), 400

    if UserDetails.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username already exists"}), 409

    try:
        hashed_password = generate_password_hash(data["password"])
        new_user = UserDetails(
            full_name=data["full_name"],
            username=data["username"],
            password=hashed_password,
            email=data["email"]
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": f"User {data['full_name']} registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(handle_error(e, "Failed to register user")), 500

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and set JWT cookie."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = UserDetails.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"full_name": user.full_name, "email": user.email, "username": user.username},
        expires_delta=timedelta(days=7)
    )

    response = make_response(jsonify({"msg": "Login successful", "user_id": user.id}))
    response.set_cookie(
        "access_token", access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite='Lax',
        max_age=7 * 24 * 60 * 60,
        path='/'
    )
    return response, 200

@app.route('/market-data-us', methods=['GET'])
@jwt_required()
def get_market_data_us():
    url = 'https://www.moneycontrol.com/us-markets'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Extract data
    gain_loss = soup.find(id='umdow')
    if not gain_loss:
        return jsonify({"error": "Failed to find market data"}), 500

    tables = gain_loss.find_all("table")[:2]  # Get only the first two tables
    all_tables_json = []

    for table in tables:
        df = pd.read_html(str(table))[0]  # Convert each table to DataFrame
        json_table = df.to_dict(orient='records')  # Convert to list of dicts
        all_tables_json.append(json_table)

    return jsonify(all_tables_json), 200

@app.route('/market-data-in', methods=['GET'])
@jwt_required()
def get_market_data_in():
    url = 'https://www.moneycontrol.com'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Extract data
    gain_loss = soup.find(id='inBN')
    if not gain_loss:
        return jsonify({"error": "Failed to find market data"}), 500

    tables = gain_loss.find_all("table")  # Get only the first two tables
    all_tables_json = []

    for table in tables:
        df = pd.read_html(str(table))[0]  # Convert each table to DataFrame
        json_table = df.to_dict(orient='records')  # Convert to list of dicts
        all_tables_json.append(json_table)

    return jsonify(all_tables_json), 200

@app.route('/add-stock', methods=['POST'])
@jwt_required()
def add_stock():
    """Add a stock to user's portfolio."""
    try:
        data = request.get_json()
        stock_name = data.get("name")
        quantity = int(data.get("quantity", 1))
        current_price_flag = data.get("currentPrice", True)
        user_purchase_price = data.get("purchasePrice", None)
        user_id = int(get_jwt_identity())  # Use JWT identity

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
        return jsonify(handle_error(e)), 500

@app.route('/get-stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    """Retrieve user's stock portfolio."""
    try:
        user_id = int(get_jwt_identity())  # Use JWT identity
        stocks = UserStocks.query.filter_by(user_id=user_id).all()

        if not stocks:
            return jsonify({"msg": "No stocks found"}), 404

        stock_list: List[Dict[str, Any]] = []
        for stock in stocks:
            stock_yf = yf.Ticker(stock.stock_symbol)
            price = Decimal(str(stock_yf.info['currentPrice']))
            if stock_yf.info['currency'] != "INR":
                response = requests.get(f"https://api.frankfurter.app/latest?amount={price}&from={stock_yf.info['currency']}&to=INR")
                fx_data = response.json()
                if 'rates' not in fx_data:
                    return jsonify({"error": "Currency conversion failed", "details": fx_data}), 400
                price = Decimal(str(fx_data['rates']['INR'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

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
        return jsonify(handle_error(e)), 500

@app.route('/edit-stock/<int:stock_id>', methods=['PUT'])
@jwt_required()
def edit_stock(stock_id: int):
    """Update a stock in user's portfolio."""
    try:
        data = request.get_json()
        new_quantity = data.get("quantity")
        new_price = data.get("purchasePrice")
        user_id = int(get_jwt_identity())  # Use JWT identity

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
        return jsonify(handle_error(e, "Failed to update stock")), 500

@app.route('/delete-stock/<int:stock_id>', methods=['DELETE'])
@jwt_required()
def delete_stock(stock_id: int):
    """Delete a stock from user's portfolio."""
    try:
        user_id = int(get_jwt_identity())  # Use JWT identity
        stock = UserStocks.query.filter_by(id=stock_id, user_id=user_id).first()
        if not stock:
            return jsonify({"msg": "Stock not found"}), 404

        db.session.delete(stock)
        db.session.commit()
        return jsonify({"msg": f"Stock with ID {stock_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(handle_error(e, "Failed to delete stock")), 500

@app.route('/predict', methods=['POST'])
@jwt_required()
def analyze():
    """Predict stock performance."""
    data = request.get_json()
    company = data.get('company', '')

    if not company:
        return jsonify({"error": "Missing 'company' field"}), 400

    try:
        stock_data = analyze_stock(company)
        prompt = predictionPrompt(stock_data)
        result = json.loads(generate_content(prompt))
        return jsonify({"result": result, "raw_data": stock_data}), 200
    except Exception as e:
        return jsonify(handle_error(e, "Failed to analyze stock")), 500

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Access protected user information."""
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "id": current_user,
        "username": claims.get("username"),
        "full_name": claims.get("full_name"),
        "email": claims.get("email"),
    }), 200

@app.route('/logout', methods=['POST'])
def logout():
    """Log out user by clearing JWT cookie."""
    response = make_response(jsonify({"msg": "Logged out"}))
    response.set_cookie("access_token", "", max_age=0, httponly=True, secure=False, samesite='Lax', path='/')
    return response, 200

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)