# Fluxo de caixa — tratamentos, reembolsos e cheque especial

> Análise datada: os números e cenários abaixo pertencem às datas indicadas. Para valores posteriores, consultar o fechamento e o holerite do mês antes de reutilizar projeções.
## Confirmações de Luiz em 13/09/2026

- CAIXA-SALDO-20260913: saldo informado no cheque especial de aproximadamente -R$ 7.600,00; informação do usuário, sem extrato atual conciliado e sem confirmação explícita de qual conta está negativa.
- CAIXA-SALARIO-DIA15: Luiz confirmou que EXT-042 e EXT-011 são portabilidade do salário Santander → Itaú, após os descontos legais. Referência de agosto: R$ 6.368,79 em 14/08 para o adiantamento do dia 15 e R$ 3.086,09 em 31/08 para o pagamento do fim do mês; total líquido R$ 9.454,88. O calendário informado é dias 15 e 30, com pensão já descontada no fim do mês. Não dividir a renda líquida igualmente nem aplicar nova dedução de pensão. Valores de agosto são referência, não garantia de crédito futuro.
- SAUDE-PRAZO-USUAL: atualização de Luiz: geralmente recebe 100% do Bradesco Saúde em cerca de 15 a 20 dias. Substitui a estimativa anterior de aproximadamente 15 dias. Não esclareceu dias úteis/corridos nem o marco inicial exato; prazo habitual não é previsão garantida ou aprovação dos pedidos atuais.
- SAUDE-REEMBOLSO-ATUAL: imagem recebida em 13/09 mostra três pedidos solicitados em 10/09/2026, com valor apresentado total de R$ 7.875,00, todos Em Análise. Protocolos e procedimentos registrados abaixo. Valor aprovado e previsão de crédito não aparecem; não registrar recebimento nem aprovação integral.
- CAIXA-CICLO: relata que nunca sobra dinheiro; tratamento, espera do reembolso, entrada de salário e pagamento de cartão mantêm o uso recorrente do limite e a cobrança de juros. A antiga margem de R$ 2.317,41 foi superada pela confirmação salarial; a comparação de -R$ 4.149,68 frente a agosto pressupõe auxílios por fora, composição ainda pendente e questionada pela nova imagem dos descontos.

A regra anterior informa reembolsos Bradesco Saúde no Santander e posterior transferência própria ao Itaú. Não associar automaticamente os pagamentos abaixo aos pedidos ainda pendentes, nem registrar crédito recebido sem evidência.

## Pagamentos recuperados dos documentos

| Data contábil | ID na extração | Destinatário | Saída R$ |
| --- | --- | --- | --- |
| 03/08/2026 | EXT-060 | Naomi | 1.875,00 |
| 03/08/2026 | EXT-061 | SP SERV | 1.250,00 |
| 03/08/2026 | EXT-062 | Mario Pinheiro | 1.750,00 |
| 31/08/2026 | EXT-013 | SP SERV | 3.000,00 |
| 04/09/2026 | EXT-004 | Mario Pinheiro | 2.000,00 |
| 04/09/2026 | EXT-005 | Naomi | 2.875,00 |

Fontes: `../periodos/2026-08/output/.auditoria/dados/extrato_extraido.json`, movimentos e páginas; pagamentos de agosto também em `../periodos/2026-08/output/detalhes/EXTRATO.md`. A extração contém movimentos de setembro marcados `no_periodo: false`; eles não pertencem ao fechamento de agosto.

- Tratamentos pagos em agosto: R$ 7.875,00.
- Tratamentos identificados em 04/09: R$ 4.875,00; cobertura parcial de setembro.
- Bloco mais recente, de 31/08 a 04/09: R$ 7.875,00. Este total coincide numericamente com o de agosto, mas corresponde a pagamentos diferentes. Não somar os dois subtotais sobrepostos. Nenhum deles é comprovação do reembolso atualmente pendente.
- Encargos bancários debitados em agosto: juros do limite de R$ 127,82 (17/08, EXT-041) e IOF de R$ 21,04 (04/08, EXT-059), total R$ 148,86. A linha geral Juros/IOF de R$ 170,48 inclui também outros documentos; não atribuir toda a linha ao cheque especial.
- Saldo bancário do fechamento de agosto: -R$ 3.887,74. Não confundir com o saldo atual informado de aproximadamente -R$ 7.600,00.

