from services.diagnostico import gerar_diagnostico

def test_diagnostico_comparativo():
    r = gerar_diagnostico({'cultura':'Soja','produtividade':3200,'produtividade_anterior':3000})
    assert r['cultura'] == 'Soja'
    assert 'positiva' in r['resultado']
