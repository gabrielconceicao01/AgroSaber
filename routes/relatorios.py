from flask import Blueprint, jsonify, request
from database.db import get_db
from services.diagnostico import gerar_diagnostico
bp=Blueprint('relatorios',__name__)
@bp.get('')
def listar():
    rows=get_db().execute('SELECT * FROM relatorios ORDER BY id DESC').fetchall(); return jsonify([dict(r) for r in rows])
@bp.post('')
def criar():
    d=request.get_json(silent=True) or {}
    try: resultado=gerar_diagnostico(d)
    except ValueError as e: return jsonify({'error':str(e)}),400
    db=get_db(); cur=db.execute('INSERT INTO relatorios(cultura,titulo,resultado,pontos_atencao,recomendacao,produtividade) VALUES(?,?,?,?,?,?)',(resultado['cultura'],resultado['titulo'],resultado['resultado'],resultado['pontos_atencao'],resultado['recomendacao'],resultado['produtividade'])); db.commit()
    resultado['id']=cur.lastrowid; return jsonify(resultado),201
