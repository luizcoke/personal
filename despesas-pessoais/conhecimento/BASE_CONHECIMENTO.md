# Base de conhecimento — despesas pessoais

## Fechamento manual de agosto — confirmação final de Luiz

Após receber a comparação das diferenças, Luiz respondeu “está correto, finalizamos”. A planilha final prevalece para a apresentação de agosto: financiamento R$ 1.219,50; manutenção R$ 435,00; babás R$ 2.239,97; eSocial R$ 209,14; AABB R$ 806,17. Total dos blocos R$ 15.224,56 (R$ 8.220,15 + R$ 7.004,41). As confirmações anteriores de manter R$ 4.479,94 de babás e R$ 17.608,97 no quadro pessoal ficam superadas somente neste fechamento manual. O eSocial menor é ajuste explícito do usuário, não uma regra para dividir novamente o eSocial nos próximos meses.

Os R$ 17.608,97 por documentos permanecem como auditoria em `resultados/detalhes/RESUMO_POR_DOCUMENTOS.md`; o controle de Reembolso empresa de R$ 140,00 não aparece nos blocos da imagem final. Não inferir pagamento ou novo crédito. A confirmação detalhada está em `auditoria/dados/fechamento_manual.json`, referenciada por `periodo.json`. Se houver fechamento manual, preservar o resumo final e não executar `gerar` sobre ele: qualquer recálculo por documentos deve ir aos detalhes, salvo pedido para reabrir o mês. Não reabrir dúvidas já aceitas pelo usuário nem generalizar os ajustes para os meses seguintes.

Versão consolidada em 10/09/2026. Esta é a entrada da base vigente; suas referências são parte da mesma base. O histórico foi preservado para consulta, mas não fornece regras em conflito com estas.

## O que entregar a cada mês

Luiz envia extrato Itaú e faturas Mastercard/Visa; o agente processa os documentos, aplica os aprendizados e entrega uma tabela Markdown com os mesmos itens e ordem da imagem do Excel. A planilha não está conectada: a saída padrão é o `.md` para transpor os valores. Criar/alterar `.xlsx` somente quando solicitado.

- `periodos/AAAA-MM/resultados/RESUMO_MENSAL.md`: principal, uma soma por item do modelo, subtotais dos blocos e total pessoal; depois fontes e detalhamento.
- `resultados/RESUMO_PALOMA.md`: tabela curta para copiar ao Excel, **Gastos totais | Forma | Condição/parcela | Valor total | Valor rateado**, total e quadro informativo de snacks/restaurantes. Análises de PIX e fontes ficam em `resultados/detalhes/`, com no máximo um link. Não repetir pendências já resolvidas manualmente por Luiz nem supor divisão de todas as contas.
- `resultados/PENDENCIAS.md`: dúvidas que mudam o fechamento e parcelas a conferir no período seguinte. Entregar a versão provisória enquanto faltarem respostas; continuar o trabalho conhecido.
- Relatórios individuais e conciliações ficam em `resultados/detalhes/`; PDFs originais em `entradas/`; dados e extrações em `auditoria/`. Não somar novamente relatórios auxiliares.

## Fontes da verdade e precedência

1. Instrução/confirmacão mais recente de Luiz, respeitando a finalidade e o escopo informados.
2. Decisão por lançamento do período, com referência à fonte, data e distinção de categoria, participação e recebimento.
3. [Extrato e rateios](C:/github/personal/despesas-pessoais/conhecimento/EXTRATO_E_RATEIOS.md) e [estabelecimentos](C:/github/personal/despesas-pessoais/conhecimento/ESTABELECIMENTOS.md).
4. [Modelo de linhas](C:/github/personal/despesas-pessoais/modelos/planilha.json) para IDs, categorias, ordem e nomes.
5. Hipóteses/heurísticas apenas quando não houver regra confiável; sinalizar. `historico/` não prevalece sobre regra vigente.

Respostas com “acho” permanecem hipóteses do ciclo. “Deixe em Outros” resolve a apresentação daquele lançamento, sem identificar a atividade do beneficiário. Não promover comparação de valor/data a confirmação de reembolso.

## Período e identificação dos documentos