## Pedidos apresentados no aplicativo — imagem recebida em 13/09/2026

Todos têm data de solicitação 10/09/2026 e situação Em Análise. O campo mostrado é Valor apresentado, não valor aprovado ou pago.

| Protocolo (ID) | Procedimento | Valor apresentado R$ | Situação |
| --- | --- | --- | --- |
| 2026.0003738083.00 | Psicoterapia | 3.000,00 | Em Análise |
| 2026.0003737979.00 | Fonoaudiologia | 2.000,00 | Em Análise |
| 2026.0003737888.00 | Terapia Ocupacional | 2.875,00 | Em Análise |
| Total | | 7.875,00 | Sem data de crédito informada |

Fonte: imagem enviada por Luiz, `C:/Users/ang-01/.codex/codex-remote-attachments/01a09afc-5a05-75a2-be69-0008f02aa9ec/6C06D2E6-5AE2-421D-8884-377501F84339/1-Foto-1.jpg`. Transcrição visual. Dados sem valor/data aprovados são desconhecidos, não zero.

Os valores coincidem com os pagamentos a SP SERV (31/08, R$ 3.000,00), Mario Pinheiro (04/09, R$ 2.000,00) e Naomi (04/09, R$ 2.875,00). O vínculo individual é candidato por valor e contexto; a imagem não identifica prestadores ou comprovantes vinculados. Não transformar a coincidência em conciliação documental confirmada.

Luiz atualizou a espera habitual para 15 a 20 dias, com reembolso geralmente integral. A imagem dos três protocolos continua mostrando Em Análise. Não há confirmação de dias úteis/corridos, marco inicial ou previsão específica desses pedidos; não atribuir data prometida ou valor aprovado. Apenas como cenário, se forem dias corridos a partir de 10/09, a janela aritmética seria 25 a 30/09, sem confirmação da operadora.

## Faturas e comparação inicial de caixa

- Mastercard Black: fatura integral de R$ 7.905,53 com vencimento em 15/09/2026; fonte `../periodos/2026-08/output/detalhes/MASTERCARD_BLACK.md`. No fluxo bancário considerar a saída integral se Luiz a pagar; a participação pessoal do orçamento é uma medida diferente. Identificar separadamente recebimentos de Paloma, sem duplicar abatimentos nem presumir a data.
- Visa Infinite: fatura de R$ 936,61, vencimento em 01/09, com débito dessa quantia documentado em 01/09 no extrato (EXT-010); não reapresentá-la como vencimento futuro.
- Comparação isolada, sem outros movimentos: saldo informado de -R$ 7.600,00 + R$ 7.875,00 = R$ 275,00, somente se os pedidos forem integralmente aprovados, creditados e disponibilizados na conta negativa. Juros, IOF, salário, faturas, transferências, demais entradas e saídas podem alterar esse resultado. Não apresentar R$ 275,00 como previsão de saldo real ou sobra mensal.

## Calendário de receitas — esclarecimento de Luiz em 13/09/2026

| Receita | Data informada | Valor / observação |
| --- | --- | --- |
| Adiantamento salarial | Dia 15 | R$ 6.368,79 líquidos de referência, creditados em 14/08 (EXT-042); portabilidade confirmada. |
| Restante do salário | Dia 30 | R$ 3.086,09 líquidos de referência, creditados em 31/08 (EXT-011); pensão e descontos aplicáveis já considerados. |
| Auxílio-creche | Variável, vinculado à solicitação de reembolso do auxílio | R$ 720,00 como referência mensal. Não fixar recebimento no dia 30 nem presumir crédito imediato após a solicitação. |
| Auxílio APAE e demais benefícios | Dia 30, conforme referência de Luiz a “os demais” | APAE calculado em R$ 900,00 pela diferença do total. Alelo de R$ 1.011,60 continua separado do dinheiro bancário. |

