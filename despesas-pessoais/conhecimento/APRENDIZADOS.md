# Aprendizados e situação do primeiro ciclo

## Fechamento manual de agosto — confirmação final de Luiz

Após receber a comparação das diferenças, Luiz respondeu “está correto, finalizamos”. A planilha final prevalece para a apresentação de agosto: financiamento R$ 1.219,50; manutenção R$ 435,00; babás R$ 2.239,97; eSocial R$ 209,14; AABB R$ 806,17. Total dos blocos R$ 15.224,56 (R$ 8.220,15 + R$ 7.004,41). As confirmações anteriores de manter R$ 4.479,94 de babás e R$ 17.608,97 no quadro pessoal ficam superadas somente neste fechamento manual. O eSocial menor é ajuste explícito do usuário, não uma regra para dividir novamente o eSocial nos próximos meses.

Os R$ 17.608,97 por documentos permanecem como auditoria em `resultados/detalhes/RESUMO_POR_DOCUMENTOS.md`; o controle de Reembolso empresa de R$ 140,00 não aparece nos blocos da imagem final. Não inferir pagamento ou novo crédito. A confirmação detalhada está em `auditoria/dados/fechamento_manual.json`, referenciada por `periodo.json`. Se houver fechamento manual, preservar o resumo final e não executar `gerar` sobre ele: qualquer recálculo por documentos deve ir aos detalhes, salvo pedido para reabrir o mês. Não reabrir dúvidas já aceitas pelo usuário nem generalizar os ajustes para os meses seguintes.

Consolidado em 10/09/2026. Referência agosto/2026; cartões do ciclo setembro/2026.

| Aprendizado | Regra vigente / efeito |
| --- | --- |
| Dois formatos de Excel | Modelo pessoal por linhas; quadro para Paloma com total e participação. Imagens de referência fornecem formato; a imagem atual preenchida e validada por Luiz também documenta seu quadro manual, separado dos documentos bancários. |
| 22 classificações de cartão | Preservadas integralmente em ESTABELECIMENTOS.md, com confirmação, hipótese e escopo. OneDrive anual; OpenAI mensal; gestor de babá; roupas/drogaria/lazer/zoológico; restaurantes do trabalho; sorvetes/padaria; filmes; outros aceitos. |
| 14 grupos do extrato | Preservados em EXTRATO_E_RATEIOS.md por ID, beneficiário, valor e decisão: acordo WALTER, Magali, devolução, AABB, temporárias, faxina, BodyCam, Outros, financiamento e condomínio. |
| Tratamentos do filho | SP SERV R$ 4.250,00 + NAOMI R$ 1.875,00 + Mario R$ 1.750,00 = R$ 7.875,00 fora do orçamento, mantidos no saldo bancário. Reembolso no Santander; PIX próprio não vira receita. |
| Reembolso e rateio | Categoria, participação e recebimento são confirmações diferentes. O valor de um PIX pode ser metade, integral, agrupado ou devolvido. Não cobrar Paloma por ausência de um crédito individual. |
| Provisão do 13º | Erro corrigido: R$ 248,45 já são a metade de Luiz, enviada ao cofrinho. Não registrar R$ 124,23 nem cobrar reembolso. Ana Vitória no passado; Bruna nos próximos aportes. |
| Catálogo contraditório | Corrigidos 99Food, ZUL, CAASP, pediatria, Shopee MeuLar, Porto Seguro, refeições AABB e restaurantes do trabalho. AMZN genérico não determina assinatura. A hipótese antiga do PIX de R$ 390,77 ficou marcada como ambígua; WELLHUB e pistas complementares foram preservados com contexto. |
| Cartão família | 3878 tem categoria no detalhe e uma única metade na linha 56; sem segundo rateio. |
| Precisão | Decimal; arredondamento por item/fonte. Preservar meios centavos no detalhe. |
| Extração | Colunas separadas nos cartões; estado de cartão/compra/internacional/futuras. O mês usa data contábil do extrato. |
| Organização | Períodos pelo mês de referência; ciclo das faturas separado; fontes, resultados, auditoria, regras e modelos em locais próprios. |

## Números conferidos, não regras de gastos futuros

- 123 registros dos cartões e 55 movimentos de agosto no Itaú.
- Totais bancários: Mastercard R$ 7.905,53; Visa R$ 936,61. Participação nos cartões R$ 7.411,62.
- Extrato: saldo anterior R$ 2.738,30; créditos R$ 19.700,54; débitos R$ 26.326,58; saldo final −R$ 3.887,74; diferença zero.
- Total pessoal atual: **R$ 17.608,97** = cartões R$ 7.411,62 + extrato R$ 10.197,35. Valor das babás confirmado por Luiz; manter os valores atuais sem nova redução.
- Linha 31: R$ 4.479,94 integrais confirmados. Quadro manual de Paloma validado: R$ 5.063,40 integrais e R$ 2.531,70 rateados. A lista anterior de R$ 567,91 fica apenas no histórico da conferência; não relançar.
- Resumo de Paloma simplificado: tabela principal, total e informativo de snacks/restaurantes R$ 1.420,71 (linhas 54+53, sem linha 55). Análises ficam em detalhes; preenchimento do Excel continua manual.

## Limites da evidência bancária e das classificações

O quadro de Paloma e o valor das babás foram conferidos manualmente por Luiz. Os vínculos abaixo registram a evidência disponível, sem impedir ou alterar o quadro já validado.

- Candidatos fortes: WALTER R$ 875,00 em 19/08; Stefann R$ 27,00 em 10/08; Magali R$ 495,06 em 31/08 (PIX de 29/08). Somam R$ 1.397,06; associação por valor/data, não confirmação do usuário.
- Magali R$ 450,00 e Ana Pau R$ 100,00 coincidem com pagamentos integrais. Créditos de R$ 1.875,30 (11/08) e R$ 250,00 (31/08, PIX de 29/08) não têm finalidade confirmada. Não repartir excedentes automaticamente.
- OSASCO MARGINAL como sorvete e Amazon Digital como compra de filme continuam hipóteses deste ciclo. MP*DAVIDELIRA, GOBR e ESTRADA ITAPECERICA permanecem em Outros conforme a orientação anterior; não reinventar identidade. AABB R$ 400,58 não foi confirmada como mensalidade.

A evidência detalhada fica em [resultados de agosto](C:/github/personal/despesas-pessoais/periodos/2026-08/resultados/RESUMO_MENSAL.md) e `auditoria/dados/`. A revisão integral anterior está em [histórico](C:/github/personal/despesas-pessoais/historico/base-completa-antes-organizacao-2026-09-10.md); ela contém instruções superadas e não é a base operacional.
