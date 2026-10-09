# Extrato e participação pessoal

## Confirmações bancárias — setembro/2026, recebidas em 09/10/2026

As confirmações abaixo encerram as dúvidas dos vínculos deste período. Originais e respostas ficam em `periodos/2026-09/auditoria/dados/revisao_extrato_usuario.json`.

| Movimento | Tratamento confirmado |
| --- | --- |
| WALTER R$ 1.750,00, EXT-010, 21/09, 02/02 | Advogado do acordo judicial da ex-babá. Paloma reembolsou integralmente via EXT-009; pessoal zero. Segunda parcela concluída, sem projetar terceira. |
| Magali R$ 3.237,09, EXT-003, 30/09 | Pagamento à babá atual. Crédito de Paloma EXT-004 de R$ 1.619,00 confirmado: pessoal R$ 1.618,09. Não aplicar outra metade nem estender a decisão da gestão no cartão a este PIX. |
| Paloma R$ 2.467,00, EXT-022, 10/09 | Acerto de agosto confirmado; diferença de R$ 0,03 para o quadro de R$ 2.466,97 preservada. Não distribuir por despesas de setembro nem marcar como crédito disponível. |
| AABB R$ 651,00, EXT-023, 10/09 | Duplicado e compensado pelo clube, conforme Luiz. Excluir da despesa de setembro, mantendo o débito bancário original; não inventar estorno ou despesa de outra competência. |
| ASSOCIA R$ 2,00, EXT-005, 29/09 | Complemento AABB confirmado. Linha 57, R$ 2,00 pessoais. Classificação deste PIX identificado, não regra para toda associação. |

Bruna não tem eSocial segundo Luiz; não tratar ausência de eSocial dela como pendência. Não generalizar a outras babás. Em setembro não foi guardada a provisão do 13º: nenhum aporte realizado nesse mês. Condomínio segue sem confirmação; não interpretar omissão da resposta como pagamento ou gasto zero.

## Cartões de Paloma — confirmação geral em 09/10/2026

Todo gasto nos cartões de Paloma é dividido 50%, inclusive AABB. Os cabeçalhos atuais identificam os finais 3878 e 6553. A regra depende da titularidade e tem precedência sobre a categoria do estabelecimento. Consolidar na linha 56, uma única metade, incluindo estornos com seus sinais; não lançar a mesma participação também em restaurantes, clube ou outra categoria. O modelo cadastra os finais conhecidos em `cartoes_paloma`; identificar o titular antes de acrescentar um novo cartão. Esta confirmação substitui a antiga restrição ao final 3878, sem reabrir agosto.

Setembro/ciclo outubro: MASTERCARD-115, AABB SP, R$ 50,00 no 6553 → R$ 25,00 pessoais. Demais lançamentos do 3878 já estavam divididos. Rateio confirmado não prova recebimento nem saldo devido.

## Correção vigente — gestão Magali fora do quadro de Paloma

Luiz retirou Gestão Bruna/Magali, cartão 01/04 de R$ 129,46 (MASTERCARD-026), pois Paloma já pagou sua parte e essa cobrança é integralmente dele. Não cobrar novamente R$ 64,73 nem aplicar novo rateio a essa compra. Nas parcelas seguintes da mesma compra, preservar essa decisão, sem generalizar a todos os serviços/PIX de Magali. Não inventar crédito bancário ou data de recebimento.

Quadro de Paloma atualizado: R$ 4.933,94 integrais e R$ 2.466,97 rateados, substituindo os totais anteriores de R$ 5.063,40 e R$ 2.531,70. O PIX de R$ 221,64 (parte R$ 110,82) continua no quadro. A imagem atual fica em `auditoria/referencias/planilha_paloma_sem_gestao_magali.png`. O informativo calculado de snacks/restaurantes continua R$ 1.420,71; R$ 1.420,00 da imagem é apresentação manual e não altera o cálculo dos documentos. O fechamento pessoal manual de agosto não foi reaberto.

As regras confirmadas mais recentes prevalecem sobre exemplos antigos. Os valores da revisão de agosto documentam aquele mês; não são novos lançamentos a criar.


> Use esta seção para mapear lançamentos do **extrato bancário** (Itaú Personnalitê) para os itens da planilha.
> Diferente do cartão, o extrato contém pagamentos de contas fixas, PIX e débitos automáticos.

### Portabilidade salarial — confirmação de Luiz em 13/09/2026

