from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Register blueprints
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.cart_controller import cart_bp
    from app.controllers.order_controller import order_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/order')

    # Create tables
    with app.app_context():
        db.create_all()

    return app