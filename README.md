# Orgzaar Mini API Projesi

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen.svg)](./tests/)

Etkinlik hizmeti listeleme ve rezervasyon talebi alma işlevlerine sahip profesyonel Flask API. 

## Gereksinimler

- **Python 3.7+** 
- **pip** (Python package manager)

## Kurulum ve Çalıştırma (2 Yöntem)

### YÖNTEM 1: Git ile (Önerilen)
```bash
git clone https://github.com/turksevenalperen/orgzaar_api.git
cd orgzaar_api
pip install -r requirements.txt
```

### YÖNTEM 2: ZIP İndirme (Git Olmayanlara)
1. **ZIP İndir** 
2. **Klasörü Aç:** `orgzaar_api-main` klasörüne git
3. **Terminal Aç:** Klasörde PowerShell/CMD aç
4. **Kurulum:**
```bash
pip install -r requirements.txt
```

## API'yi Çalıştır
```bash
python app.py
```

**Görmesi Gereken:**
```
* Running on http://localhost:5000
* Press CTRL+C to quit
```

## Özellikler

- **Flask Blueprints** - Modüler ve ölçeklenebilir yapı
- **Comprehensive Validation** - Gelişmiş veri doğrulama sistemi
- **Professional Logging** - RotatingFileHandler ile log yönetimi
- **Unit Testing** - %100 test coverage (13 test)
- **Error Handling** - Detaylı hata yönetimi ve raporlama
- **RESTful Design** - Standart HTTP kodları ve JSON formatları

## Endpoints

### GET /api/v1/services
Hizmetleri listeler.

### POST /api/v1/bookings
Rezervasyon talebi oluşturur.

## Hızlı Test

### Browser'da Test Et

**Ana Sayfa:** http://localhost:5000
```json
{
  "message": "Orgzaar API'ye hoş geldiniz!",
  "version": "1.0",
  "endpoints": {
    "services": "/api/v1/services (GET)",
    "bookings": "/api/v1/bookings (POST)"
  }
}
```

**Hizmetler:** http://localhost:5000/api/v1/services
```json
[
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
```

### Unit Testleri
```bash
pytest tests/ -v
```

**Beklenen:**
```
============= 13 passed in 0.94s =============
```

## API Dokumentasyonu

### Rezervasyon Oluştur
```http
POST http://localhost:5000/api/v1/bookings
Content-Type: application/json
```

**İstek Formatı:**
```json
{
  "service_ids": [1, 3],
  "event_date": "2025-12-24",
  "notes": "Yılbaşı kutlaması için."
}
```

**Başarılı Yanıt (201 Created):**
```json
{
  "message": "Rezervasyon talebiniz alındı.",
  "booking_id": 5678
}
```

## Validation Kuralları

### service_ids
- **Zorunlu alan**
- **Liste formatında olmalı**
- **Boş liste kabul edilir**

### event_date
- **Zorunlu alan**
- **YYYY-MM-DD formatında**
- **Gelecek tarih olmalı**
- **datetime.strptime ile doğrulanır**

### notes
- **Opsiyonel alan**
- **Herhangi bir string değer**

## Hata Yanıtları

### 400 Bad Request - Validation Hatası
```json
{
  "error": "Geçersiz veri.",
  "details": {
    "event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."
  }
}
```

### 404 Not Found - Endpoint Bulunamadı
```json
{
  "error": "Endpoint bulunamadı."
}
```

### 500 Internal Server Error - Sunucu Hatası
```json
{
  "error": "Sunucu hatası oluştu."
}
```

## Test Senaryoları

API'yi test etmek için aşağıdaki PowerShell komutlarını kullanabilirsiniz:

### Başarılı Rezervasyon
```powershell
$headers = @{"Content-Type" = "application/json"}
$body = '{"service_ids": [1, 3], "event_date": "2025-12-25", "notes": "Test rezervasyon"}'
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/bookings" -Method POST -Headers $headers -Body $body
```

### Geçersiz Tarih Formatı
```powershell
$headers = @{"Content-Type" = "application/json"}
$body = '{"service_ids": [1], "event_date": "25-12-2025"}'
try { 
    Invoke-RestMethod -Uri "http://localhost:5000/api/v1/bookings" -Method POST -Headers $headers -Body $body 
} catch { 
    $_.ErrorDetails.Message 
}
```

### Geçmiş Tarih
```powershell
$headers = @{"Content-Type" = "application/json"}
$body = '{"service_ids": [1], "event_date": "2024-01-01"}'
try { 
    Invoke-RestMethod -Uri "http://localhost:5000/api/v1/bookings" -Method POST -Headers $headers -Body $body 
} catch { 
    $_.ErrorDetails.Message 
}
```

## Unit Test Sonuçları

```bash
============================================= test session starts =============================================
collected 13 items

tests/test_api.py::TestServicesEndpoint::test_get_services_success PASSED                    [  7%]
tests/test_api.py::TestServicesEndpoint::test_get_services_content PASSED                    [ 15%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_success PASSED                  [ 23%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_without_notes PASSED            [ 30%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_empty_service_ids PASSED        [ 38%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_missing_service_ids PASSED      [ 46%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_missing_event_date PASSED       [ 53%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_invalid_date_format PASSED      [ 61%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_past_date PASSED                [ 69%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_invalid_service_ids_type PASSED [ 76%]
tests/test_api.py::TestBookingsEndpoint::test_create_booking_no_json PASSED                  [ 84%]
tests/test_api.py::TestErrorHandlers::test_404_error PASSED                                  [ 92%]
tests/test_api.py::TestErrorHandlers::test_home_page PASSED                                  [100%]

============================================= 13 passed in 0.94s =============================================
```

## Proje Yapısı

```
orgzaar_api/
├── app.py                 # Ana uygulama dosyası
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Proje dokümantasyonu
├── api/
│   ├── __init__.py
│   └── routes.py         # API endpoint'leri
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Unit testler
└── logs/
    └── orgzaar_api.log   # Uygulama logları
```

## Loglama

Uygulama `logs/orgzaar_api.log` dosyasına aşağıdaki bilgileri kaydeder:

- API başlatma
- Hizmet listeleme istekleri
- Rezervasyon oluşturma işlemleri
- Validation hataları
- Sistem hataları

**Log Format:**
```
2025-11-01 16:08:12,879 INFO: Rezervasyon oluşturuldu - ID: 5678, Tarih: 2025-12-25, Hizmetler: [1, 3] [in routes.py:89]
```


