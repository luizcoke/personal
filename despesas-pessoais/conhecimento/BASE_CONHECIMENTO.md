# Base de conhecimento — despesas pessoais

## Setembro/2026 — fechamento manual confirmado em 09/10/2026

Luiz confirmou condomínio pago de **R$ 1.127,81** e corrigiu AABB para **R$ 806,17**, igual ao valor de agosto, substituindo os R$ 2,00 da apuração inicial. Correções específicas deste fechamento, não regra geral de valor mensal. Não inventar data de pagamento ou modificar o extrato para ajustar o orçamento.

**Despesas finais R$ 13.950,70**: básicas R$ 7.531,66 e estilo de vida R$ 6.419,04. Receitas após descontos incluindo Alelo R$ 10.445,62; saldo orçamentário **-R$ 3.505,08**. O total documental anterior R$ 12.018,72 fica preservado na auditoria. `periodos/2026-09/periodo.json` possui fechamento manual; não regenerar por cima do relatório final. Última leitura local ainda mostrava AABB R$ 2,00, mas Luiz afirmou ter atualizado e pediu considerar os dois itens corretos: fechamento baseado na confirmação, sem nova edição da planilha.

Condomínio e AABB resolvidos. Auxílio-creche R$ 720,00 permanece em acompanhamento para solicitação em outubro, sem receita antecipada; isso não impede o fechamento de setembro. O quadro de Paloma continua uma comparação, sem nova confirmação de quitação.

## Planilha local — confirmação de Luiz, 09/10/2026

- Auxílio-creche: Luiz reafirmou R$ 720,00 e pediu aviso em todo processamento mensal quando o recebimento não for identificado. Em setembro não consta no holerite nem foi identificado no extrato Itaú recebido; não incluído na receita. Em 09/10/2026 confirmou que esqueceu de solicitar o reembolso de setembro à empresa e pretende solicitá-lo em outubro. Solicitação e recebimento ainda não comprovados; não lançar receita futura nem reabrir setembro automaticamente. Não confundir com APAE/APDEX de R$ 900,00. Créditos Avanade de R$ 895,00 e R$ 35,00 não possuem vínculo confirmado com auxílio-creche.

- Holerite integra a rotina mensal: gerar `resultados/HOLERITE.md` e atualizar receitas/descontos de `Gastos`. Setembro/2026: salário bruto R$ 15.921,97 + APAE/APDEX R$ 900,00; descontos efetivos R$ 7.387,17; líquido mensal R$ 9.434,80 (adiantamento R$ 6.368,79 + saldo R$ 3.066,01). Não descontar o adiantamento novamente. FGTS informativo, sem entrada disponível.
- VA/Alelo: Luiz pediu perguntar o valor efetivamente recebido mês a mês; não assumir o valor habitual. Setembro confirmado em 09/10/2026: R$ 910,82 + R$ 100,00 = R$ 1.010,82. A soma de folha líquida e benefício é R$ 10.445,62, com Alelo separado de dinheiro em conta.

- Arquivo de trabalho: `planilhas/Despesas dia a dia - 2026.xlsx`; a pasta permanece fora do Git.
- Ao transpor o fechamento mensal para o Excel, atualizar a coluna do mês em `Gastos` e o quadro corrente de `Gastos Apartamento` a partir de `RESUMO_PALOMA.md`, incluindo o histórico de snacks e restaurantes (53+54+55). Luiz utiliza essa aba para enviar a Paloma. A atualização não autoriza enviar mensagens nem confirma saldo devido ou quitação.
- Preservar os meses anteriores, demais abas, fórmulas e recursos nativos. Mostrar referência e pendências do quadro. Setembro foi transposto com R$ 5.568,11 totais, R$ 2.784,06 rateados e R$ 1.254,09 no informativo de alimentação.
- Os R$ 2.000,00 no Fundo de Reserva de setembro eram previsão, não aporte realizado, conforme confirmação de Luiz. Retirados de setembro; valores futuros não comprovam poupança realizada.

