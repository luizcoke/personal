# Classificações do site Dia a dia · Gastos

Luiz pediu em 16/11/2026 para consultar as categorias e observações que já registrou no site antes de perguntar novamente sobre lançamentos.

Projeto local `sites/gastos-dia/`, a partir da raiz do repositório; identificar o projeto pela `.openai/hosting.json` vigente. Consultar em modo somente leitura as ferramentas Sites `read_database_overview` e `read_database_table_rows`. Usar binding/tabelas devolvidos e paginação `next_offset`, sem calcular offsets. Tabelas relevantes: entries, rules e spending_periods. Não precisa alterar/publicar o site para processar documentos.

Usar registros ativos, não teste e revisados. Vincular por descritor, data, titular/cartão e valor, aceitando total parcelado apenas quando a parcela do PDF o comprova; arredondamentos de centavos documentados. Correspondência ambígua não é confirmação. O SMS pode mostrar valor integral e a fatura somente parcela, além de diferença de data ou conversão internacional. Preservar valores, sinais e parcelas do PDF; não criar nova despesa a partir de SMS nem inferir estorno efetivado a partir de observação “deve estornar”.

Categoria do site é mais ampla que a planilha. A observação específica prevalece: “shopping” + “Cabeleireiro” continua Corte Cabelo; assinatura identificada permanece na rubrica específica; cartão de Paloma mantém metade na linha 56, com categoria/observação apenas no detalhe. Períodos de viagem e última confirmação orientam o agrupamento, sem transformar assinaturas simultâneas em despesas da viagem ou inventar divisão/reembolso.

Consulta de outubro/ciclo novembro em `periodos/2026-10/output/.auditoria/dados/site_classificacoes.json`; vínculos em `conferencia_site.json`. Exemplos resolvidos: URIEL GASPAR de 10/10 = circo Isabela (Lazer); G3TecAssistencia de 28/10 = Casa (parcela 01/02, R$ 122,50); MP Barbearia de 21/10 = cabeleireiro. Estes exemplos não generalizam finalidade de qualquer compra futura. Observações de presentes e compras de Isabela ficam nos IDs do período.
