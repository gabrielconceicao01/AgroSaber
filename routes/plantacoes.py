from flask import Blueprint, request, jsonify
from database.db import get_db
from models.plantacao import CULTURAS, STATUS
bp = Blueprint('plantacoes', __name__)
CAMPOS = ('nome','cultura','area_ha','quantidade_kg','data_plantio','previsao_colheita','produtividade','status','observacoes')
def validar(d):
    if not d.get('nome','').strip(): raise ValueError('Informe o nome da plantação.')
    if d.get('cultura') not in CULTURAS: raise ValueError('Selecione uma cultura válida.')
    for campo in ('area_ha','quantidade_kg','produtividade'):
        try: d[campo] = float(d.get(campo,0) or 0)
        except (TypeError,ValueError): raise ValueError(f'O campo {campo} precisa ser numérico.')
    if d['area_ha'] <= 0 or d['quantidade_kg'] < 0 or d['produtividade'] < 0: raise ValueError('Área deve ser maior que zero; quantidades não podem ser negativas.')
    if not d.get('data_plantio'): raise ValueError('Informe a data do plantio.')
    if d.get('status') not in STATUS: d['status'] = 'Em desenvolvimento'
    return d
@bp.get('')
def listar():
    db=get_db(); rows=db.execute('SELECT * FROM plantacoes ORDER BY id DESC').fetchall(); return jsonify([dict(r) for r in rows])
@bp.post('')
def criar():
    d=request.get_json(silent=True) or {}
    try: d=validar(d)
    except ValueError as e: return jsonify({'error':str(e)}),400
    db=get_db(); db.execute(f"INSERT INTO plantacoes ({','.join(CAMPOS)}) VALUES ({','.join('?' for _ in CAMPOS)})", [d.get(c,'') for c in CAMPOS]); db.commit()
    return jsonify({'message':'Plantação cadastrada.','id':db.execute('SELECT last_insert_rowid()').fetchone()[0]}),201
@bp.put('/<int:pid>')
def editar(pid):
    d=request.get_json(silent=True) or {}
    try: d=validar(d)
    except ValueError as e: return jsonify({'error':str(e)}),400
    db=get_db()
    if not db.execute('SELECT id FROM plantacoes WHERE id=?',(pid,)).fetchone(): return jsonify({'error':'Plantação não encontrada.'}),404
    db.execute('UPDATE plantacoes SET '+','.join(f'{c}=?' for c in CAMPOS)+' WHERE id=?',[d.get(c,'') for c in CAMPOS]+[pid]); db.commit(); return jsonify({'message':'Plantação atualizada.'})
@bp.delete('/<int:pid>')
def excluir(pid):
    db=get_db(); cur=db.execute('DELETE FROM plantacoes WHERE id=?',(pid,)); db.commit()
    if not cur.rowcount: return jsonify({'error':'Plantação não encontrada.'}),404
    return jsonify({'message':'Plantação excluída.'})
