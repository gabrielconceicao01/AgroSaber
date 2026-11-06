from flask import Flask, render_template, jsonify, request, send_file, abort
from config import Config
from database.db import init_db, get_db, close_db
from database.seed import seed_demo
from services.indicadores import dashboard_data, chart_data
from services.diagnostico import gerar_diagnostico
from services.exportacao import gerar_pdf
from routes.plantacoes import bp as plantacoes_bp
from routes.relatorios import bp as relatorios_bp
from routes.configuracoes import bp as configuracoes_bp

app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_db)

@app.before_request
def preparar_banco():
    init_db()
    seed_demo()

@app.get('/')
def dashboard():
    return render_template('dashboard.html', page='dashboard')

@app.get('/plantacoes')
def pagina_plantacoes():
    return render_template('plantacoes.html', page='plantacoes')

@app.get('/relatorios')
def pagina_relatorios():
    return render_template('relatorios.html', page='relatorios')

@app.get('/configuracoes')
def pagina_configuracoes():
    return render_template('configuracoes.html', page='configuracoes')

@app.get('/api/dashboard')
def api_dashboard():
    return jsonify(dashboard_data())

@app.get('/api/graficos')
def api_graficos():
    return jsonify(chart_data(request.args.get('periodo', 'mensal')))

app.register_blueprint(plantacoes_bp, url_prefix='/api/plantacoes')
app.register_blueprint(relatorios_bp, url_prefix='/api/relatorios')
app.register_blueprint(configuracoes_bp, url_prefix='/api/configuracoes')

@app.post('/api/demo/reset')
def reset_demo():
    from database.seed import reset_demo_data
    reset_demo_data()
    return jsonify({'message': 'Dados de demonstração restaurados.'})

@app.post('/api/diagnostico')
def diagnostico():
    dados = request.get_json(silent=True) or {}
    try:
        return jsonify(gerar_diagnostico(dados))
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

@app.get('/api/relatorios/<int:relatorio_id>/pdf')
def baixar_pdf(relatorio_id):
    db = get_db()
    rel = db.execute('SELECT * FROM relatorios WHERE id=?', (relatorio_id,)).fetchone()
    if not rel:
        abort(404)
    caminho = gerar_pdf(dict(rel))
    return send_file(caminho, as_attachment=True, download_name=f'agrosaber-relatorio-{relatorio_id}.pdf')

@app.errorhandler(404)
def nao_encontrado(_):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Registro ou rota não encontrada.'}), 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
