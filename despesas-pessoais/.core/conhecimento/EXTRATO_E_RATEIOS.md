# Extrato e rateios — regras vigentes

Consulta por assunto/beneficiário. Valores e recebimentos vêm dos documentos e decisões por ID do mês. Exemplos antigos não são novos lançamentos; fechamento manual prevalece sobre o total documental daquele mês.

## Cartões e Paloma

Todos os gastos de cartões de Paloma (3878/6553 conhecidos), inclusive AABB, recebem uma única metade na linha 56, preservando sinais dos estornos. Identificar novos titulares. Não redistribuir pelas categorias nem dividir novamente. Rateio não comprova recebimento.

**Gestão Bruna/Magali no cartão de Luiz:** compra de R$ 129,46, agosto 01/04 e setembro 02/04, é integralmente de Luiz porque Paloma já pagou sua parte. Preservar nas parcelas da mesma compra, incluindo crédito de R$ 0,06 em setembro. Não cobrar novamente R$ 64,73 nem generalizar a outros PIX/serviços Magali.

**Porto Seguro:** rateio antigo de 50% confirmado; usar parcela/valor da fatura atual. No cartão de Paloma, linha 56 já contém a única metade. Conferir mudança de contrato/titular.

## Exclusões, renda e tratamentos

| Descritor/contexto | Tratamento |
| --- | --- |
| `ITAU BLACK`, `PERS INFINIT` | Pagamento de fatura, fora das despesas já contadas nas compras; manter no saldo bancário |
| `PIX TRANSF LUIZ CO`, transferências próprias | Não criam renda/despesa; não duplicar passagem entre contas |
| `TED 033.2062.LUIZ C N` | Portabilidade salarial nos IDs confirmados; conferir com holerite e contar uma vez, sem descontar pensão novamente |
| `REND PAGO APLIC AUT MAIS` | Não é despesa; saldo e limite não são renda |
| SP SERV, NAOMI/NAOMI Y, MARIO P | Tratamentos do filho: exclusão do orçamento por decisão de Luiz, com reembolso Bradesco no Santander. Preservar saídas/créditos reais no fluxo, sem exigir crédito Bradesco no Itaú |

Reembolso repõe adiantamento, não renda livre. Prazo informado em 13/09/2026: geralmente 15–20 dias, sem definição de úteis/corridos; não presumir aprovação. Protocolos/saldos em [FLUXO_DE_CAIXA.md](FLUXO_DE_CAIXA.md), sempre respeitando a data da evidência.

## Babás, eSocial e provisão

| Beneficiário/rubrica | Regra |
| --- | --- |
| Magali por PIX; JIM.COM* MAGALI DA | Gastos Babá Isabela (31); distinguir salário, gestão e reembolso |
| IVANEYD, STEFANN, Giovann, ANA PAU | Temporárias identificadas em agosto; novas ocorrências compatíveis em 31, sem presumir vínculo permanente |
| ANA VIT | Participação histórica de 50%; vincular crédito somente quando confirmado, não só pela data |
| WALTER | Advogado do acordo judicial da ex-babá em 31; parcela 02/02 concluída em setembro, sem terceira prevista |
| Receita Federal/eSocial identificado | Linha 32, participação 50%; se crédito já reduziu o débito, não dividir de novo. Código genérico não comprova finalidade |
| Bruna | Luiz declarou que não tem eSocial; não repetir como pendência nem generalizar a outras babás |
| Provisão R$ 248,45 para Paloma | Já é a metade de Luiz no cofrinho, linha 33 integral, sem reembolso. Agosto para Ana Vitória; novos aportes previstos para Bruna entram somente se realizados |

Ao usar o cofrinho no 13º, não contar novamente a participação provisionada. Não cobrar Paloma por ausência de crédito individual. Crédito utilizado uma vez; PIX devolvido não quita outra despesa; excedentes não são distribuídos por suposição.

## Contas e família

| Descritor/contexto | Linha ou tratamento |
| --- | --- |
| PAG TIT INT 742995528000 / 782995528000 | Condomínio (22); conferir beneficiário, não copiar valor antigo |
| DA PMSP | IPTU (23) |
| DA ELETROPAULO | Luz (24) |
| DA VIVO-SP | Celular (25) |
| INT /CLARO S.A; PIX AUT CLARO | Internet/TV (26) |
| PIX Paloma R$ 210/220; SOS DIA | Faxina (28), segundo padrão confirmado e contexto |
| PIX Paloma R$ 1.208 / R$ 1.219,50 | Financiamento (21), segundo padrão e contexto |
| PIX Paloma R$ 390,77 | Hipótese antiga de IPVA/licenciamento; confirmar antes de aplicar 34 |
| Sonia e LUIZ FE | Gastos Meninos (29); positivo de Sonia pode ser troco/estorno, vincular antes de tratar como renda |
| IOF; JUROS LIMITE DA CONTA | Linha 45, só débitos efetivos |
| PAY ASSOC; boleto AABB identificado | Clube (57); refeições de cartão são 55, respeitando a precedência de titularidade |
| PIX QRS CAIXA INSTA | Pista de loteria; conferir contexto |
| SISPAG PIX DANIELA COKE | Entrada histórica; confirmar finalidade antes de registrar renda |

Valor de PIX é indício dentro do padrão, não identificação isolada. PAG TIT INT 001 e PagSeguro são genéricos: AABB R$ 612 e BodyCam R$ 101,99 foram decisões específicas de agosto. LUIS CA em Outros é decisão do lançamento, sem identificar atividade.

## Meses fechados

Consultar [agosto](../../periodos/2026-08/output/.auditoria/dados/fechamento_manual.json) ou [setembro](../../periodos/2026-09/output/.auditoria/dados/fechamento_manual.json) para ajustes finais. Não repetir totais provisórios como regras atuais.

Setembro: WALTER reembolsado integralmente, Magali com crédito confirmado, acerto de agosto recebido, condomínio/AABB ajustados manualmente. Vínculos na [revisão do extrato](../../periodos/2026-09/output/.auditoria/dados/revisao_extrato_usuario.json). Ajuste orçamentário não cria débito bancário.

Agosto: Paloma R$ 495,06 tem finalidade babá confirmada; associação a Magali R$ 990,13 é provável, não confirmação do beneficiário. Pagamento já fora do quadro, sem novo abatimento. Demais candidatos em [conferência de reembolsos](../../periodos/2026-08/output/detalhes/CONFERENCIA_REEMBOLSOS_BABAS.md); não reabrir o fechamento por eles.
