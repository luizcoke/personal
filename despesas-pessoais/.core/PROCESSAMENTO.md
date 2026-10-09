# Contrato do processamento mensal

Referência técnica, consultada por seção. Regras pessoais em [BASE_CONHECIMENTO.md](conhecimento/BASE_CONHECIMENTO.md); linhas e IDs em [planilha.json](modelos/planilha.json). O CLI valida dados normalizados; não faz OCR nem reconhece qualquer layout sozinho.

## Receber e extrair

- Pasta `periodos/AAAA-MM/`: mês de referência. Extrato usa data contábil do primeiro ao último dia; cartões usam faturas completas do ciclo registrado, salvo pedido diferente. Sufixo antigo `ref_*` não redefine mês.
- Originais em `input/`; texto/imagens em `output/.auditoria/extracao/`. Comparar SHA-256 antes de importar. `_unlocked`, resumos e imagens não são novas fontes. Se necessário, usar senha de `config.local.json` somente localmente, sem copiá-la para resultados.
- Conferir visualmente cabeçalhos, cartões/titulares, colunas, sinais, internacionais/IOF e parcelas atuais versus futuras. Cada lançamento preserva fonte, página e ID; transações legítimas iguais não são removidas por data/valor.
- Extrato conserva todos os movimentos para conciliação, incluindo os excluídos do orçamento; selecionar o mês na coluna contábil. Conferir saldo anterior, final e diários disponíveis.

## Manifesto e dados

Valores monetários nos JSON são strings decimais com ponto; cálculos usam Decimal.

`periodo.json`: `versao`, `mes_referencia`, `ciclo_faturas`, `extrato_inicio`, `extrato_fim`, `criterio_cartoes`, `arquivos` com caminho relativo e SHA-256. `fechamento_manual` protege o resumo confirmado: não executar `gerar` sobre ele. Documentos complementares como holerite ficam em `documentos_complementares`, com tipo, arquivo, hash e caminho dos dados; não entram nas fontes de despesas.

`output/.auditoria/dados/lancamentos.json`: `versao: 1`, mês/ciclo, `fontes`, `lancamentos` e `observacoes`.

| Registro | Campos e invariantes |
| --- | --- |
| Toda fonte | `id`, `nome`, `tipo` (`cartao`/`extrato`), `arquivo` relativo ao período, `sha256` igual ao manifesto |
| Cartão | `total_integral`, `vencimento`, `subtotais` por cartão/tipo nacional ou internacional, com IOF real |
| Extrato | `saldo_inicial`, `saldo_final`, `saldos_diarios` por data ISO, apenas controles do período |
| Todo lançamento | `id`, `fonte_id`, `data`, `descricao`, `pagina` a partir de 1, `valor_original`, `valor_pessoal_exato`, `linha` ou null para exclusão, `status`, `observacao` |
| Data e sinais | Banco: ISO e débito negativo. Cartão: data literal, sem inventar ano; compras positivas e estornos negativos |
| Cartão específico | `cartao`, `parcela`, `tipo` nacional/internacional/iof; titularidade determina aplicação da regra de Paloma |
| Participação | `rateio_status`: `aguardando_confirmacao` ou `confirmado_manter_integral`; `base_participacao: ja_parte_pessoal` impede segundo rateio |
| Créditos | `credito_vinculado` com ID confirmado e vínculo recíproco, ou `creditos_aplicados` com IDs/valores. Não combinar os dois; soma não excede crédito e não reutiliza valor |
| Devolução | `tipo_recebimento: devolvido`: crédito não pode quitar outra despesa |

Status usuais: `confirmada_usuario`, `regra_kb`, `provisoria`, `pendente_extrato`, `nao_identificado` ou exclusão justificada. `origem` é rótulo legível opcional. Categoria desconhecida vai a Outros; categoria conhecida com rateio incerto permanece na categoria, com participação provisória. Respostas por ID ficam na auditoria.

## Validar e entregar

Executar na raiz `despesas-pessoais/`:

```powershell
python .core/scripts/mensal.py preparar --mes AAAA-MM --ciclo AAAA-MM --arquivos "documento.pdf"
python .core/scripts/mensal.py validar --mes AAAA-MM
python .core/scripts/mensal.py gerar --mes AAAA-MM
```

`validar` confere hashes, IDs, linhas, sinais, janela bancária, fontes, rateios, créditos, totais de fatura/cartão e saldos bancários. `gerar` valida e escreve resumo, pendências e `conferencia_mensal.json`. Falta de conciliação bloqueia a emissão; classificação pode continuar provisória. Em mês fechado, validar sem regenerar; diferenças documentais permanecem em detalhes.

Saídas em `output/`: `RESUMO_MENSAL.md`, `RESUMO_PALOMA.md`, `HOLERITE.md` e `PENDENCIAS.md`. Detalhes em `output/detalhes/`; dados em `output/.auditoria/dados/`. O quadro de Paloma é preparado pelo agente usando vínculos identificados e [modelo próprio](modelos/resumo_paloma.md), sem inferir cobrança. Somar participações exatas e arredondar o total; explicar eventual diferença das linhas exibidas. Alimentação informativa = 54+55+53, sem novo rateio e fora do acerto.

## Holerites e benefícios

Guardar `holerite.json` na auditoria: competência, pagamento, fonte/hash/página, rubricas com código/descrição/tipo/valor, totais, bases informativas, vínculos bancários e células de destino. O CLI de despesas não valida folha; conferir separadamente:

1. Proventos − todos os descontos do recibo = líquido do pagamento.
2. Líquido + adiantamento pago = líquido recebido no mês.
3. Proventos − descontos efetivos sem adiantamento = o mesmo líquido mensal.

Conciliar depósitos/portabilidade uma vez. Ao registrar bruto e descontos efetivos no Excel, adiantamento não vira nova despesa. FGTS e bases tributárias são informativos, não dinheiro disponível. Benefícios embutidos no salário não entram novamente.

Perguntar a Luiz o VA/Alelo efetivo a cada mês, salvo confirmação já disponível. Conferir auxílio-creche esperado de R$ 720,00 e avisar quando não identificado no holerite/documentos bancários; não presumir ausência em conta não fornecida. APAE/APDEX de R$ 900,00 é outro benefício. Solicitação futura não confirma receita; créditos agrupados sem vínculo permanecem inconclusivos.

`HOLERITE.md` mostra rubricas, conferência, fonte e mapa do Excel. Não preencher receita com previsão ou salário de outro mês se faltar o documento.

## Excel local

Usar skill de planilhas quando solicitado. Arquivo em `planilhas/`, fora do Git; conferir que a versão salva contém as últimas alterações do usuário e preservar cópia anterior. Atualizar só o mês/escopo pedido, sem perder fórmulas, validações, vínculos, tabelas dinâmicas ou estilos.

Conferir rótulos antes do mapeamento. `Gastos` usa bruto menos descontos embora exista rótulo legado “líquido”; explicitar no relatório, sem dupla dedução nem alteração histórica silenciosa. Separar coparticipação odontológica da médica. `Gastos Apartamento` recebe a conferência de Paloma e o informativo alimentar. Valores por célula e exceções ficam nos dados do mês, não como defaults da skill.

## Desenvolvimento

Testes: `python -m unittest discover -s .core/testes -p test_mensal.py`. Validação documental exige originais; testes podem conferir dados versionados sem PDFs. Preservar fechamentos manuais. Scripts específicos em `output/.auditoria/` dependem do layout/mês, não são parsers universais; não executar rotinas históricas como atuais.
