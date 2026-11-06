from database.db import get_db

def dashboard_data():
    db=get_db(); rows=db.execute('SELECT * FROM plantacoes').fetchall()
    return {'total_plantacoes':len(rows),'area_total':round(sum(r['area_ha'] for r in rows),1),'producao_total':round(sum(r['quantidade_kg'] for r in rows)/1000,1),'relatorios':db.execute('SELECT COUNT(*) FROM relatorios').fetchone()[0], 'recentes':[dict(r) for r in db.execute('SELECT * FROM plantacoes ORDER BY id DESC LIMIT 4')]}

def chart_data(periodo='mensal'):
    db=get_db(); culturas=['Trigo','Soja','Feijão','Arroz']; resultado={}
    for cultura in culturas:
        rows=db.execute('SELECT periodo, produtividade FROM historico_safras WHERE cultura=? ORDER BY id',(cultura,)).fetchall()
        labels=[r['periodo'] for r in rows]
        valores=[r['produtividade'] for r in rows]
        atuais=db.execute('SELECT produtividade FROM plantacoes WHERE cultura=? ORDER BY id',(cultura,)).fetchall()
        if atuais:
            media=round(sum(r['produtividade'] for r in atuais)/len(atuais),1)
            labels.append('Atual')
            valores.append(media)
        elif not rows:
            labels=['Sem dados']; valores=[0]
        resultado[cultura]={'labels':labels, 'valores':valores}
    return resultado