## Setembro/2026 — extrato e confirmações de 09/10/2026

Extrato recebido cobre 10/08–09/10; setembro usa somente 01–30/09, com 32 movimentos e 15 saldos diários conciliados. Saldo inicial -R$ 3.887,74; final -R$ 2.084,82. Relatórios em `periodos/2026-09/resultados/` e respostas por ID em `auditoria/dados/revisao_extrato_usuario.json` do mesmo período.

- WALTER, EXT-010: segunda e última parcela do acordo da ex-babá, R$ 1.750,00 em 21/09; reembolso integral de Paloma EXT-009 confirmado. Pessoal zero, sem terceira parcela ou nova cobrança.
- Babá atual via Magali, EXT-003: R$ 3.237,09 em 30/09; reembolso confirmado de Paloma EXT-004 de R$ 1.619,00. Pessoal líquido R$ 1.618,09, sem dividir novamente. Não confundir com a parcela de gestão no cartão, que permanece integral de Luiz.
- EXT-022: R$ 2.467,00 recebidos de Paloma em 10/09 são o acerto do quadro de agosto (R$ 2.466,97), confirmado por Luiz. Diferença documental R$ 0,03; não usar como abatimento adicional de setembro nem reabrir o fechamento de agosto.
- Bruna não tem eSocial, segundo declaração de Luiz; não buscar pagamento de eSocial dela como pendência recorrente. Essa declaração não é uma conclusão jurídica nem regra para outras babás. Em setembro não houve aporte à provisão do 13º; não copiar R$ 248,45 de outro mês.
- AABB: EXT-023, boleto de R$ 651,00, foi duplicado e compensado pelo clube, conforme esclarecimento de Luiz. Manter na conciliação, excluído das despesas de setembro; nenhum estorno bancário foi criado. EXT-005, PIX de R$ 2,00, é o complemento e a despesa da AABB atribuída ao mês. Destino/competência da compensação não informado; não criar despesa futura automaticamente.
- Condomínio de setembro permanece sem lançamento localizado e sem confirmação de pagamento/ausência. Amazon Digital BR de R$ 34,90 (MASTERCARD-040) foi confirmado como filme em 09/10/2026 e classificado em Lazer/Viagem (64). Os gastos que Luiz não reconheceu ficam em Outros, sem repetir a pergunta.

Total pessoal provisório atualizado: R$ 12.018,72; fontes conciliadas. O mês não recebeu confirmação de fechamento final.

## Alimentação prática — confirmação de Luiz, 13/09/2026

- PLANO-JANTAR-PESSOAS: Luiz confirmou que o jantar por delivery atende a ele e à esposa (dois adultos), e pediu usar as faturas já existentes para estimar custos. Não perguntar novamente quantidade de pessoas ou preço médio antes de consultar os lançamentos. A confirmação da rotina não prova que cada compra histórica atendeu exatamente duas pessoas.
- PLANO-JANTAR-PRATICO: delivery atende principalmente ao jantar. Luiz confirmou que refeições prontas para aquecer seriam aceitáveis para a família. A solução deve preservar praticidade, sem depender de a esposa cozinhar; não inferir que ela aprovou pessoalmente um fornecedor ou cardápio.
- Teste proposto: substituir dois jantares de delivery por semana durante duas semanas, escolhendo opções em conjunto. Frequência, datas, fornecedor e orçamento do teste ainda não foram confirmados; nenhuma compra realizada.
- O total de R$ 1.420,71 reúne restaurantes, delivery, snacks e padaria, não apenas jantares. Não usar esse total para estimar preço por pedido nem registrar economia sem medir substituições. Teto anterior de R$ 600,00 permanece hipótese, não decisão.

## Preferências do planejamento — AABB e OpenAI, 13/09/2026

