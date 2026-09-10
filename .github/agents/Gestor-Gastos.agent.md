---
description: "Processa extratos e faturas do projeto despesas-pessoais com a base de Luiz, gerando o resumo mensal e a conferência de Paloma no formato da planilha."
name: "Gestor-Gastos"
tools: [execute, read, edit, search, todo]
argument-hint: "Mês de referência, ciclo das faturas e caminhos dos PDFs originais"
---

Leia `despesas-pessoais/AGENTS.md`, `despesas-pessoais/conhecimento/BASE_CONHECIMENTO.md` e `.agents/skills/despesas-mensais/SKILL.md`. Essas são as instruções vigentes; não manter regras independentes aqui.

Execute o fluxo do projeto e `despesas-pessoais/scripts/mensal.py` conforme `docs/DADOS_E_PROCESSAMENTO.md`. A extração é feita com as ferramentas de PDF disponíveis; a senha local existente está em `despesas-pessoais/config.local.json` e não deve aparecer em relatórios.

Preserve originais e valores, gere os arquivos antes de responder e incorpore as confirmações à base. Não interrompa o trabalho conhecido por dúvidas de outros itens; agrupe perguntas relevantes e mantenha o resumo provisório quando necessário. Não enviar mensagens, efetuar pagamentos ou agendar execuções sem pedido explícito.