As TEDs `033.2062.LUIZ C N` de 14/08 (EXT-042, R$ 6.368,79) e 31/08 (EXT-011, R$ 3.086,09) são salário por portabilidade Santander → Itaú, confirmado por Luiz após consulta ao extrato. Somar R$ 9.454,88 como referência salarial líquida no planejamento, uma única vez; manter esses créditos fora das despesas e não duplicar com a conta de origem. Valores originais e fechamento de agosto preservados. Essa confirmação específica supera a antiga observação genérica de transferência própria para esses dois IDs, sem reclassificar os demais PIX próprios. Não deduzir novamente pensão de crédito já líquido nem pedir confirmação salarial novamente. A imagem anterior de R$ 15.921,97 deixa de ser a base de renda disponível. Os auxílios continuam discriminados, com inclusão nas TEDs ainda a conferir.

### Tratamentos do filho — reembolso integral via Bradesco/Santander

**Complemento atualizado em 13/09/2026:** Luiz informa reembolso geralmente integral pelo Bradesco Saúde em cerca de 15 a 20 dias, sem especificar dias úteis/corridos. O adiantamento dos tratamentos e essa espera afetam o caixa e, segundo Luiz, contribuem para o uso recorrente do cheque especial. Os pedidos atuais continuam Em Análise conforme a imagem disponível. Manter a exclusão no orçamento, mas incluir saídas e créditos efetivos no calendário financeiro. Ver [FLUXO_DE_CAIXA.md](FLUXO_DE_CAIXA.md). Não marcar pedidos como pagos ou pendentes só pelo valor/data dos PIX.

**Confirmado por Luiz em 10/09/2026:** pagamentos a SP SERV, NAOMI e Mario Pinheiro são tratamentos do filho, reembolsados integralmente pelo Bradesco Saúde na conta Santander. Luiz costuma transferir esse dinheiro para sua própria conta Itaú por PIX. Por decisão expressa do usuário, esses pagamentos e transferências ficam fora dos gastos da planilha.

| Contém no extrato | Tratamento na planilha |
| --- | --- |
| `PIX TRANSF SP SERV` | Excluir dos gastos: tratamento com reembolso integral |
| `PIX TRANSF NAOMI` | Excluir dos gastos: tratamento com reembolso integral; inclui o descritor NAOMI Y |
| `PIX TRANSF MARIO P` | Excluir dos gastos: Mario Pinheiro, tratamento com reembolso integral |
| `PIX TRANSF LUIZ CO` e TED entre contas próprias já mapeados | Transferências próprias, fora de despesas e receitas; podem transportar os reembolsos recebidos no Santander |

- Preservar os movimentos originais na conciliação bancária e na lista de exclusões. A exclusão é apenas do orçamento pessoal, não da soma que confere os saldos.
- Não exigir um crédito Bradesco correspondente no extrato Itaú: o usuário confirmou que o reembolso entra no Santander. Não inventar data/valor de crédito no Itaú nem abater novamente a transferência própria.
- Não estender essa exclusão a outros beneficiários sem confirmação. WALTER foi identificado como advogado do acordo judicial da ex-babá Ana Vitória; entra em Gastos Babá Isabela, conforme a revisão abaixo.
- Agosto/2026: SP SERV R$ 4.250,00 (dois PIX), NAOMI Y R$ 1.875,00 e Mario Pinheiro R$ 1.750,00; total excluído por esta regra R$ 7.875,00. Mario já estava excluído; esta confirmação retira mais R$ 6.125,00 do resumo provisório.

### Revisão do extrato confirmada por Luiz — 10/09/2026

Estas respostas substituem as hipóteses anteriores para os movimentos indicados. Os valores abaixo documentam agosto/2026, não são cobranças a criar em meses futuros.

