import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        path = current_app.config['DATABASE']
        path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(_=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS plantacoes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL, cultura TEXT NOT NULL CHECK(cultura IN ('Trigo','Soja','Feijão','Arroz')),
      area_ha REAL NOT NULL CHECK(area_ha > 0), quantidade_kg REAL NOT NULL DEFAULT 0 CHECK(quantidade_kg >= 0),
      data_plantio TEXT NOT NULL, previsao_colheita TEXT, produtividade REAL NOT NULL DEFAULT 0,
      status TEXT NOT NULL DEFAULT 'Em desenvolvimento', observacoes TEXT DEFAULT '', criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS historico_safras (
      id INTEGER PRIMARY KEY AUTOINCREMENT, plantacao_id INTEGER,
      cultura TEXT NOT NULL, periodo TEXT NOT NULL, produtividade REAL NOT NULL,
      FOREIGN KEY(plantacao_id) REFERENCES plantacoes(id) ON DELETE SET NULL
    );
    CREATE TABLE IF NOT EXISTS relatorios (
      id INTEGER PRIMARY KEY AUTOINCREMENT, cultura TEXT NOT NULL, titulo TEXT NOT NULL,
      resultado TEXT NOT NULL, pontos_atencao TEXT NOT NULL, recomendacao TEXT NOT NULL,
      produtividade REAL DEFAULT 0, criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS configuracoes (
      chave TEXT PRIMARY KEY, valor TEXT NOT NULL
    );
    """)
    db.commit()

