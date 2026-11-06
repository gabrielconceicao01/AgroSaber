CULTURAS={'Trigo','Soja','Feijão','Arroz'}
def gerar_diagnostico(dados):
    cultura=dados.get('cultura');
    if cultura not in CULTURAS: raise ValueError('Selecione uma cultura válida.')
    try: produtividade=float(dados.get('produtividade',0) or 0)
    except (TypeError,ValueError): raise ValueError('Produtividade precisa ser numérica.')
    if produtividade < 0: raise ValueError('Produtividade não pode ser negativa.')
    anterior=dados.get('produtividade_anterior')
    if anterior not in (None,''):
        try: anterior=float(anterior)
        except (TypeError,ValueError): raise ValueError('Produtividade anterior inválida.')
    else: anterior=None
    if anterior and anterior > 0:
        variacao=(produtividade-anterior)/anterior*100
        if variacao >= 5: resultado=f'Evolução positiva de {variacao:.1f}% em relação ao valor de referência.'; atencao='Manter o acompanhamento periódico e conferir se os registros usam a mesma unidade e metodologia.'
        elif variacao <= -5: resultado=f'Redução de {abs(variacao):.1f}% em relação ao valor de referência.'; atencao='Verificar os registros de campo e investigar possíveis fatores associados antes de concluir a causa.'
        else: resultado=f'Indicador relativamente estável ({variacao:+.1f}%).'; atencao='Acompanhar os próximos registros para confirmar a tendência.'
    else:
        resultado='Primeiro registro recebido. Ainda não há histórico suficiente para comparar a evolução.'; atencao='Cadastre medições em períodos diferentes para habilitar a comparação.'
    recomendacao='Este resultado é uma análise automática dos números informados. Confira os dados de campo e consulte um profissional habilitado para decisões agronômicas.'
    return {'cultura':cultura,'titulo':f'Diagnóstico demonstrativo — {cultura}','resultado':resultado,'pontos_atencao':atencao,'recomendacao':recomendacao,'produtividade':produtividade}
