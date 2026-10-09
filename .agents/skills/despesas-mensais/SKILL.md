---
name: despesas-mensais
description: Processa extratos bancários, faturas e holerites do projeto despesas-pessoais, aplica a base de Luiz e atualiza os relatórios mensais, a planilha e a conferência de Paloma. Use ao receber documentos mensais ou respostas de classificação/rateio desse projeto.
---

# Despesas mensais

O projeto está em `../../../despesas-pessoais/`, relativo a esta skill. O mês da pasta é o mês de referência das despesas; o ciclo das faturas é separado.

1. Leia [AGENTS.md](../../../despesas-pessoais/AGENTS.md) e [BASE_CONHECIMENTO.md](../../../despesas-pessoais/conhecimento/BASE_CONHECIMENTO.md). Consulte as referências de estabelecimentos/rateios conforme a fonte e os acompanhamentos do próximo mês. Não carregar o histórico inteiro como instrução.
2. Receba os PDFs originais e identifique referência/ciclo. Use `scripts/mensal.py preparar --mes AAAA-MM --ciclo AAAA-MM --arquivos ...` a partir do projeto. A senha existente está em `config.local.json`; usá-la localmente apenas se necessário. Nunca copiar senha para resultados.
3. Extraia e confira o layout dos PDFs com as ferramentas disponíveis. Siga [DADOS_E_PROCESSAMENTO.md](../../../despesas-pessoais/docs/DADOS_E_PROCESSAMENTO.md) para produzir `auditoria/dados/lancamentos.json`. Scripts em `auditoria/historico/` não são o processador atual.
4. Aplique as regras e últimas confirmações. Preserve sinal, valor, fonte, página, parcela e cartão. Cartão 3878 tem uma única metade; provisão de R$ 248,45 já é metade pessoal e não requer reembolso. Pagamento de fatura e PIX próprio não são novas despesas. Candidato por valor/data não é crédito confirmado.
5. Valide e gere com `scripts/mensal.py validar --mes AAAA-MM` e `gerar --mes AAAA-MM`. Entregue `RESUMO_MENSAL.md` com os IDs/ordem de `modelos/planilha.json`, totais, origem e pendências. Prepare também `RESUMO_PALOMA.md` quando solicitado ou houver acerto a conferir, seguindo o modelo próprio e indicando o limite dos vínculos.
6. Pergunte somente por fatos novos que mudem classificação, participação ou fechamento. Continue itens conhecidos. Quando houver resposta, atualize o lançamento por ID, a regra existente com escopo/confiança e os resumos afetados. Não promover hipótese do ciclo a regra permanente.

## Holerite e transposição ao Excel

- Incluir o holerite na conferência mensal. Identificar competência e data de pagamento no documento; guardar original/hash no período e rubricas, códigos, valores e página em `auditoria/dados/holerite.json`. Seguir a seção Holerites de [DADOS_E_PROCESSAMENTO.md](../../../despesas-pessoais/docs/DADOS_E_PROCESSAMENTO.md).
- Gerar `resultados/HOLERITE.md`, com proventos, descontos, líquido, adiantamento, conferência com extrato e mapa das células da planilha. Holerite ausente deixa receitas/descontos sem conferência; não copiar previsão ou mês anterior como realizado.
- Não descontar o adiantamento duas vezes: ao lançar o bruto e os descontos efetivos do mês, o adiantamento é parte do líquido recebido, não nova despesa. FGTS e bases tributárias são informativos, não dinheiro disponível. Benefícios não presentes no recibo precisam de outra fonte ou confirmação.
- Perguntar a Luiz o VA/Alelo efetivamente recebido em cada mês, conforme preferência confirmada em 09/10/2026. Somar os componentes que ele informar; não copiar o valor habitual nem projetado como realizado. Se já confirmou o mês na conversa/base, não perguntar novamente.
- Conferir mensalmente o auxílio-creche esperado de R$ 720,00 no holerite e nos documentos bancários disponíveis. Se não houver recebimento identificado, avisar Luiz no fechamento e registrar a pendência para ele verificar a solicitação. Não somar esse valor à receita sem evidência, confundir com APAE/APDEX de R$ 900,00 ou concluir ausência em contas não fornecidas; créditos agrupados não identificados continuam inconclusivos.
- Ao atualizar o Excel local, usar a skill de planilhas, preservar fórmulas, recursos nativos e meses anteriores. Conferir os rótulos antes de mapear rubricas; separar coparticipação odontológica de saúde. Preencher receitas e descontos em `Gastos`, além das despesas e do quadro `Gastos Apartamento` conforme `RESUMO_PALOMA.md`.
- O informativo Snacks e restaurantes soma as linhas **54 + 55 + 53** do resumo pessoal (Ifood/snacks/padaria + Mercadão/feira/bebidas/restaurante AABB + restaurantes), sem novo rateio e fora do total do acerto. Aplicar a setembro/2026 e próximos meses; preservar agosto já fechado.

## Conclusão

Mostrar links para o resumo e pendências, total pessoal, período/ciclo e qualquer diferença ou confirmação material restante. Uma versão provisória é útil; não declarar quitado, devido ou fechado quando os dados não sustentam isso. Não enviar mensagens à Paloma, efetuar pagamentos ou criar agendamento sem pedido explícito.

O aprendizado fica na base do projeto; não depende da memória desta conversa. A skill orienta o agente e os scripts conferem os valores, sem prometer que qualquer layout PDF seja processado por um parser universal.