| Resposta | Movimento / referência de agosto | Valor original R$ | Item da planilha / decisão |
| --- | --- | --- | --- |
| 1 | WALTER, 20/08, EXT-029 | 1.750,00 | Gastos Babá Isabela * — acordo judicial, parcela 01/02 |
| 2 | Magali, EXT-014 / EXT-021 / EXT-022 | 1.661,77 | Gastos Babá Isabela * — empresa que gerencia a nova babá Bruna |
| 3 | Paloma, entrada e devolução de 21/08, EXT-026 / EXT-024 | +875,00 / -875,00 | PIX enviado por engano e devolvido; excluir os dois, efeito zero |
| 4 | PAG TIT INT 001, 20/08, EXT-032 | 612,00 | CLUBE AABB — mensalidade |
| 5 | IVANEYD, EXT-030 / EXT-037 / EXT-043 | 497,71 | Gastos Babá Isabela * — babá temporária que não ficou |
| 6 | STEFANN, EXT-047 / EXT-051 | 230,40 | Gastos Babá Isabela * — babá temporária que não ficou |
| 7 | Paloma, 10/08, EXT-049 | 210,00 | Casa Faxina semanal * |
| 8 | SOS DIA, 20/08, EXT-028 | 199,00 | Casa Faxina semanal * — empresa de faxina |
| 9 | Giovann, 21/08, EXT-025 | 110,60 | Gastos Babá Isabela * — babá temporária que não ficou |
| 10 | PAGSEGURO I, 07/08, EXT-055 | 101,99 | Lazer / Viagem — compra do jogo de PC BodyCam |
| 11 | ANA PAU, data contábil 10/08, EXT-050 | 100,00 | Gastos Babá Isabela * — babá temporária que não ficou |
| 12 | LUIS CA, 20/08, EXT-027 | 70,00 | Outros — Despesas Básicas, por decisão do usuário |
| 13 | Paloma, data contábil 31/08, EXT-012 | 1.208,00 | Financiamento Apt Lapa * |
| 14 | PAG TIT INT 782995528000, 10/08, EXT-054 | 1.127,81 | Condomínio |

**Padrões para os próximos meses:** Magali (PIX) e JIM.COM* MAGALI DA (cartão) correspondem à empresa contratada que gerencia a babá Bruna, em Gastos Babá Isabela *. Os beneficiários IVANEYD, STEFANN, Giovann e ANA PAU foram identificados como babás temporárias; novas ocorrências compatíveis vão ao mesmo item, sem presumir uma contratação permanente. PIX para Paloma de R$ 210,00 correspondem à faxina semanal, além do padrão anterior de R$ 220,00. SOS DIA foi confirmado como empresa de faxina. Identificar o destinatário e o contexto, especialmente quando o descritor vier abreviado.

**Limites dos padrões:** PAG TIT INT 001 é um código genérico: a mensalidade de R$ 612,00 foi confirmada neste ciclo, mas conferir beneficiário e contexto antes de classificar outro boleto. PAGSEGURO I identifica um intermediador; BodyCam vale para este pagamento de R$ 101,99 em 07/08/2026, não para todos os PIX PagSeguro. A classificação de LUIS CA em Outros é decisão para este lançamento, não identificação de sua atividade. A mensalidade bancária da AABB não confirma a natureza da compra de R$ 400,58 no cartão, mantida conforme a regra anterior.

**Valores confirmados por Luiz — agosto/2026:** Luiz informou que o valor das babás está correto e que já lançou e conferiu Paloma. Manter R$ 4.479,94 integrais na linha 31 e total pessoal R$ 17.608,97. Não aplicar novamente os 50% do quadro de Paloma ao resumo pessoal. O quadro manual validado soma R$ 5.063,40 de gastos e R$ 2.531,70 de participação. Esta decisão resolve a pendência de participação para lançar agosto, sem converter créditos candidatos em recebimentos confirmados.

**Evidência anterior de recebimentos — agosto/2026:** `periodos/2026-08/resultados/detalhes/CONFERENCIA_REEMBOLSOS_BABAS.md` preserva a comparação dos pagamentos com os PIX. WALTER R$ 875,00, Stefann R$ 27,00 e Magali R$ 495,06 eram candidatos fortes; R$ 450,00 e R$ 100,00 coincidiam com pagamentos integrais; R$ 1.875,30 e R$ 250,00 não tinham finalidade identificada. A validação posterior do quadro manual não identifica cada vínculo nem autoriza abater créditos. Não tratar essas associações históricas como impedimento ao quadro já conferido nem cobrar novamente a antiga lista de R$ 567,91. O PIX recebido e devolvido de 21/08 permanece excluído.

**Parcela a acompanhar em setembro/2026:** WALTER é o advogado da ex-babá Ana Vitória no acordo judicial. Agosto contém a parcela **01/02**, R$ 1.750,00. Luiz informou outro pagamento em setembro, parcela **02/02**, também em Gastos Babá Isabela *. Valor e data da segunda parcela serão conferidos no extrato de setembro; não criar cobrança, não somar previsão aos gastos de agosto e não continuar a recorrência após a segunda parcela sem novo documento/instrução.

### Provisão do 13º — metade de Luiz guardada por Paloma

