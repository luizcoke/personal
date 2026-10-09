# Contrato de dados e procedimento mensal

O processador é um agente com instruções, apoiado por um validador e gerador determinísticos. O comando não faz OCR nem identifica sozinho qualquer layout de PDF. O agente extrai os documentos, aplica a base vigente e preenche o contrato abaixo; o comando recusa inconsistências antes de gerar o quadro.

## Receber e extrair

1. Identificar mês de referência e ciclo pelas instruções e cabeçalhos. Se indefinidos e materialmente ambíguos, perguntar enquanto organiza os arquivos. Preparar com `mensal.py preparar`; PDFs repetidos pelo SHA-256 são ignorados. Mesmo nome com conteúdo diferente exige resolução e não sobrescreve.
2. Ler `config.local.json` somente quando precisar da senha já configurada. Desbloquear em `auditoria/extracao/` pelos utilitários de `.core/tools` ou ferramenta PDF disponível. Guardar texto e, quando útil, recortes/páginas para inspeção.
3. Nos cartões, separar colunas, cabeçalhos de cartão, compras atuais, estornos, internacionais/IOF e futuras. Não confiar nos recortes fixos dos scripts antigos. Conferir cada subtotal contra o PDF.
4. No extrato, extrair todos os movimentos para auditoria e selecionar somente a janela contábil em `periodo.json`. Preservar saldo anterior, saldo final e saldos diários do mês.
5. Classificar por regras específicas e última confirmação. Anotar quando um item já é a participação pessoal, quando usa um reembolso confirmado e quando continua integral por falta de rateio. Cada ID pertence a uma única fonte e a no máximo uma linha.

## `periodo.json`

Gerado pelo comando preparar: `versao`, `mes_referencia` (AAAA-MM), `ciclo_faturas` (AAAA-MM), `extrato_inicio`/`extrato_fim` (ISO), `criterio_cartoes` e `arquivos` (`arquivo` relativo ao período, `sha256`). O ciclo é explícito, não calculado a partir do nome do extrato.

## `auditoria/dados/lancamentos.json`

Objeto com `versao: 1`, `mes_referencia`, `ciclo_faturas`, `fontes`, `lancamentos` e `observacoes` (texto de decisões relevantes para o resumo).

Cada fonte contém:

- `id`, `nome`, `tipo` (`cartao` ou `extrato`), `arquivo` relativo ao período e `sha256` igual ao manifesto.
- Cartão: `total_integral`, `vencimento`, `subtotais` com `cartao`, `tipo` (`nacional` ou `internacional`, incluindo IOF real) e `valor`.
- O modelo `planilha.json` cadastra `cartoes_paloma` (3878 e 6553, identificados pelos cabeçalhos). Por confirmação de 09/10/2026, todo gasto desses cartões, inclusive AABB, entra a 50% na linha 56; estornos seguem o mesmo fator. O validador impede segundo rateio e entrada de cartão de Luiz nessa linha. Novos finais requerem identificação do titular.
- Extrato: `saldo_inicial`, `saldo_final`, `saldos_diarios` como objeto de data ISO para saldo. Só incluir controles da janela do mês; verificar também o saldo anterior no PDF.

Cada lançamento contém:

| Campo | Significado |
| --- | --- |
| `id` | Único no período; não usar só data/valor/descrição como chave de deduplicação |
| `fonte_id` | ID da fonte original |
| `origem` | Rótulo legível opcional, mantido no primeiro ciclo |
| `data` | ISO completa no extrato; data literal do PDF no cartão, sem inventar ano da compra |
| `descricao` | Texto original/normalizado fiel ao estabelecimento ou PIX |
| `pagina` | Página original, começando em 1 |
| `cartao`, `parcela`, `tipo` | Para cartão, final e parcela atual literal; tipo nacional/internacional/iof |
| `valor_original` | String decimal com ponto, sinal original; débitos negativos no banco e compras positivas nas faturas atuais |
| `valor_pessoal_exato` | String decimal, incluindo meios centavos; zero quando excluído |
| `linha` | ID string de `modelos/planilha.json`, ou null para exclusão |
| `status` | `confirmada_usuario`, `regra_kb`, `provisoria`, `pendente_extrato`, `nao_identificado` ou exclusão descrita |
| `observacao` | Regra/decisão, motivo da exclusão e limites da evidência |
| `rateio_status` | `aguardando_confirmacao` quando a participação no resumo depende de Luiz; `confirmado_manter_integral` quando ele confirma o valor integral no quadro pessoal. Essa decisão não identifica um crédito bancário |
| `credito_vinculado` | ID de crédito confirmado que reduz a despesa; preservar vínculo recíproco no crédito. Não preencher com candidato provável |
| `creditos_aplicados` | Alternativa para distribuição confirmada de crédito agrupado: lista de `id` e `valor` decimal; soma das alocações nunca excede o crédito. Não combinar com `credito_vinculado` nem usar candidato provável |
| `base_participacao` | `ja_parte_pessoal` quando o valor original já é a participação de Luiz, como o cofrinho do 13º |
| `tipo_recebimento` | `devolvido` em crédito que foi devolvido e não pode quitar outra despesa |