A referência de salário disponível passa a ser R$ 9.454,88, conforme créditos do extrato e confirmação de Luiz. Os R$ 15.921,97 da imagem ficam como histórico substituído para planejamento; não classificar esse número como salário bruto nem atribuir a diferença inteira à pensão sem holerite. Manter os auxílios discriminados, mas confirmar antes do calendário definitivo se algum já está embutido no pagamento final para não somá-lo duas vezes.

## Créditos salariais por portabilidade — confirmados por Luiz

Consulta feita após Luiz informar que os valores líquidos podem ser obtidos do extrato de agosto. A extração original e os dados normalizados concordam:

| Data | ID na extração | Descrição bancária | Crédito R$ |
| --- | --- | --- | --- |
| 14/08/2026 | EXT-042 | TED 033.2062.LUIZ C N | 6.368,79 |
| 31/08/2026 | EXT-011 | TED 033.2062.LUIZ C N | 3.086,09 |
| Total das duas TEDs de agosto | | | 9.454,88 |
| 15/07/2026 | EXT-081 | TED 033.2062.LUIZ C N | 6.368,79 |
| 31/07/2026 | EXT-067 | TED 033.2062.LUIZ C N | 3.086,09 |

Fontes: `../periodos/2026-08/output/.auditoria/extracao/itau_extrato_072026_unlocked.txt` (linhas 46, 111, 162 e 194) e `../periodos/2026-08/output/.auditoria/dados/extrato_extraido.json`. Luiz confirmou expressamente que EXT-042 e EXT-011 são portabilidade salarial com descontos legais. O ledger registra essa natureza por ID, mantendo os créditos fora do quadro de despesas. No planejamento, contar a renda salarial uma única vez, sem duplicar seu trânsito entre Santander e Itaú. As recorrências de julho corroboram os valores; não compõem a renda de agosto.

Os PIX próprios de R$ 1.000,00 (EXT-044) e R$ 3.880,00 (EXT-045) em 14/08 também estão classificados como transferências próprias e não foram somados às TEDs como salário. O crédito identificado diretamente com AVANADE de R$ 895,00 em 03/09 (EXT-006) está fora de agosto e tem finalidade não confirmada; o de 20/07 é R$ 790,00. Não presumir salário, auxílio-creche ou APAE para essas TEDs da empresa sem identificação.

A diferença de R$ 6.467,09 entre a imagem e os créditos foi resolvida para a escolha da base: Luiz pediu usar o salário efetivamente creditado, por já conter os descontos legais. Uma imagem posterior trouxe linhas de descontos de Meta, julho e agosto; a pensão de agosto foi corrigida por Luiz e há indício aritmético de APAE incluído na portabilidade. A discriminação está em CONFERENCIA_DESCONTOS.md. Não aplicar nova dedução aos créditos líquidos. A pergunta sobre portabilidade está encerrada.

## Descontos em azul — nova evidência e conciliação em aberto

[Conferência corrigida](../../periodos/2026-08/output/detalhes/CONFERENCIA_DESCONTOS.md): Luiz corrigiu expressamente a pensão de agosto para R$ 4.306,25. Total vigente dos descontos de agosto: R$ 7.367,09, igual ao total de julho; Meta continua R$ 7.422,69. Sobre as receitas da coluna Ago de R$ 17.909,55, a remuneração após descontos calculada é R$ 10.542,46. A antiga leitura de pensão de R$ 2.013,87 foi preservada como histórico, sem validade para planejamento. Não voltar a perguntar sobre essa correção e não descontá-la novamente das TEDs líquidas.

A conta 15.921,97 (base Meta) − 7.367,09 (descontos corrigidos de agosto) + 900,00 = 9.454,88 coincide com os créditos. É indício de APAE já incluído; manter a composição pendente, pois a base salarial vem da Meta e a imagem não demonstra a rubrica dentro da portabilidade. O salário/benefícios não devem sofrer nova dedução das linhas azuis. A comparação abaixo é um cenário histórico com auxílios adicionais, não renda confirmada. Se somente creche for adicional às TEDs, o caixa seria R$ 10.174,88 e a diferença para agosto -R$ 5.049,68, também apenas cenário.

