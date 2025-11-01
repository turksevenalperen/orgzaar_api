from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import random

api_bp = Blueprint('api', __name__)


SERVICES = [
    {
        "id": 1,
        "name": "DJ Hizmeti (2 Saat)",
        "category": "Müzik & Sanatçı",
        "price": 5000
    },
    {
        "id": 2,
        "name": "Masa Süsleme (Romantik)",
        "category": "Dekorasyon & Süsleme",
        "price": 1500
    },
    {
        "id": 3,
        "name": "Catering (Kişi Başı)",
        "category": "Yemek & İkram",
        "price": 800
    },
    {
        "id": 4,
        "name": "Fotoğraf Çekimi (Tüm Gün)",
        "category": "Fotoğraf & Video",
        "price": 3500
    },
    {
        "id": 5,
        "name": "Düğün Pastası (3 Katlı)",
        "category": "Yemek & İkram",
        "price": 2000
    }
]


@api_bp.route('/services', methods=['GET'])
def get_services():
    """
    Tüm hizmetleri listeleyen GET endpoint
    """
    try:
        current_app.logger.info(f'Hizmetler listelendi: {len(SERVICES)} adet')
        return jsonify(SERVICES), 200
    except Exception as e:
        if not current_app.config.get('TESTING'):
            current_app.logger.error(f'Hizmetler listelenirken hata: {str(e)}')
        return jsonify({"error": "Hizmetler listelenemedi."}), 500


@api_bp.route('/bookings', methods=['POST'])
def create_booking():
    """
    Rezervasyon talebi oluşturan POST endpoint
    """
    try:
       
        data = request.get_json(force=False)
        
        # Veri yoksa hata döndür
        if data is None:
            if not current_app.config.get('TESTING'):
                current_app.logger.warning('Boş veri ile rezervasyon denemesi')
            return jsonify({
                "error": "Geçersiz veri.",
                "details": {"request": "JSON verisi gönderilmedi."}
            }), 400
        
        
        errors = validate_booking_data(data)
        
        if errors:
            if not current_app.config.get('TESTING'):
                current_app.logger.warning(f'Validasyon hatası: {errors}')
           
            first_error_field = list(errors.keys())[0]
            return jsonify({
                "error": "Geçersiz veri.",
                "details": {first_error_field: errors[first_error_field]}
            }), 400
        
       
        booking_id = random.randint(1000, 9999)
        
     
        if not current_app.config.get('TESTING'):
            current_app.logger.info(
                f'Rezervasyon oluşturuldu - ID: {booking_id}, '
                f'Tarih: {data["event_date"]}, '
                f'Hizmetler: {data["service_ids"]}'
            )
        
        return jsonify({
            "message": "Rezervasyon talebiniz alındı.",
            "booking_id": booking_id
        }), 201
        
    except Exception as e:
       
        if not current_app.config.get('TESTING'):
            current_app.logger.error(f'Rezervasyon oluşturulurken hata: {str(e)}')
        return jsonify({
            "error": "Geçersiz veri.",
            "details": {"request": "JSON verisi gönderilmedi."}
        }), 400


def validate_booking_data(data):
    """
    Rezervasyon verisini doğrula
    """
    errors = {}
    
    
    if 'service_ids' not in data:
        errors['service_ids'] = 'service_ids alanı zorunludur.'
    elif not isinstance(data['service_ids'], list):
        errors['service_ids'] = 'service_ids bir liste olmalıdır.'
    
    
    if 'event_date' not in data:
        errors['event_date'] = 'event_date alanı zorunludur.'
    else:
        
        try:
            event_date = datetime.strptime(data['event_date'], '%Y-%m-%d')
            
          
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if event_date < today:
                errors['event_date'] = (
                    'Tarih formatı YYYY-MM-DD olmalıdır ve '
                    'gelecek bir tarih olmalıdır.'
                )
        except ValueError:
            errors['event_date'] = (
                'Tarih formatı YYYY-MM-DD olmalıdır ve '
                'gelecek bir tarih olmalıdır.'
            )
    
    return errors