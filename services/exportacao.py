from pathlib import Path
from tempfile import gettempdir
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(relatorio):
    caminho=Path(gettempdir())/f"agrosaber-relatorio-{relatorio['id']}.pdf"
    c=canvas.Canvas(str(caminho),pagesize=A4); w,h=A4; y=h-65
    c.setTitle('Relatório AgroSaber')
    c.setFillColorRGB(.09,.29,.19); c.setFont('Helvetica-Bold',22); c.drawString(50,y,'AgroSaber'); y-=35
    c.setFillColorRGB(.15,.15,.15); c.setFont('Helvetica-Bold',14); c.drawString(50,y,relatorio['titulo']); y-=28
    def bloco(titulo, texto):
        nonlocal y
        c.setFont('Helvetica-Bold',11); c.drawString(50,y,titulo); y-=18
        c.setFont('Helvetica',10)
        for linha in quebrar(str(texto),90): c.drawString(50,y,linha); y-=15
        y-=12
    bloco('Cultura',relatorio['cultura']); bloco('Resultado',relatorio['resultado']); bloco('Pontos de atenção',relatorio['pontos_atencao']); bloco('Recomendação',relatorio['recomendacao'])
    c.setFont('Helvetica-Oblique',8); c.drawString(50,45,'Relatório demonstrativo. Não substitui avaliação de profissional habilitado.')
    c.save(); return caminho

def quebrar(texto, limite):
    palavras=texto.split(); linhas=[]; atual=''
    for p in palavras:
        if len(atual)+len(p)+1>limite: linhas.append(atual); atual=p
        else: atual=(atual+' '+p).strip()
    if atual: linhas.append(atual)
    return linhas