- Pasta pelo **mês de referência das despesas**: `periodos/2026-08`. O ciclo das faturas é registrado separadamente em `periodo.json` (neste primeiro caso, 2026-09).
- **Extrato:** primeiro ao último dia do mês, inclusive, pela data contábil da primeira coluna. Nome do PDF e data abreviada no PIX não definem o filtro. O PDF `itau_extrato_072026.pdf` contém julho a setembro, mas agosto usa somente 01–31/08.
- **Cartões:** convenção adotada é usar as faturas completas do ciclo enviadas, preservando parcelas atuais de compras antigas; suas datas ficam no detalhe. Uma instrução de Luiz para filtrar compras por data prevalece. Não alterar silenciosamente o critério.
- Identificar cada documento, total, vencimento e todos os cartões pelos cabeçalhos. Os finais conhecidos são Mastercard 0539, 1929, 9871 e 3878; Visa 2587 e 7396. A lista não substitui o PDF.
- Preservar originais. Desbloquear cópias quando necessário e guardar extrações na auditoria. Os utilitários existentes ficam em `C:/github/personal/.core/tools/`. A senha já configurada fica em `config.local.json` (campo `pdf_password`, arquivo local fora do Git); usar sem pedir novamente ou expô-la nos relatórios.
- Antes de importar, comparar SHA-256: um arquivo repetido não cria novas despesas. Transações legítimas iguais dentro da fonte permanecem separadas por ID/localização. `_unlocked`, textos, resumos e imagens de referência não são novas entradas.

## Regras de valores e de apresentação

- Preservar valor e sinal originais do documento; guardar participação pessoal em campo separado. Dinheiro é Decimal, não ponto flutuante.
- Usar somente a parcela cobrada agora. Próximas parcelas são acompanhamento, não gastos atuais. OneDrive anual entra pela cobrança integral, sem inventar 12 parcelas. As duas cobranças reais de OpenAI são preservadas até evidência de duplicidade.
- Estornos identificáveis reduzem a linha da compra original; Samsung → manutenção, Levi’s → compras. Compras internacionais usam BRL efetivo e cada IOF real uma única vez. Limites, CET, juros de simulação e totais futuros não são despesas.
- **Cartão 3878:** metade de todos os lançamentos, com precisão integral; no quadro principal uma única linha 56. Não redistribuir categorias nem dividir novamente. Cartões de Luiz não são rateados por essa regra.
- Arredondar para centavos uma vez por item/fonte. Em agosto, metade do cartão 3878 = R$ 1.430,525 → R$ 1.430,53. No quadro para Paloma, somar participações exatas e arredondar somente o total, como no Excel validado por Luiz. Se a soma das linhas exibidas divergir em centavos, informar em uma nota curta; não criar gasto de ajuste.
- Os 50%/30% dos blocos do Excel são metas de orçamento, não fatores de rateio. Não importar saldos, metas ou histórico de snacks das imagens. Um quadro atual preenchido e expressamente validado por Luiz pode definir a apresentação de Paloma; guardar essa confirmação separada e preservar os dados originais dos PDFs.
- Manter Outros básicos (46) e Outros de estilo de vida (66) separados. OneDrive e OpenAI ficam em Assinaturas nas linhas Excel 61 e 62; Reembolso empresa permanece complementar. Ausência de lançamento é `—`, não comprovação de gasto zero.
- Gastos de trabalho PRATUS/VERBO DIVINO/JOTASIFREITAS → linha 42; refeições AABB identificadas → 55; mensalidade confirmada → 57. Não converter a compra de R$ 400,58 em mensalidade sem confirmação.

## Extrato, exclusões e créditos

- Excluir do orçamento pagamentos das faturas (`ITAU BLACK`, `PERS INFINIT`) para não duplicar compras. Continuam na conciliação do banco.
- Excluir transferências entre contas próprias e rendimentos do quadro de despesas. Não inferir salário/receita de PIX próprios ou do saldo bancário. Receitas só são apresentadas separadamente se documentadas e solicitadas.
- SP SERV, NAOMI e Mario Pinheiro: tratamento do filho integralmente reembolsado pelo Bradesco no Santander; Luiz pediu excluir. PIX dele próprio para o Itaú também ficam fora; não exigir um crédito Bradesco no Itaú nem abater de novo.
- eSocial: despesas integrais via Receita Federal são divididas 50%. Se o crédito identificado já reduziu o débito, não dividir novamente. Um crédito só pode ser usado uma vez.
- **Provisão do 13º:** o PIX de R$ 248,45 para Paloma **já é a metade de Luiz**, guardada no cofrinho. Lançar R$ 248,45 pessoais na linha 33 (nome legado “férias”), sem reembolso ou cobrança de Paloma. Agosto pertence a Ana Vitória; próximos aportes são para Bruna. Não lançar previsão como aporte realizado nem contar o uso do cofrinho de novo como a mesma despesa.
- **Gastos de babá:** WALTER, Magali/gestão de Bruna e temporárias pertencem à linha 31. Luiz confirmou manter R$ 4.479,94 integrais no resumo pessoal de agosto, total R$ 17.608,97, e informou que já lançou e conferiu o quadro de Paloma. Não aplicar nova redução ao orçamento nem reabrir a pendência resolvida. Os 50% do quadro separado não provam recebimento bancário. Nos próximos meses, seguir as confirmações e fontes do período.
- **Devolução de PIX:** em 21/08, +R$ 875 e −R$ 875 de Paloma são envio por engano e devolução, efeito zero. Não usar esse crédito como reembolso; o R$ 875 de 19/08 é outro movimento.
- Despesa sem categoria → Outros provisório. Despesa com categoria definida mas rateio incerto → categoria correta, com participação provisória. Crédito sem vínculo não prova quitação ou dívida; informar a dúvida e não distribuir diferenças por suposição.