## Comparação corrigida com agosto

| Componente | Valor R$ |
| --- | --- |
| Salário líquido confirmado | 9.454,88 |
| Auxílios creche + APAE, se adicionais aos créditos salariais | 1.620,00 |
| Renda em dinheiro nesse cenário | 11.074,88 |
| Despesas pessoais do fechamento de agosto | 15.224,56 |
| Diferença usando agosto como referência | -4.149,68 |

Alelo: R$ 1.011,60 no cartão de benefícios, separado do caixa. Total de recursos com Alelo nesse cenário: R$ 12.086,48; não tratar o benefício como dinheiro para pagar faturas ou abater novamente gastos já pagos com ele. Se algum auxílio já estiver incluído nas TEDs, a renda adicional será menor que a usada acima.

A estimativa anterior de sobra de R$ 2.317,41 está corrigida. O atraso do reembolso e a diferença entre despesas e renda precisam ser analisados separadamente. Agosto contém gastos pontuais e anuais, incluindo OneDrive de R$ 599,00 e acordo relacionado à ex-babá; não projetar automaticamente o déficit de agosto como valor fixo dos próximos meses. O total de despesas permanece o fechamento confirmado, sem novo abatimento do quadro de Paloma ou reembolso de tratamento.

Para o dia 15, apenas como cenário baseado no último crédito e na fatura atual: R$ 6.368,79 de salário menos R$ 7.905,53 do Mastercard deixa diferença de -R$ 1.536,74. Partindo do saldo aproximado de -R$ 7.600,00, seriam -R$ 9.136,74 antes de outros créditos, gastos e encargos. Recebimentos de Paloma e eventual pagamento antecipado não estão conciliados; o valor do próximo salário não foi documentado. Não apresentar esse cenário como saldo futuro garantido.

## Patrimônio e suficiência dos dados — declaração de 13/09/2026

PATRIMONIO-RENDA: Luiz informou não possuir patrimônio que gere renda. RESERVA-DISPONIVEL: em seguida confirmou “Não tenho nenhum valor disponível”; registrar R$ 0,00 de reserva e dinheiro acessível fora da conta negativa nesta data. Essas declarações não significam patrimônio bruto zero. Há financiamento de apartamento no fechamento; não inferir valor, participação patrimonial, saldo devedor ou disponibilidade para venda.

Os dados permitem iniciar o diagnóstico e a revisão do orçamento: créditos líquidos confirmados, despesas pessoais fechadas de agosto, faturas e datas conhecidas, saldo aproximado no cheque especial, pedidos de reembolso e calendário habitual de receitas. Não prometer um plano definitivo de crédito ou quitação sem conhecer seus custos e recursos disponíveis.

Disponibilidade resolvida: Luiz confirmou R$ 0,00. Não repetir perguntas sobre reservas ou renda patrimonial, nem propor usar dinheiro guardado inexistente. Para fechar a execução, completar entradas atuais de Paloma, compromissos até o próximo recebimento e composição dos benefícios. A taxa mensal de 8% mais IOF foi informada; CET e propostas alternativas só serão necessários para uma comparação de crédito. O cabeçalho do extrato arquivado informa limite total de R$ 21.600,00; é um registro documental, não consulta bancária atual.

A ausência de rendimentos patrimoniais não impede começar o plano. O inventário completo de bens pode ficar para a etapa patrimonial; primeiro concluir o diagnóstico de renda/despesa e do caixa por data com o que já está disponível. Os cenários de auxílios adicionais versus já incluídos continuam hipóteses até conciliação.

## Limite e juros — confirmação de Luiz em 13/09/2026