- PLANO-AABB-MANTER: Luiz decidiu manter o clube, pago mensalmente, pois esposa e filha usam bastante. A família frequenta o restaurante praticamente todos os fins de semana. Mensalidade e refeições são componentes separados; manter o clube não define automaticamente teto para consumo. EXT-032 registra mensalidade de R$ 612,00; o fechamento manual da linha 57 de R$ 806,17 permanece preservado. A confirmação de uso não explica a diferença nem reclassifica MASTERCARD-002.
- PLANO-OPENAI-USO: Luiz confirmou OpenAI como mensal e em uso com Codex. Manter no cenário atual, sem economia presumida. MASTERCARD-105 (R$ 105,74) e MASTERCARD-106 (R$ 457,56) são os valores observados do ciclo; a resposta não confirma que ambas as cobranças se repetirão integralmente todos os meses. Não voltar a perguntar sobre finalidade ou periodicidade do serviço. Não inferir uso profissional ou geração de renda.
- Nenhuma mudança de categoria, rateio, valor histórico ou aceite dos tetos anteriores decorre dessas confirmações. Próxima discussão: consumo ajustável preservando as prioridades familiares e custo regular de cuidados.


## Renda e fluxo de caixa — confirmação vigente de 13/09/2026

Limite e juros atualizados por Luiz: R$ 13.900,00 de limite ainda disponível, além do valor usado, e taxa de 8% ao mês mais IOF. Ele não pretende usar todo o limite e conta com salário no dia 15 e reembolso esperado. Não interpretar limite como dinheiro próprio nem fixar data de crédito do Bradesco sem evidência. Juros são sobre o saldo utilizado, não sobre a disponibilidade. A pergunta sobre taxa mensal está resolvida; detalhes e cenários em FLUXO_DE_CAIXA.md.

RESERVA-DISPONIVEL: R$ 0,00, confirmado por Luiz. Primeira versão do [plano financeiro](../planejamento/PLANO_FINANCEIRO_INICIAL.md) consolidada com cenários, orçamento proposto e limites da informação. O extrato arquivado informa limite contratado de R$ 21.600,00; a taxa de 8% ao mês mais IOF foi informada posteriormente por Luiz. Não confundir limite com patrimônio ou disponibilidade própria.

Luiz informou não possuir patrimônio que gere renda. Registrar renda patrimonial/passiva não existente segundo sua declaração, sem inferir ausência de bens, reservas ou saldos disponíveis. Dados suficientes para diagnóstico inicial. Luiz confirmou posteriormente não ter nenhum valor disponível: reserva e saldos acessíveis fora da conta negativa de R$ 0,00 nesta data. Não perguntar novamente nem supor uso de reserva existente. Ver FLUXO_DE_CAIXA.md; não repetir a pergunta sobre renda patrimonial.

Descontos corrigidos em 13/09/2026: Luiz confirmou pensão de agosto de R$ 4.306,25 (DESC-PENSAO), substituindo R$ 2.013,87 da imagem. Agosto totaliza R$ 7.367,09 de descontos, igual a julho; Meta permanece R$ 7.422,69. Receitas da coluna Ago de R$ 17.909,55 menos descontos corrigidos resultam em R$ 10.542,46, cálculo da planilha ainda não conciliado com todos os créditos e benefícios. A pensão está resolvida; não perguntar novamente nem descontar das TEDs já líquidas. A coincidência 15.921,97 − 7.367,09 + 900,00 = 9.454,88 agora usa os descontos corrigidos de agosto e sugere APAE já incluído, mas ainda usa a base Meta e não identifica a rubrica dentro da portabilidade. Não somar APAE novamente como entrada confirmada nem deduzir descontos dos créditos já líquidos. Os cenários anteriores de renda/deficit continuam condicionais. Ver [CONFERENCIA_DESCONTOS.md](../periodos/2026-08/resultados/detalhes/CONFERENCIA_DESCONTOS.md) e os dados por ID da imagem.