**Confirmado expressamente por Luiz em 10/09/2026:** o PIX de **R$ 248,45 para Paloma em 06/08/2026** (EXT-056) era a sua participação na provisão do 13º da babá **Ana Vitória**. Esse valor **já é metade** do total conjunto de R$ 496,90. Paloma recebe a parte de Luiz e guarda no cofrinho do banco, junto com a parte dela, para pagar o 13º no final do ano.

- **Orçamento pessoal:** lançar os R$ 248,45 integrais na linha 33, Gastos Babá Isabela férias *, com observação de provisão do 13º. Não dividir novamente. A rubrica mantém o nome da planilha; a finalidade confirmada do aporte é o 13º.
- **Acerto com Paloma:** não há reembolso esperado nem valor a cobrar dela por esse PIX. O movimento representa uma parte de Luiz já paga. Não classificar ausência de crédito como pendência, não procurar R$ 124,23 para abater e não incluir essa provisão na lista de valores que Paloma deve pagar.
- **Próximos aportes:** Luiz informou que precisa passar a enviar a mesma provisão para a babá **Bruna**. A referência atual da sua parte é R$ 248,45; o total conjunto correspondente é R$ 496,90. Registrar a continuidade para Bruna, preservando Ana Vitória no histórico de agosto. Um aporte futuro só entra como realizado quando houver o respectivo lançamento; não criar pagamento automático, nem assumir que a transferência para Bruna já ocorreu.
- **Uso do cofrinho:** ao conferir o pagamento do 13º no fim do ano, identificar a utilização das provisões já registradas para não contabilizar a mesma participação de Luiz duas vezes.
- **Precedência:** esta confirmação invalida a regra antiga de “Paloma reembolsa 50%” da provisão. Ela não altera a regra de eSocial nem confirma o vínculo dos outros créditos de babá.

### Regra especial — Babá (ANA VIT)

> Luiz paga o valor integral para a babá via PIX. Paloma reembolsa 50% no mesmo dia ou no dia seguinte.
> **Regra:** quando `PIX TRANSF ANA VIT` aparecer, subtrair o `PIX TRANSF PALOMA` de reembolso do mesmo período.
> Lançar apenas o **valor líquido (50%)** no item **Gastos Babá Isabela \***.

| Contém no extrato | Ação | Item na planilha |
|-------------------|------|------------------|
| `PIX TRANSF ANA VIT` | Subtrair reembolso de PALOMA no mesmo dia/semana | Gastos Babá Isabela * |

### Casa / Moradia — Contas fixas

| Contém no extrato | Exemplo real | Item na planilha |
|-------------------|-------------|------------------|
| `PAG TIT INT 742995528000` ou `782995528000` | Agosto: PAG TIT INT 782995528000, R$ 1.127,81 | Condomínio |
| `DA PMSP` | DA PMSP 095250000000946 | IPTU |
| `DA ELETROPAULO` | DA ELETROPAULO 13724657 | Luz |
| `INT /CLARO S.A` | INT /CLARO S.A 003000005 | Conta Internet + TV |
| `DA VIVO-SP` | DA VIVO-SP 11280214885 | Conta Celular |
| `PIX TRANSF PALOMA` + valor `-210,00` ou `-220,00` | Agosto: PIX TRANSF PALOMA 10/08, R$ 210,00 | Casa Faxina semanal |
| `PIX TRANSF PALOMA` + valor `-390,77` | PIX TRANSF PALOMA 15/04 | Hipótese histórica de IPVA/licenciamento; o histórico também diz “a confirmar”. Se reaparecer, confirmar a finalidade antes de aplicar a linha 34 |
| `PIX TRANSF PALOMA` + valor `-1.208,00` ou padrão anterior `-1.219,50` | Agosto: PIX TRANSF PALOMA 30/08, contabilizado em 31/08 | Financiamento Apt Lapa * (parcela mensal) |
| `PIX TRANSF PALOMA` + valor `-248,45` | PIX TRANSF PALOMA 06/08 — já é a metade de Luiz guardada no cofrinho | Gastos Babá Isabela férias * (provisão do 13º, linha 33); lançar R$ 248,45 integrais, sem reembolso |

> ⚠️ Nem todo PIX para PALOMA é igual. Diferenciar pelo **valor exato**: R$210,00 ou R$220,00 = faxina | R$1.208,00 ou padrão anterior R$1.219,50 = financiamento | R$248,45 = parte de Luiz já dividida da provisão do 13º (linha 33, valor pessoal integral). Entradas não são despesas; só usar como abatimento quando o vínculo e o rateio estiverem confirmados.

