---
name: plano-financeiro
description: Conduz o planejamento financeiro pessoal de Luiz no projeto despesas-pessoais, usando a base e os fechamentos mensais para revisar orçamento, fluxo de caixa, reembolsos, dívidas e patrimônio. Use para continuar o plano, avaliar mudanças ou incorporar confirmações financeiras; a extração de novas faturas pertence à rotina despesas-mensais.
---

# Planejamento financeiro pessoal

O projeto está em `../../../despesas-pessoais/`, relativo a esta skill. O perfil associado é `../../../.github/agents/Planejador-Financeiro.agent.md`.

## Retomar o trabalho

Leia as [instruções do projeto](../../../despesas-pessoais/AGENTS.md), o [índice da base](../../../despesas-pessoais/.core/conhecimento/BASE_CONHECIMENTO.md) e as [ações](../../../despesas-pessoais/planejamento/ACOES.md). Depois abra somente o documento necessário à ação: plano, revisão de gastos ou fluxo de caixa. Leia o [método](../../../despesas-pessoais/planejamento/METODO.md) apenas ao aplicar um módulo ainda não consultado. Para valores atuais, conferir o fechamento e o holerite do período; as análises datadas de setembro não foram automaticamente atualizadas por um fechamento posterior. Não carregar todos os relatórios, prompts originais ou históricos. Buscar IDs e trechos relevantes antes de ler arquivos longos.

Aplique o módulo pertinente entre os cinco do método. Não exigir executar os cinco a cada resposta. Primeiro procure a informação nos arquivos e nas confirmações; pergunte apenas por fatos novos que mudem a decisão atual. Se faltarem dados, apresente cenários explícitos e avance nas análises independentes. Não solicitar de novo valores, taxa, reservas ou origem salarial já confirmados. Sugestões de tetos não são decisões aceitas nem economias realizadas.

## Contas e atualizações

- Use Decimal ou centavos inteiros. Separe receita declarada, crédito observado, previsão e hipótese; mantenha data, fonte e IDs. Salário por portabilidade conta uma vez e já contém os descontos aplicáveis. Verifique se o benefício está embutido antes de somá-lo.
- Orçamento pessoal e fluxo bancário têm bases diferentes: a fatura integral sai do banco; participações pessoais e créditos de terceiros são registrados separadamente. Reembolso de tratamento repõe o adiantamento; transferências entre contas não criam renda. Alelo é benefício separado, e limite bancário não é recurso próprio.
- Consulte `periodo.json` e respeite fechamentos manuais. O planejamento não deve rodar `gerar` sobre agosto fechado nem deduzir novamente Paloma, pensão, cartão familiar ou provisões. Mudanças de classificação de fontes usam a rotina `despesas-mensais`; preserve o histórico e valide os dados afetados.
- Use valores, prazos e condições do período. A confirmação antiga é base, não previsão automática de salário, reembolso, disponibilidade de limite ou parcela futura. Compare taxas, CET, tarifas e alternativas financeiras em fontes oficiais atuais quando a recomendação depender dessas condições.
- Atualize o mesmo plano, a revisão e as ações afetadas. Novas confirmações entram na regra existente e no dado por ID; mantenha hipóteses identificadas e remova perguntas já resolvidas do estado vigente. Não espalhe valores correntes pelo perfil ou pela skill.

## Entrega e continuidade

Explique o resultado, a ação proposta, o valor ou intervalo de efeito e o que sustenta a conta. Linke os arquivos atualizados e indique a próxima ação útil. A revisão periódica acontece quando solicitada ou ao receber novos dados; não criar automação por inferência. A criação do agente autoriza o trabalho local de análise e manutenção do plano, sem autorizar operações financeiras ou mensagens externas.