Luiz confirmou que as TEDs Santander → Itaú de R$ 6.368,79 em 14/08 (EXT-042) e R$ 3.086,09 em 31/08 (EXT-011) são portabilidade do salário, já com os descontos legais. Adotar R$ 9.454,88 líquidos como referência mensal, substituindo os R$ 15.921,97 apresentados na imagem. A confirmação e os registros por ID encerram a dúvida sobre origem salarial. Não pedir novamente os valores nem aplicar nova dedução de pensão. Contar uma única receita, sem duplicar a passagem entre contas próprias.

| ID | Receita / benefício | Valor mensal R$ | Evidência e calendário |
| --- | --- | --- | --- |
| RENDA-SALARIO | Salário líquido após descontos aplicáveis | 9.454,88 | Extrato de agosto e confirmação de Luiz. R$ 6.368,79 referentes ao dia 15 e R$ 3.086,09 ao fim do mês. Datas habituais informadas: 15 e 30; em agosto, créditos em 14 e 31. |
| RENDA-AUXILIO-CRECHE | Auxílio-creche | 720,00 | Valor mensal informado; recebimento variável vinculado à solicitação. |
| RENDA-AUXILIO-APAE | Auxílio APAE | 900,00 | Diferença entre total de auxílios da imagem (1.620,00) e creche (720,00); demais benefícios no dia 30. |
| BENEFICIO-ALELO | VA + benefícios Alelo | 1.011,60 | Cartão Alelo, usado por exemplo no mercado; separar do caixa bancário. |

Somando os auxílios por fora do salário: R$ 11.074,88 em dinheiro e R$ 12.086,48 com Alelo. A inclusão dos auxílios nas TEDs deve ser conferida antes de fechar o calendário para evitar duplicidade; não presumir a finalidade das TEDs diretas da Avanade de R$ 790,00 em julho e R$ 895,00 em setembro.

Comparação com as despesas pessoais confirmadas de agosto, R$ 15.224,56: diferença de -R$ 4.149,68 no cenário de auxílios adicionais. Isso substitui a antiga sobra calculada de R$ 2.317,41. Agosto contém gastos anuais e pontuais; separar recorrência antes de projetar meses futuros. Não abater novamente o quadro de Paloma. O fechamento de despesas de agosto permanece inalterado.

Histórico da correção: a imagem foi apresentada como salário líquido de R$ 15.921,97. Luiz escolheu os valores efetivamente creditados para planejamento, por já conterem os descontos legais. Não inferir salário bruto nem decompor a diferença de R$ 6.467,09 sem holerite.

Luiz informou cheque especial de aproximadamente -R$ 7.600,00 e espera habitual de 15 a 20 dias por reembolso geralmente integral do Bradesco Saúde, sem esclarecer dias úteis/corridos. Imagem atual: três pedidos de 10/09, total apresentado de R$ 7.875,00, todos Em Análise, sem data/valor aprovado. Mastercard integral de R$ 7.905,53 vence em 15/09. A exclusão dos tratamentos do orçamento pessoal permanece; saídas e créditos efetivos devem constar no fluxo de caixa por data. Reembolsos repõem dinheiro adiantado, sem gerar nova renda livre.

Consultar [FLUXO_DE_CAIXA.md](FLUXO_DE_CAIXA.md) para pagamentos, protocolos, cálculos e próximos dados. Preservar a classificação dos demais PIX próprios; a confirmação salarial tem escopo nas TEDs identificadas, não em todas as transferências.

## Correção vigente — gestão Magali fora do quadro de Paloma

Luiz retirou Gestão Bruna/Magali, cartão 01/04 de R$ 129,46 (MASTERCARD-026), pois Paloma já pagou sua parte e essa cobrança é integralmente dele. Não cobrar novamente R$ 64,73 nem aplicar novo rateio a essa compra. Nas parcelas seguintes da mesma compra, preservar essa decisão, sem generalizar a todos os serviços/PIX de Magali. Não inventar crédito bancário ou data de recebimento.