### Filhos / Educação / Cuidados

| Contém no extrato | Exemplo real | Item na planilha |
|-------------------|-------------|------------------|
| `PIX TRANSF Sonia` | PIX TRANSF Sonia p13/04 | Gastos Meninos |
| `PIX TRANSF LUIZ FE` | PIX TRANSF LUIZ FE15/04 | Gastos Meninos |

Luiz confirmou na revisão de agosto/2026 os três pagamentos em Gastos Meninos: Sonia R$ 180,00 em 03/08 e R$ 80,00 em 20/08; LUIZ FE R$ 50,00 no PIX de 15/08, contabilizado em 17/08. Total R$ 310,00, IDs EXT-063, EXT-031 e EXT-038. A confirmação valida a categoria; não especifica a finalidade individual de cada PIX.

### Cartões e Dívidas

| Contém no extrato | Exemplo real | Item na planilha |
|-------------------|-------------|------------------|
| `IOF` | IOF (débito conta) | Juros/IOF |
| `JUROS LIMITE DA CONTA` | Juros efetivamente debitados | Juros/IOF |

### Lançamentos a IGNORAR (não lançar na planilha)

| Contém no extrato | Motivo |
|-------------------|---------|
| `PERS INFINIT` | Débito automático fatura Visa Infinite — já lançada separadamente |
| `ITAU BLACK` | Débito automático fatura Mastercard Black — já lançada separadamente |
| `TED 033.2062.LUIZ C N` | Transferência entre contas próprias |
| `PIX TRANSF LUIZ CO` | Transferência entre contas próprias |
| `REND PAGO APLIC AUT MAIS` | Rendimento de aplicação automática (não é despesa) |

### Outros padrões do extrato

| Contém no extrato | Suspeita | Item na planilha |
|-------------------|----------|------------------|
| `PIX QRS CAIXA INSTA` | Loteria instantânea Caixa | Loterias |
| `PIX QRS RECEITA FED` | eSocial da babá (encargo trabalhista) — **Paloma paga 50%** | Gastos Babá Isabela Esocial * (50% líquido) |
| `PAY ASSOC` | Mensalidade AABB clube (parcelas) | CLUBE AABB (linha 57) |
| `PIX TRANSF MARIO P` | Tratamento filho (Luiz Guilherme) — **Bradesco Saúde reembolsa** | IGNORAR (não lançar) |
| `SISPAG PIX DANIELA COKE` | Entrada de dinheiro — parente/conhecida | Receita eventual |

---

### Limites de outros exemplos históricos

- Porto Seguro de abril: parcela integral de R$ 434,73, parte de Luiz de R$ 217,37. Preservar o aprendizado de divisão daquele seguro, mas valores/parcela atuais vêm da fatura. Quando a cobrança já estiver no cartão 3878, a metade da linha 56 é o único rateio, sem redução adicional. Mudança de titular/contrato deve ser conferida antes de reutilizar a divisão.
- PIX positivo de Sonia pode ser troco/estorno de Gastos Meninos, conforme o histórico. Vincular ao gasto quando identificado; não presumir nova receita ou reembolso de babá.
- Salário, auxílio creche/APAE, benefícios, horas extras, férias, 13º/PPR/IR e FGTS, assim como INSS, IR, pensão, coparticipação e plano dental, dependem de holerite/documento específico. Não preencher essas linhas a partir de PIX próprios ou saldo bancário. Apresentar receitas/descontos separadamente quando Luiz solicitar e fornecer as fontes.

## PIX de Paloma de R$ 495,06 — esclarecimento após o fechamento

Luiz informou que Paloma confirmou que o PIX de 29/08 era para babá. No Itaú foi contabilizado em 31/08, EXT-015. Finalidade babá confirmada; associação específica mais provável: Magali R$ 990,13 de 31/08, EXT-014 (metade exata R$ 495,065). Não tratar a associação específica como confirmação expressa do beneficiário sem informação adicional.

O pagamento de R$ 990,13 já estava fora do quadro de Paloma de R$ 2.531,70, pois o crédito já havia sido identificado como candidato forte. Os itens Magali presentes no quadro são outros: PIX R$ 221,64 (parte R$ 110,82) e cartão R$ 129,46 (parte R$ 64,73). Não subtrair R$ 495,06 novamente desse total com base no mesmo pagamento. Não alterar o fechamento manual de agosto por esta anotação.
