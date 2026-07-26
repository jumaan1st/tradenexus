from views.auth import auth_bp
from views.stock import stock_bp
from views.analysis import analysis_bp
from views.market import market_bp
from views.bot import bot_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(bot_bp)
