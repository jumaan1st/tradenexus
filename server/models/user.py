from extensions import db


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
