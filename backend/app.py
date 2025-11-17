from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
import os

# Import blueprints
from routes.auth import auth_bp
from routes.books import books_bp
from routes.transactions import transactions_bp
from routes.users import users_bp
from routes.reports import reports_bp
from routes.fines import fines_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(fines_bp, url_prefix='/api/fines')

    # Serve static files from frontend directory
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory('../frontend', filename)

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok'}), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=True)
