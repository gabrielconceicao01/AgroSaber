from app import app

def test_listar_plantacoes():
    app.config['TESTING'] = True
    response = app.test_client().get('/api/plantacoes')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
