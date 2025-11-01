from flask import Flask
from api.routes import api_bp
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    
    app = Flask(__name__)
    

    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    
    if not app.debug and not app.config.get('TESTING'):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/orgzaar_api.log', 
                                          maxBytes=10240, 
                                          backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Orgzaar API başlatıldı')
    
    
    @app.route('/')
    def index():
        return {
            "message": "Orgzaar API'ye hoş geldiniz!",
            "version": "1.0",
            "endpoints": {
                "services": "/api/v1/services (GET)",
                "bookings": "/api/v1/bookings (POST)"
            }
        }
    
   
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint bulunamadı."}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Sunucu hatası: {error}')
        return {"error": "Sunucu hatası oluştu."}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)