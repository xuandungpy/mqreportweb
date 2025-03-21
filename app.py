from flask import Flask
from config import Config
from controllers.auth_controller import auth_bp
from controllers.report_controller import report_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(report_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)