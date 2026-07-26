import re


class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def required_fields(data, fields):
    """Validate that all required fields exist and are non-empty."""
    if not data:
        raise ValidationError("Request body is required")
    missing = [f for f in fields if not data.get(f)]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")


def validate_email(email):
    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError("Invalid email format")


def validate_password(password):
    if not password:
        raise ValidationError("Password is required")
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters")
    if len(password) > 128:
        raise ValidationError("Password must be at most 128 characters")


def validate_username(username):
    if not username:
        raise ValidationError("Username is required")
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters")
    if len(username) > 50:
        raise ValidationError("Username must be at most 50 characters")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Username can only contain letters, numbers, and underscores")


def validate_name(name):
    if not name or not name.strip():
        raise ValidationError("Name is required")
    if len(name) > 150:
        raise ValidationError("Name must be at most 150 characters")


def validate_stock_name(name):
    if not name or not name.strip():
        raise ValidationError("Stock name is required")


def validate_quantity(value, field_name="quantity"):
    if value is None:
        return 1
    try:
        qty = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a valid integer")
    if qty <= 0:
        raise ValidationError(f"{field_name} must be positive")
    if qty > 100000:
        raise ValidationError(f"{field_name} too large")
    return qty


def validate_price(value, field_name="price"):
    if value is None:
        return None
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a valid number")
    if price <= 0:
        raise ValidationError(f"{field_name} must be positive")
    return price


def validate_stock_id(stock_id):
    if stock_id is None or stock_id <= 0:
        raise ValidationError("Invalid stock ID")


def validate_messages(messages):
    if not messages:
        raise ValidationError("No messages provided")
    if not isinstance(messages, list):
        raise ValidationError("Messages must be a list")
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            raise ValidationError(f"Message at index {i} must be an object")
        if not any(k in msg for k in ("user", "bot", "role")):
            raise ValidationError(f"Message at index {i} must have 'user', 'bot', or 'role' key")


def validate_company_name(company):
    if not company or not company.strip():
        raise ValidationError("Company name is required")


def validate_analysis_params(data):
    amount = data.get('Amount', '100000')
    try:
        float(amount)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a valid number")
    term = data.get('term', 'medium-term')
    if term not in ('short-term', 'medium-term', 'long-term'):
        raise ValidationError("Term must be short-term, medium-term, or long-term")
    risk = data.get('risk', 'medium')
    if risk not in ('low', 'medium', 'high'):
        raise ValidationError("Risk must be low, medium, or high")
    frequency = data.get('frequency', 'SIP')
    if frequency not in ('lump sum', 'SIP', 'Lump Sum'):
        raise ValidationError("Frequency must be lump sum or SIP")