Guardar também os dados extraídos integrais e as respostas do usuário na auditoria, sem sobrescrever fontes. Números monetários em JSON são strings: nunca floats. Valores atuais vêm do PDF, não dos exemplos históricos.

## Validar e gerar

`python scripts/mensal.py validar --mes AAAA-MM` verifica fonte/hash, IDs, linhas, período bancário, sinais, participação, cartão família, não reutilização de crédito, total da fatura/subtotais e saldos bancários/diários. Falta de classificação pode ser provisória; falta de fechamento da fonte impede emissão por esse comando.

`python scripts/mensal.py gerar --mes AAAA-MM` valida novamente, gera `RESUMO_MENSAL.md`, `PENDENCIAS.md` e `auditoria/dados/conferencia_mensal.json`. Os totais pessoais são arredondados por item/fonte. O arquivo novo substitui o resumo vigente de forma determinística; não somar versões.

O agente prepara o `RESUMO_PALOMA.md` com `modelos/resumo_paloma.md` e o registro dos vínculos daquele período. O CLI atual não adivinha esses vínculos nem monta uma cobrança automaticamente. Se a divisão não estiver confirmada, apresentar como comparação para conferência e não saldo devido. A versão de agosto serve como exemplo real.

## Holerites

Incluir o recibo mensal em `documentos_complementares` de `periodo.json` e em `entradas/`, com tipo `holerite`, SHA-256 e caminho dos dados, sem sobrescrever originais. A lista `arquivos` permanece destinada às fontes do validador de despesas. Manter `auditoria/dados/holerite.json` separado do contrato de despesas: competência, pagamento, fonte/hash/página, rubricas com código/descrição/tipo/valor decimal, totais, bases informativas, vínculo bancário e células de destino. Não adicionar proventos ou descontos de folha ao total de despesas dos cartões/extrato. O validador `mensal.py` não valida holerites; executar separadamente as conferências a seguir e verificar seu hash.

Conferir com Decimal: proventos menos todos os descontos do recibo = líquido do pagamento; líquido + adiantamento já pago = líquido recebido no mês; proventos menos descontos efetivos (excluindo adiantamento) = esse mesmo líquido mensal. Conciliar depósitos/portabilidade sem contar a transferência novamente como receita. Tratar divergências como pendência, não ajuste forçado.

Produzir `resultados/HOLERITE.md` com tabelas de rubricas, conciliação e mapa da planilha. Ao lançar salário bruto e reembolsos em receitas, lançar INSS, IRRF, pensão e demais descontos efetivos uma vez; não lançar o adiantamento como despesa. FGTS/base IR/base INSS não são receitas disponíveis. VA/Alelo e benefícios ausentes do recibo não estão validados por ele. Preservar valores já confirmados, apontar previsões e pedir apenas a informação nova necessária.

O Excel pode ter rótulo legado de salário “líquido” numa estrutura que subtrai descontos. Explicitar a base bruta da célula do mês e evitar dupla dedução; não alterar silenciosamente todos os meses anteriores por causa desse rótulo.

## Limites conhecidos do processador

- Leitor PDF universal, OCR genérico e sincronização com Excel não estão implementados. O agente adapta a extração ao documento recebido.
- Os scripts antigos de agosto estão arquivados porque usam IDs, páginas, datas e valores daquele ciclo. As regras atuais são as referências da base, não comentários desses scripts.
- O validador confirma coerência e integridade; uma categoria plausível porém errada ainda depende da base e das confirmações do usuário.
- Só arquivos normalizados completos geram um fechamento conferido. Se faltar PDF ou saldo de abertura, informar o que falta e entregar o progresso conhecido sem alegar conclusão financeira.

## Novas linhas de assinaturas — imagem final de agosto

OneDrive anual e OpenAI mensal passaram ao bloco Assinaturas, nas linhas Excel 61 e 62. O modelo usa `linha` como ID estável e `linha_excel` para a posição de exibição; os IDs citados nas regras e lançamentos continuam válidos. Spotify, Apple, Netflix, Lazer, Loterias e Outros aparecem nas linhas Excel 63–68. Fundo de Reserva não está visível no recorte; não inferir a nova posição. Reembolso empresa segue complementar.

A imagem preenchida foi preservada em `periodos/2026-08/auditoria/referencias/planilha_mensal_preenchida.png`. Há diferenças de valores em relação ao resumo (incluindo eSocial já rateado); registradas em `resultados/detalhes/CONFERENCIA_PLANILHA_FINAL.md`. Não transformar essas divergências em novas regras sem esclarecer a intenção.
