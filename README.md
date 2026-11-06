# AgroSaber 🌱

Micro SaaS demonstrativo para gestão e acompanhamento de culturas agrícolas. Projeto de portfólio com dashboard, gráficos, cadastro de plantações, diagnósticos por regras e relatórios.

## Tecnologias
- Python 3.10+
- Flask
- SQLite
- HTML, CSS e JavaScript
- Chart.js
- ReportLab (PDF)

## Executar no Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000.

O banco SQLite e os dados fictícios são criados automaticamente na primeira execução. Use Configurações > Restaurar demonstração para repor a base inicial.

## Funcionalidades
- Dashboard com indicadores e quatro gráficos de culturas.
- Cadastro, edição, pesquisa e exclusão de plantações.
- Diagnóstico demonstrativo baseado em regras transparentes.
- Histórico e exportação PDF de relatórios.
- Preferências de produtor, propriedade e unidade.

## Aviso
Os dados iniciais são fictícios. Os diagnósticos são demonstrações computacionais e não substituem avaliação de engenheiro(a) agrônomo(a), análise de solo ou recomendação técnica oficial.