- LIMITE-DISPONIVEL-20260913: Luiz informou ter mais R$ 13.900,00 disponíveis no cheque especial. É limite ainda não utilizado, não saldo próprio nem limite total. Não subtrair novamente os R$ 7.600,00 dessa disponibilidade. O total histórico contratado de R$ 21.600,00 continua como dado do extrato; não reconstruir o total atual como número exato somando valores aproximados.
- TAXA-CHEQUE-ESPECIAL: 8% ao mês, mais IOF, informado por Luiz em resposta à pergunta sobre taxa mensal. Taxa de juros confirmada por declaração; IOF efetivo e CET contratual não informados. Não repetir a pergunta sobre a taxa mensal.
- DIRETRIZ-USO-LIMITE: Luiz explicitou que não pretende usar todo o limite, pois receberá salário no próximo dia 15 e espera o reembolso. O planejamento deve minimizar o uso e o tempo no saldo negativo; o limite não é orçamento disponível nem meta de empréstimo.
- EXPECTATIVA-REEMBOLSO: Luiz reforçou que receberá o reembolso. Sua frase não fixa inequivocamente o dia 15 para o crédito do Bradesco; registrar salário previsto para o dia 15 e reembolso esperado, sem inventar data. A imagem disponível continua Em Análise, sem valor/data aprovados. Crédito integral de R$ 7.875,00 é hipótese do cenário, não recebimento realizado.

Cenário isolado, com salário igual ao último e fatura integral: -7.600,00 + 6.368,79 − 7.905,53 + 7.875,00 = -R$ 1.261,74 depois desses eventos, antes de juros, IOF e demais movimentações. Se a fatura preceder o reembolso, o saldo após salário/fatura seria aproximadamente -R$ 9.136,74, aumento de uso de R$ 1.536,74 sobre a posição informada, bem abaixo do limite adicional relatado. A ordem dos créditos altera o pico negativo e os juros; não é previsão bancária garantida.

Referência simples de custo: saldo devedor constante de R$ 7.600,00 por um mês a 8% resulta em R$ 608,00 de juros, mais IOF. Saldo constante de R$ 1.261,74 por um mês resulta em aproximadamente R$ 100,94 de juros, mais IOF. Não são valores de cobrança prevista: saldo diário, períodos, encargos e condições contratuais alteram o custo efetivo. Não aplicar juros sobre todo o limite disponível.

## Tratamento no planejamento

Preservar o fechamento pessoal de agosto e sua exclusão dos tratamentos integralmente reembolsáveis. No fluxo de caixa por data, registrar separadamente o pagamento integral, o pedido, o crédito efetivo do Bradesco no Santander e a transferência entre contas próprias. Transferências próprias não criam renda; reembolsos repõem valores adiantados. Juros e IOF efetivamente cobrados são despesas. Isso complementa o orçamento, sem reclassificar ou duplicar o histórico.

O relato indica falta de dinheiro disponível durante a espera do reembolso; não prova que essa seja a única causa de não sobrar dinheiro. O valor necessário para cobrir o intervalo deve ser calculado pelo maior saldo negativo do calendário completo, considerando faturas, contas, salários, demais saldos disponíveis e reembolsos identificados. Ainda não há dados para recomendar valor ou modalidade de novo crédito.

Próximo passo: separar os gastos pontuais dos recorrentes de agosto e completar o calendário até o reembolso, usando os valores já encontrados. Confirmar somente fatos ainda não documentados: inclusão ou não dos auxílios nas TEDs líquidas, datas/valores dos recebimentos de Paloma, demais saídas atuais; CET/propostas somente para avaliar alternativas de crédito, pois os juros de 8% ao mês mais IOF estão informados. A reserva disponível já foi confirmada em R$ 0,00. Não repetir perguntas sobre portabilidade, créditos de agosto ou datas habituais do salário. O fechamento de agosto continua preservado.

## Plano inicial consolidado

[PLANO_FINANCEIRO_INICIAL.md](../../planejamento/PLANO_FINANCEIRO_INICIAL.md) contém o diagnóstico e propostas, sem execução de pagamentos, contratação de crédito, cancelamentos ou alteração do fechamento mensal. Limite histórico de R$ 21.600,00 identificado no cabeçalho do extrato; saldo ali de -R$ 9.868,02 é daquela consulta e não substitui o saldo atual de aproximadamente -R$ 7.600,00 declarado por Luiz. Posteriormente Luiz informou 8% ao mês mais IOF e R$ 13.900,00 de limite ainda disponível; CET contratual não foi apresentado.
