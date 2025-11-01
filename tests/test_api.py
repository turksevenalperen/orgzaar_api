import pytest
import json
from datetime import datetime, timedelta
from app import create_app


@pytest.fixture
def client():
    """Test client oluştur"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestServicesEndpoint:
    """Hizmetler endpoint testleri"""
    
    def test_get_services_success(self, client):
        """Hizmetlerin başarıyla listelenmesi"""
        response = client.get('/api/v1/services')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 3
        
       
        first_service = data[0]
        assert 'id' in first_service
        assert 'name' in first_service
        assert 'category' in first_service
        assert 'price' in first_service
    
    def test_get_services_content(self, client):
        """Hizmet içeriklerinin doğruluğu"""
        response = client.get('/api/v1/services')
        data = json.loads(response.data)
        
        
        dj_service = next((s for s in data if s['id'] == 1), None)
        assert dj_service is not None
        assert dj_service['name'] == "DJ Hizmeti (2 Saat)"
        assert dj_service['category'] == "Müzik & Sanatçı"
        assert dj_service['price'] == 5000


class TestBookingsEndpoint:
    """Rezervasyon endpoint testleri"""
    
    def test_create_booking_success(self, client):
        """Başarılı rezervasyon oluşturma"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        booking_data = {
            "service_ids": [1, 3],
            "event_date": future_date,
            "notes": "Test rezervasyonu"
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'message' in data
        assert 'booking_id' in data
        assert data['message'] == "Rezervasyon talebiniz alındı."
        assert 1000 <= data['booking_id'] <= 9999
    
    def test_create_booking_without_notes(self, client):
        """Not olmadan rezervasyon (notes opsiyonel)"""
        future_date = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        
        booking_data = {
            "service_ids": [2],
            "event_date": future_date
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
    
    def test_create_booking_empty_service_ids(self, client):
        """Boş service_ids listesi (kabul edilmeli)"""
        future_date = (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
        
        booking_data = {
            "service_ids": [],
            "event_date": future_date
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
    
    def test_create_booking_missing_service_ids(self, client):
        """service_ids eksik"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        
        booking_data = {
            "event_date": future_date
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'details' in data
        assert 'service_ids' in data['details']
    
    def test_create_booking_missing_event_date(self, client):
        """event_date eksik"""
        booking_data = {
            "service_ids": [1, 2]
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'event_date' in data['details']
    
    def test_create_booking_invalid_date_format(self, client):
        """Geçersiz tarih formatı"""
        booking_data = {
            "service_ids": [1],
            "event_date": "24-12-2025"
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'event_date' in data['details']
        assert 'YYYY-MM-DD' in data['details']['event_date']
    
    def test_create_booking_past_date(self, client):
        """Geçmiş tarih"""
        past_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        
        booking_data = {
            "service_ids": [1],
            "event_date": past_date
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'event_date' in data['details']
        assert 'gelecek' in data['details']['event_date'].lower()
    
    def test_create_booking_invalid_service_ids_type(self, client):
        """service_ids liste değil"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        
        booking_data = {
            "service_ids": "1,2,3",
            "event_date": future_date
        }
        
        response = client.post(
            '/api/v1/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'service_ids' in data['details']
    
    def test_create_booking_no_json(self, client):
        """JSON gönderilmemiş"""
        response = client.post('/api/v1/bookings')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestErrorHandlers:
    """Hata yönetimi testleri"""
    
    def test_404_error(self, client):
        """Olmayan endpoint"""
        response = client.get('/api/v1/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_home_page(self, client):
        """Ana sayfa"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data