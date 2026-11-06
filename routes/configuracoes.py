from flask import Blueprint, jsonify, request
from database.db import get_db
bp=Blueprint('configuracoes',__name__)
@bp.get('')
def obter(): return jsonify({r['chave']:r['valor'] for r in get_db().execute('SELECT * FROM configuracoes')})
@bp.put('')
def salvar():
    d=request.get_json(silent=True) or {}; db=get_db()
    for k in ('produtor','propriedade','unidade'):
        if k in d: db.execute('INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES(?,?)',(k,str(d[k]).strip()))
    db.commit(); return jsonify({'message':'Configurações salvas.'})