## Aprendizado do primeiro ciclo e próximos passos

As 22 respostas sobre cartões e as 14 sobre o extrato estão preservadas nas referências da base. O [registro de aprendizados](C:/github/personal/despesas-pessoais/conhecimento/APRENDIZADOS.md) resume as correções, os limites e as pendências atuais. [Acompanhamentos](C:/github/personal/despesas-pessoais/conhecimento/ACOMPANHAMENTOS.md) registra WALTER 02/02 em setembro e a continuidade da provisão para Bruna.

Ao receber uma resposta nova: atualizar a regra existente com escopo/confiança, ajustar o lançamento pelo ID, recalcular os resumos e conferir os totais. Não acumular instruções contraditórias ou deixar uma versão antiga como regra ativa.

## Quadro simples de Paloma — confirmado em 10/09/2026

- Entregar tabela principal com gastos, forma, parcela, valor total e valor rateado; total ao final. Análises de PIX, textos de cobrança, histórico e fontes detalhadas ficam fora do resumo para copiar.
- Segundo quadro: **Snacks e restaurantes — informativo**. Luiz confirmou somar apenas **Ifood + snacks + Padaria (54) + Restaurantes (53)** pelos valores do resumo pessoal. Agosto: R$ 1.100,39 + R$ 320,32 = **R$ 1.420,71**. Não incluir 55 (Mercadão/feira/bebidas/AABB), trabalho (42), novo rateio ou duplicação das categorias do 3878. Não somar esse informativo ao acerto.
- Quadro manual de agosto validado: R$ 5.063,40 integrais e R$ 2.531,70 rateados. As linhas exibidas somam R$ 2.531,71; a diferença de R$ 0,01 é arredondamento de exibição, pois o Excel soma as metades exatas.
- A imagem atual, IDs e particularidades ficam em `periodos/2026-08/auditoria/dados/confirmacao_paloma.json` e `resultados/detalhes/CONFERENCIA_PLANILHA_PALOMA.md`. Campos Forma/parcela do controle manual não alteram os registros originais do extrato/fatura.
- Luiz continuará preenchendo o Excel manualmente para conferir; atualização direta da planilha fica para um pedido futuro.

## Fechamento verificável

Validar o total integral por fatura e cartão antes do rateio; validar saldo inicial + todos os movimentos contábeis = saldo final, e os saldos diários quando disponíveis. Toda despesa incluída tem fonte, página, ID único e uma única linha do modelo. Separar conciliação bancária, valor pessoal e acerto com Paloma.

O comando em `scripts/mensal.py` prepara o período, verifica os dados normalizados e gera o quadro principal. A extração e a identificação de layouts continuam sendo feitas pelo agente, com inspeção do PDF e ferramentas de PDF; os scripts do primeiro dia são históricos, não um leitor genérico comprovado para qualquer banco. Se o layout mudar, adaptar a extração e fechar os totais antes de concluir.

A rotina autorizada é processar os arquivos quando enviados, atualizar a base e criar os relatórios. Não há agendamento, envio de mensagens à Paloma, pagamento bancário ou publicação automática.

## Novas linhas de assinaturas — imagem final de agosto

OneDrive anual e OpenAI mensal passaram ao bloco Assinaturas, nas linhas Excel 61 e 62. O modelo usa `linha` como ID estável e `linha_excel` para a posição de exibição; os IDs citados nas regras e lançamentos continuam válidos. Spotify, Apple, Netflix, Lazer, Loterias e Outros aparecem nas linhas Excel 63–68. Fundo de Reserva não está visível no recorte; não inferir a nova posição. Reembolso empresa segue complementar.

A imagem preenchida foi preservada em `periodos/2026-08/auditoria/referencias/planilha_mensal_preenchida.png`. Há diferenças de valores em relação ao resumo (incluindo eSocial já rateado); registradas em `resultados/detalhes/CONFERENCIA_PLANILHA_FINAL.md`. Não transformar essas divergências em novas regras sem esclarecer a intenção.