Quadro de Paloma atualizado: R$ 4.933,94 integrais e R$ 2.466,97 rateados, substituindo os totais anteriores de R$ 5.063,40 e R$ 2.531,70. O PIX de R$ 221,64 (parte R$ 110,82) continua no quadro. A imagem atual fica em `auditoria/referencias/planilha_paloma_sem_gestao_magali.png`. O informativo calculado de snacks/restaurantes continua R$ 1.420,71; R$ 1.420,00 da imagem é apresentação manual e não altera o cálculo dos documentos. O fechamento pessoal manual de agosto não foi reaberto.

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
- Identificar cada documento, total, vencimento e todos os cartões pelos cabeçalhos. Os finais conhecidos são Mastercard de Luiz 0539, 1929 e 9871, Mastercard de Paloma 3878 e 6553; Visa de Luiz 2587 e 7396. A lista não substitui o PDF.
- Preservar originais. Desbloquear cópias quando necessário e guardar extrações na auditoria. Os utilitários existentes ficam em `C:/github/personal/.core/tools/`. A senha já configurada fica em `config.local.json` (campo `pdf_password`, arquivo local fora do Git); usar sem pedir novamente ou expô-la nos relatórios.
- Antes de importar, comparar SHA-256: um arquivo repetido não cria novas despesas. Transações legítimas iguais dentro da fonte permanecem separadas por ID/localização. `_unlocked`, textos, resumos e imagens de referência não são novas entradas.

## Regras de valores e de apresentação

- Preservar valor e sinal originais do documento; guardar participação pessoal em campo separado. Dinheiro é Decimal, não ponto flutuante.
- Usar somente a parcela cobrada agora. Próximas parcelas são acompanhamento, não gastos atuais. OneDrive anual entra pela cobrança integral, sem inventar 12 parcelas. As duas cobranças reais de OpenAI são preservadas até evidência de duplicidade.
- Estornos identificáveis reduzem a linha da compra original; Samsung → manutenção, Levi’s → compras. Compras internacionais usam BRL efetivo e cada IOF real uma única vez. Limites, CET, juros de simulação e totais futuros não são despesas.
- **Todos os cartões de Paloma — confirmação de 09/10/2026:** metade de todos os lançamentos, independentemente do estabelecimento, inclusive AABB. Finais identificados: 3878 e 6553; cadastrar outros finais somente quando a titularidade estiver identificada. Preservar precisão integral e consolidar uma única vez na linha 56, sem redistribuir por categoria nem dividir novamente. Esta confirmação amplia a regra antes restrita ao 3878; cartões de Luiz não são rateados por ela.
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
- Segundo quadro: **Snacks e restaurantes — informativo**. Regra corrigida por Luiz em 09/10/2026, vigente para setembro e próximos meses: somar **Ifood + snacks + Padaria (54) + Mercadão + feira + Bebida + rest. AABB (55) + Restaurantes (53)** pelos valores pessoais do resumo, sem novo rateio. Setembro: R$ 703,75 + R$ 344,23 + R$ 206,11 = **R$ 1.254,09**. Não incluir trabalho (42), nem duplicar categorias dos cartões de Paloma. Informativo fora do acerto. A regra anterior excluía 55; agosto permanece como fechamento histórico confirmado, sem recálculo retroativo.
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

## Planejador financeiro — criado a pedido de Luiz em 13/09/2026

Luiz pediu criar um agente no projeto baseado nos cinco textos do OCR e seguir com o plano. Perfil: `.github/agents/Planejador-Financeiro.agent.md`; skill do repositório: `.agents/skills/plano-financeiro/SKILL.md`. O método fica em `planejamento/METODO.md`, preserva os cinco roteiros e usa esta base como fonte das confirmações. Retomar o plano e as ações existentes, sem repetir entrevista. A revisão de gastos é proposta e não representa cortes aceitos ou executados. A criação não solicita agendamento, nova conversa, contratação financeira ou mensagens externas.
