# Despesas pessoais — rotina mensal

Comece por este arquivo. Você envia os PDFs e informa o mês; o agente lê a base, processa, confere os valores e entrega as tabelas no formato das imagens do Excel.

## Continuar o plano financeiro

O [Planejador-Financeiro](../.github/agents/Planejador-Financeiro.agent.md) segue os cinco roteiros enviados por Luiz e a base já confirmada. Para retomá-lo no Codex, use: **“Use $plano-financeiro e continue pelas próximas ações do plano.”** A skill do projeto fica em `.agents/skills/plano-financeiro` na raiz do repositório; se uma sessão ainda não a descobrir, peça a leitura direta desse `SKILL.md`.

- [Plano atual](planejamento/PLANO_FINANCEIRO_INICIAL.md), [revisão de gastos](planejamento/REVISAO_GASTOS.md) e [ações](planejamento/ACOES.md).
- [Método dos cinco módulos](planejamento/METODO.md) e [textos originais das imagens](planejamento/referencias/PROMPTS_ORIGINAIS.md).

O perfil `.agent.md` segue a convenção já existente neste repositório. No Codex, a rotina reutilizável fica na skill e nas instruções do projeto; não foi criado serviço em segundo plano. A estrutura usa as [instruções e skills de repositório documentadas pela OpenAI](https://learn.chatgpt.com/pt-BR/docs/customization/overview).

## Usar no próximo mês

1. Abra este projeto no Codex e anexe o extrato e as faturas originais, ou coloque-os em `periodos/AAAA-MM/entradas/`.
2. Envie uma mensagem como: **“Use $despesas-mensais. Processe setembro/2026 com o extrato de 01 a 30/09 e as faturas do ciclo outubro. Gere o resumo da planilha e a conferência de Paloma.”** Ajuste os meses conforme os arquivos enviados.
3. Leia `resultados/RESUMO_MENSAL.md`. Se houver dúvidas, elas ficam em `PENDENCIAS.md`; suas respostas atualizam a mesma base e os mesmos relatórios.

O formato padrão é Markdown, para transpor à planilha. Não é necessário reenviar as imagens ou explicar de novo as regras conhecidas. Luiz continuará preenchendo o Excel manualmente para conferir; atualização direta fica para um pedido futuro. O resumo de Paloma contém a tabela, o total e o informativo das linhas 54+53; análises ficam nos detalhes.

## Arquivos que você usa

- [Resumo de agosto/2026](C:/github/personal/despesas-pessoais/periodos/2026-08/resultados/RESUMO_MENSAL.md) — **R$ 15.224,56**, fechamento manual final confirmado por Luiz. Valores por documentos preservados nos detalhes.
- [Conferência de Paloma](C:/github/personal/despesas-pessoais/periodos/2026-08/resultados/RESUMO_PALOMA.md) — **R$ 2.466,97 rateados**, quadro manual conferido por Luiz; tabela simples e informativo de snacks/restaurantes **R$ 1.420,71**.
- [Pendências](C:/github/personal/despesas-pessoais/periodos/2026-08/resultados/PENDENCIAS.md) e [créditos por babá](C:/github/personal/despesas-pessoais/periodos/2026-08/resultados/detalhes/CONFERENCIA_REEMBOLSOS_BABAS.md).
- [Base de conhecimento](C:/github/personal/despesas-pessoais/conhecimento/BASE_CONHECIMENTO.md) — entrada das regras e aprendizados atuais.

## Estrutura

```text
despesas-pessoais/
├── README.md                     por onde começar
├── AGENTS.md                     instruções do agente neste projeto
├── conhecimento/                 regras atuais, estabelecimentos e aprendizados
├── modelos/                      linhas do Excel e modelos dos dois resumos
├── periodos/
│   └── 2026-08/                  mês de referência
│       ├── periodo.json          mês, ciclo das faturas e originais com hash
│       ├── entradas/             PDFs originais
│       ├── resultados/           resumos mensal, Paloma e pendências
│       │   └── detalhes/         cartões, extrato e conferências
│       └── auditoria/            dados, extração e histórico da execução
├── scripts/mensal.py             preparar, validar e gerar o quadro mensal
├── docs/                         contrato de dados e limites do processamento
├── testes/                       verificações de regressão e de integridade
└── historico/                    base anterior e análise inicial preservadas
```

A skill do repositório está em [despesas-mensais](C:/github/personal/.agents/skills/despesas-mensais/SKILL.md). O perfil já existente [Gestor-Gastos](C:/github/personal/.github/agents/Gestor-Gastos.agent.md) também aponta para esta mesma base. Não existem duas cópias concorrentes de regras.

## Skill, agente e aprendizado

A **base** guarda suas decisões; a **skill** ensina quando e como executar o fluxo; o **AGENTS.md** orienta o agente ao trabalhar no projeto; o **script** faz as contas e verificações reproduzíveis. Uma skill é um conjunto de instruções e referências, não treinamento permanente do modelo. Assim, uma conversa nova consegue consultar o aprendizado salvo.

A documentação oficial descreve a descoberta de skills em `.agents/skills` e o carregamento de instruções via `AGENTS.md`: [skills](https://learn.chatgpt.com/docs/build-skills) e [instruções de projeto](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Se a skill não aparecer na sessão atual, abra uma nova tarefa no mesmo projeto ou reinicie o Codex; também é possível pedir para ler o `AGENTS.md` diretamente.

## O que está automatizado

O agente realiza a extração e a classificação com as regras registradas. `mensal.py` cria a estrutura, evita reimportar o mesmo PDF, valida fontes/valores/rateios e gera a tabela pessoal mais a lista de pendências. O quadro de Paloma usa os vínculos efetivamente identificados, sem transformar correspondências prováveis em dívida. PDFs com outro layout podem exigir adaptação da extração pelo agente.

```powershell
python scripts/mensal.py preparar --mes 2026-09 --ciclo 2026-10 --arquivos "caminho/extrato.pdf" "caminho/fatura.pdf"
python scripts/mensal.py validar --mes 2026-08
python scripts/mensal.py gerar --mes 2026-08
```

Execute a partir de `despesas-pessoais`; os caminhos dos dados são resolvidos pelo script. Se `python` não estiver disponível, o agente deve localizar o runtime configurado no app. O contrato de extração está em [docs/DADOS_E_PROCESSAMENTO.md](C:/github/personal/despesas-pessoais/docs/DADOS_E_PROCESSAMENTO.md).

## Cuidados já incorporados

A provisão do 13º de R$ 248,45 já é a sua metade; o cartão 3878 é dividido uma única vez; fatura paga no banco não duplica compras; tratamentos integralmente reembolsados e PIX próprios ficam fora do orçamento; créditos de Paloma têm vínculo e disponibilidade conferidos. Próximas parcelas e aportes futuros ficam como acompanhamento, não como despesas realizadas.

As instruções, modelos, scripts, testes, resumos mensais, `periodo.json` e os JSON de `auditoria/dados/` são versionados, incluindo confirmações e fechamento manual. PDFs originais, imagens, extrações, cópias históricas, caches e `config.local.json` ficam locais conforme `.gitignore`; faça backup desses arquivos separadamente para preservá-los entre computadores. O repositório contém dados financeiros pessoais nos resumos e JSON. Não houve agendamento, envio de mensagem ou pagamento automático.

## Restaurar o projeto em outra máquina

Os dados e os resumos fechados vêm do Git. Para validar a integridade documental ou processar novamente, restaure os PDFs originais em `periodos/AAAA-MM/entradas/` e as imagens/extrações necessárias a partir do backup local. Crie `config.local.json` usando `config.example.json` e configure a senha localmente. A configuração real nunca entra no Git. Os testes conferem os dados versionados mesmo sem PDFs; a validação da rotina mensal continua exigindo os originais.
