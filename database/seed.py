from database.db import get_db

def seed_demo():
    db = get_db()
    marcado = db.execute("SELECT valor FROM configuracoes WHERE chave='demo_initialized'").fetchone()
    if not marcado:
        inserir_demo(db)
        db.execute("INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES ('demo_initialized','1')")
        db.commit()

def inserir_demo(db):
    plantacoes = [
      ('Talhão Horizonte','Soja',18,42000,'2026-10-10','2027-02-20',3200,'Em desenvolvimento','Acompanhamento demonstrativo de umidade.'),
      ('Área Santa Luzia','Trigo',12,26000,'2026-09-15','2027-01-10',2800,'Em desenvolvimento','Registro fictício para demonstração.'),
      ('Talhão Primavera','Feijão',8,13500,'2026-10-01','2026-12-20',1680,'Atenção','Exemplo de ocorrência: observar uniformidade.'),
      ('Várzea do Norte','Arroz',22,51000,'2026-08-20','2027-01-25',5100,'Em desenvolvimento','Área demonstrativa irrigada.'),
      ('Talhão 05','Soja',14,31000,'2026-10-18','2027-02-28',2950,'Planejada','Plantio recente, dados ilustrativos.'),
    ]
    db.executemany("""INSERT INTO plantacoes (nome,cultura,area_ha,quantidade_kg,data_plantio,previsao_colheita,produtividade,status,observacoes)
      VALUES (?,?,?,?,?,?,?,?,?)""", plantacoes)
    historico = []
    series = {'Trigo':[2200,2350,2480,2600,2800], 'Soja':[2600,2750,2900,3050,3200], 'Feijão':[1500,1580,1620,1550,1680], 'Arroz':[4300,4500,4700,4900,5100]}
    periodos = ['Jun','Jul','Ago','Set','Out']
    for cultura, valores in series.items():
        historico.extend([(None,cultura,p,v) for p,v in zip(periodos,valores)])
    db.executemany('INSERT INTO historico_safras (plantacao_id,cultura,periodo,produtividade) VALUES (?,?,?,?)', historico)
    db.execute("INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES ('produtor','Produtor demonstrativo')")
    db.execute("INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES ('propriedade','Fazenda Modelo')")
    db.execute("INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES ('unidade','kg')")
    db.commit()

def reset_demo_data():
    db = get_db()
    for table in ('historico_safras','relatorios','plantacoes','configuracoes'):
        db.execute(f'DELETE FROM {table}')
    db.execute("DELETE FROM sqlite_sequence WHERE name IN ('plantacoes','historico_safras','relatorios')")
    inserir_demo(db)
    db.execute("INSERT OR REPLACE INTO configuracoes(chave,valor) VALUES ('demo_initialized','1')")
    db.commit()
