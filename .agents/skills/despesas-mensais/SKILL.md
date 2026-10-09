---
name: despesas-mensais
description: Processa extratos bancários, faturas e holerites do projeto despesas-pessoais, aplica a base de Luiz e atualiza os relatórios mensais, a planilha e a conferência de Paloma. Use ao receber documentos mensais ou respostas de classificação/rateio desse projeto.
---

# Despesas mensais

Projeto: `../../../despesas-pessoais/`. Ler [AGENTS.md](../../../despesas-pessoais/AGENTS.md) e o [índice da base](../../../despesas-pessoais/.core/conhecimento/BASE_CONHECIMENTO.md). Não carregar todas as referências: abrir somente a seção da fonte ou do fato tratado; usar busca por descritor/ID para detalhes.

1. Consultar `periodos/AAAA-MM/periodo.json` e, no começo de um mês, os [acompanhamentos](../../../despesas-pessoais/.core/conhecimento/ACOMPANHAMENTOS.md). Preservar fechamento manual; não executar `gerar` sobre resumo confirmado.
2. Receber documentos em `input/`, identificar referência/ciclo, comparar hashes e extrair conforme [PROCESSAMENTO.md](../../../despesas-pessoais/.core/PROCESSAMENTO.md). Manter fonte/página/ID e dados em `output/.auditoria/dados/`; senha local nunca vai aos relatórios.
3. Aplicar regras e últimas confirmações. Consultar catálogo só pelos descritores relevantes e rateios só pelos assuntos envolvidos. Participação, categoria e recebimento são distintos; não inferir quitação ou cobrança.
4. Incluir holerite e sua conferência própria. Perguntar VA/Alelo a cada mês se ainda não confirmado; procurar auxílio-creche de R$ 720,00 e avisar se não identificado. Não somar adiantamento/FGTS como nova receita nem descontar o adiantamento duas vezes. Detalhes na seção Holerites do contrato.
5. Validar pelo CLI `.core/scripts/mensal.py`; gerar os relatórios aplicáveis em `output/`. IDs/nomes vêm de `.core/modelos/planilha.json`. O quadro de Paloma usa o modelo próprio, com informativo **54+55+53**, sem segundo rateio e fora do acerto.
6. Quando solicitado, usar a skill de planilhas para atualizar o mês em `Gastos` e a conferência em `Gastos Apartamento`, preservando estrutura, recursos e outros meses. Dados e dúvidas por célula ficam no período.
7. Incorporar respostas ao mesmo dado/regra, validar os efeitos e entregar links, total, referência/ciclo e pendências materiais. Não generalizar ajuste manual de um mês. Uma versão provisória é útil; não declarar fechado, devido ou quitado sem confirmação.

Mensagens à Paloma, pagamentos ou agendamentos exigem pedido próprio. Não carregar históricos nem executar os scripts antigos na rotina.
