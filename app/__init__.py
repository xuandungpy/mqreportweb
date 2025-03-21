from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Đăng ký các blueprint
    from app.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.views.vien_phi import vien_phi as vien_phi_blueprint
    app.register_blueprint(vien_phi_blueprint)
    
    return app