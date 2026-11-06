from app import app

def test_dashboard_page():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_api():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    assert 'total_plantacoes' in response.get_json()
