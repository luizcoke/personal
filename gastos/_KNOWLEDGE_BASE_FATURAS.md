# Base de Conhecimento — Faturas de Cartão de Crédito

> Objetivo: documentar a estrutura dos PDFs de fatura para facilitar a extração de gastos e preenchimento da planilha mensal.

---

## Cartões Mapeados

| Cartão | Arquivo padrão | Observações |
|--------|---------------|-------------|
| Mastercard Black | `AAAA-MM-MASTERCARD_BLACK.pdf` | |
| Visa Infinite | `AAAA-MM-VISA_INFINITE.pdf` | |

---

## Estrutura Geral de uma Fatura PDF

A maioria das faturas segue este padrão de seções:

1. **Resumo da fatura** — total a pagar, vencimento, limite disponível
2. **Lançamentos da fatura atual** — lista de compras do titular e adicionais
3. **Parcelas futuras** — compras parceladas que ainda vão vencer
4. **Encargos / Juros** — quando houver pagamento mínimo anterior
5. **Informações do cartão** — dados da conta, agência, etc.

---

## Como Localizar os Lançamentos

### Campos por transação (linha típica)

```
DATA       ESTABELECIMENTO / DESCRIÇÃO          VALOR (R$)
05/04/26   SUPERMERCADO EXTRA                   -  452,30
07/04/26   NETFLIX.COM                          -   55,90
10/04/26   PAGAMENTO EM 3X LOJA XYZ   1/3       -  100,00
```

| Campo | O que é |
|-------|---------|
| Data | Data da compra (não da fatura) |
| Descrição | Nome do estabelecimento ou serviço |
| Parcela | Quando existir `X/Y`, indica parcela atual / total |
| Valor | Valor debitado nesta fatura (sempre positivo no PDF; anotar como saída) |

---

## Padrões Específicos por Cartão

### Mastercard Black (Itaú Personnalitê)

- **Três cartões na mesma fatura**: final 0539 (Luiz titular), final 1929 (Luiz adicional), final 3878 (Paloma)
- Seção chama-se **"Lançamentos: compras e saques"** — dividida em duas colunas lado a lado
- Compras parceladas: aparecem com `DD/MM ESTABELECIMENTO XX/YY`
- Linha de totalização por cartão: `Lançamentos no cartão (final XXXX) R$ X.XXX,XX`
- Linha de totalização geral: `Total dos lançamentos atuais R$ X.XXX,XX`
- Débito automático em conta corrente Itaú
- **Cartão 3878 (Paloma):** dividido 50/50 com a esposa — aplicar 50% de todos os valores na planilha

### Visa Infinite (Itaú Personnalitê)

- **Dois cartões na mesma fatura**: final 2587 (titular) e final 7396 (adicional) — cada um com subtotal próprio
- Seção chama-se **"Lançamentos: compras e saques"** — dividida em duas colunas lado a lado no PDF
- Compras parceladas: aparecem com `DD/MM ESTABELECIMENTO  XX/YY` (parcela atual / total)
- Compras internacionais mostram valor em moeda original + conversão BRL
- Linha de totalização: `Total dos lançamentos atuais R$ X.XXX,XX`
- Seção separada **"Compras parceladas - próximas faturas"** lista apenas as parcelas vindouras (não somar — já estão fora do total atual)
- Estornos: aparecem com valor negativo precedido de `-` na mesma linha do estabelecimento
- Débito automático em conta corrente Itaú (fatura quitada automaticamente)

---

## Regras de Classificação Automática

> Use esta seção como dicionário: ao encontrar um texto no PDF, consulte a coluna **"Contém no PDF"** para saber em qual item da planilha somar o valor.  
> A correspondência é por **prefixo ou trecho** — basta o texto do PDF *conter* a palavra/padrão listado.

### Alimentação — Ifood + snacks + Padaria

> Delivery em casa, snacks noturnos, comida rápida por app. Valores menores e frequentes.

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `IFD*` | IFD*iFood, IFD*ARCOS DOURADOS COM | Pedidos via iFood |
| `IFOOD` | IFOOD | Variação sem abreviação |
| `99Food *` | 99Food *Pizza Hut - Lap | Delivery pelo app 99 (mesmo que seja de restaurante conhecido) |
| `Kee*` | Kee*EMPORIO DAS PIZZ | Entrega direta pelo app da loja |
| `PANIFICADORA` | PANIFICADORA BELLA ALB | Padarias em geral |
| `PADARIA` | PADARIA NOSSA SENHORA | |
| `CAFETERIA` | CAFETERIA CENTRAL | |
| `SNACK` | SNACK BAR | |
| `OAKBERRY` | OAKBERRY ACAI | Açaí snack |
| `AmabiliQueijos` | AmabiliQueijos | Queijaria / snack |
| `ALMEIDA QUEIJOS` | ALMEIDA QUEIJOS | Queijaria / snack |
| `BELLA SAUIPE` | BELLA SAUIPE II | Snack / fast food |
| `HIGH LAPA FOODS` | HIGH LAPA FOODS LTDA | Snack / lanche |

### Alimentação — Restaurantes

> Jantar / almoço presencial em restaurante. Gastos maiores, ocasiões especiais (ex: Coco Bambu, Pecorino).

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `COCO BAMBU` | COCO BAMBU LAPA | Restaurante presencial |
| `PECORINO` | PECORINO REST | Restaurante presencial |
| `RESTAURANTE` | RESTAURANTE DO JOSE | Use para estabelecimentos onde foi presencialmente |
| `CHURRASCARIA` | CHURRASCARIA BOI | |
| `ASSOCIACAO ATLETICA` | ASSOCIACAO ATLETICA B | Restaurante AABB — **somente quando valor ≤ R$ 250** |
| `ASSOCIACAO ATLETIC` | ASSOCIACAO ATLETIC | Restaurante AABB — **somente quando valor ≤ R$ 250** |

> ⚠️ `99Food *` e `Kee*` = delivery → **Ifood + snacks + Padaria**, mesmo que o nome seja de restaurante.  
> ⚠️ `ASSOCIACAO ATLETIC` com valor **acima de R$ 250** = mensalidade/outro → **Outros**.

### Alimentação — HiperMercado

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `EXTRA` | EXTRA HIPERMERCADO | |
| `CARREFOUR` | CARREFOUR BARRA FUNDA | |
| `ATACADAO` | ATACADAO | |
| `ASSAI` | ASSAI ATACADISTA | |
| `WALMART` | WALMART | |
| `BIG` | BIG SUPERMERCADO | |

### Alimentação — Mercadão + Bebidas

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `MERCADO MUNICIPAL` | MERCADO MUNICIPAL SP | |
| `DISTRIBUIDORA` | DISTRIBUIDORA BEBIDAS | |
| `ADEGA` | ADEGA DO VINHO | |

### Alimentação — Marmitas

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `MARMITA` | MARMITA EXPRESS | |
| `RANCHO` | RANCHO GRILL | |

### Saúde — Drogaria

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `DROGASIL` | DROGASIL1008 | |
| `DROGARAIA` | PG *DROGARAIA | Inclui pagamentos via PicPay/PG* |
| `RDSAUDE` | RDSAUDE ONLINE | RD Saúde online (mesma rede Droga Raia) |
| `ULTRAFARMA` | ULTRAFARMA | |
| `PANVEL` | PANVEL FARMACIA | |
| `FARMACIA` | FARMACIA POPULAR | |

### Pessoal / Vestuário / Beleza — Corte Cabelo

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `C.N.D. LOCACAO` | C.N.D. LOCACAO DE BEN | Cabeleireiro |
| `BARBEARIA` | BARBEARIA CENTRAL | |
| `CABELEREIRO` | CABELEREIRO JOAO | |
| `SALAO` | SALAO DE BELEZA | |

> Vacinas, consultas médicas e despesas de saúde da Isabela.

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `CL PEDIATRICA` | CL PEDIATRICA LUCI | Vacinas / consultas pediatra |
| `PEDIATRIA` | CLINICA PEDIATRIA | |
| `VACINA` | CLINICA VACINA | |

### Filhos / Educação / Cuidados — Gastos Babá Isabela *

> Pagamentos da babá da Isabela. Normalmente não aparece no cartão (pago em dinheiro / transferência).

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `BABA` | PAGTO BABA | Pagamento babá se vier no cartão |
| `CAASP` | CAASP LAPA | Caixa de Assist. dos Advogados (plano de saúde) → Drogaria |

### Filhos / Educação / Cuidados — Gastos Isabela *

> Atividades, natação, cursos e demais gastos da Isabela (não babá). Normalmente no cartão da Paloma (3878) — aplicar 50%.

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `WellhubIsabelaPaixao` | WellhubIsabelaPaixao | Wellhub (natação / atividade física da Isabela) — cartão 3878, 50% |

### Filhos / Educação / Cuidados — Gastos Meninos

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `ESCOLA` | ESCOLA SABER | |
| `COLEGIO` | COLEGIO OBJETIVO | |
| `LIVRARIA` | LIVRARIA CULTURA | |

### Pessoal / Vestuário / Beleza — Compras / Presentes

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `SHOPEE *` | SHOPEE *MRILOJA | Loja genérica no Shopee |
| `MERCADO LIVRE` | MERCADO LIVRE | |
| `AMAZON` | AMAZON.COM.BR | Compras (não Prime) |
| `AMAZONMKTPLC` | AMAZONMKTPLC*UPTEC | Amazon Marketplace — **Compras/Presentes**, não veículo |
| `ITAUSHOP` | ITAUSHOP | Compra parcelada via Itaú Shop (ex: celular) → **Compras/Presentes** |
| `RENNER` | RENNER | |
| `RIACHUELO` | RIACHUELO 366 | |
| `ZARA` | Zara Brasil LTDA | |
| `C&A` | C&A MODA | |
| `ESKALA` | ESKALA 106 | Loja de roupas |
| `HERING` | HERING STORE | |

### Pessoal / Vestuário / Beleza — Compras / Presentes (marketplace casa)

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `Shopee*SHOPEE*MeuLar` | Shopee*SHOPEE*MeuLar | Produtos para casa no Shopee → **Compras / Presentes** |

### Casa / Moradia — Casa Manutenção Apartamento

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `Shopee*SHOPEE*MeuLar` | Shopee*SHOPEE*MeuLar | Produtos para casa no Shopee |
| `LEROY` | LEROY MERLIN | Materiais de construção |
| `TELHANORTE` | TELHANORTE | |
| `CASAS BAHIA` | CASAS BAHIA | Eletrodomésticos/móveis |
| `TOK&STOK` | TOK&STOK | |

### Veículo / Transporte — Uber - 99 / Estac / ConectCar

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `UBER` | UBER *TRIP | |
| `99*` | 99* | Corrida pelo app 99 (sem "Food") |
| `99APP` | 99APP | |
| `CONECTCAR` | CONECTCAR | Pedágio tag |
| `ESTAPAR` | ESTAPAR | Estacionamento |
| `MULTIPARK` | MULTIPARK | Estacionamento |

> ⚠️ `99Food *` (com "Food") → **Alimentação → Restaurantes**. Sem "Food" → **Transporte**.

### Veículo / Transporte — Carro Gasolina

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `POSTO` | POSTO SHELL, POSTO DE SERVICOS PAZ | Qualquer posto com "POSTO" no nome |
| `SERVICOS PAZ` | POSTO DE SERVICOS PAZ | Posto na Lapa |
| `SHELL` | SHELL LAPA | |
| `IPIRANGA` | IPIRANGA AUTO | |
| `BR DISTRIBUIDORA` | BR DISTRIBUIDORA | |
| `PETROBRAS` | PETROBRAS POSTO | |
| `AUTO POSTO` | AUTO POSTO ALBION LTD | |
| `FUKUYA` | FUKUYA KANEMOTO | Posto de gasolina |

### Assinaturas

| Contém no PDF | Item na planilha | Exemplo real |
|---------------|-----------------|-------------|
| `AMAZON PRIME` | AMAZON PRIME BR - 12/12 | AMAZON PRIME BR |
| `AMZN` | AMAZON PRIME BR - 12/12 | AMZN Digital |
| `SPOTIFY` | Spotify | SPOTIFY |
| `APPLE.COM` | APPLE COM/BILL Cloud | APPLE.COM/BILL |
| `APPLE COM` | APPLE COM/BILL Cloud | APPLE COM/BILL |
| `NETFLIX` | Netflix | NETFLIX.COM |

### Cartões e Dívidas — Juros/IOF

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `JUROS` | JUROS ROTATIVO | |
| `IOF` | IOF FINANCIAMENTO | |
| `ENCARGOS` | ENCARGOS FINANCEIROS | |
| `PORTO SEGURO` | PORTO SEGURO AUTO | Seguro do carro parcelado |

### Outros

| Contém no PDF | Item na planilha | Exemplo real |
|---------------|-----------------|-------------|
| `CAASP` | Drogaria | CAASP LAPA | Saúde → Drogaria (plano assistência advogados) |
| `CAIXA LOTERIAS` | Loterias | CAIXA LOTERIAS |
| `LOTERIA` | Loterias | LOTERIA FEDERAL |

---

## Regras de Classificação — Extrato Conta Corrente

> Use esta seção para mapear lançamentos do **extrato bancário** (Itaú Personnalitê) para os itens da planilha.  
> Diferente do cartão, o extrato contém pagamentos de contas fixas, PIX e débitos automáticos.

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
| `PAG TIT INT 742995528000` | PAG TIT INT 742995528000 | Condomínio |
| `DA PMSP` | DA PMSP 095250000000946 | IPTU |
| `DA ELETROPAULO` | DA ELETROPAULO 13724657 | Luz |
| `INT /CLARO S.A` | INT /CLARO S.A 003000005 | Conta Internet + TV |
| `DA VIVO-SP` | DA VIVO-SP 11280214885 | Conta Celular |
| `PIX TRANSF PALOMA` + valor `-220,00` | PIX TRANSF PALOMA 17/04 | Casa Faxina semanal |
| `PIX TRANSF PALOMA` + valor `-390,77` | PIX TRANSF PALOMA 15/04 | Carro IPVA + Licenciamento + Multa * |
| `PIX TRANSF PALOMA` + valor `-1.219,50` | PIX TRANSF PALOMA 30/04 | Financiamento Apt Lapa * (parcela mensal) |
| `PIX TRANSF PALOMA` + valor `-248,45` | PIX TRANSF PALOMA 06/04 | Gastos Babá Isabela Esocial * (provisão 13º/férias) |

> ⚠️ Nem todo PIX para PALOMA é igual. Diferenciar pelo **valor exato**: R$220,00 = faxina | R$1.219,50 = financiamento | R$248,45 = provisão babá. Valores positivos (entrada) = reembolso, não lançar como despesa.

### Filhos / Educação / Cuidados

| Contém no extrato | Exemplo real | Item na planilha |
|-------------------|-------------|------------------|
| `PIX TRANSF Sonia` | PIX TRANSF Sonia p13/04 | Gastos Meninos |
| `PIX TRANSF LUIZ FE` | PIX TRANSF LUIZ FE15/04 | Gastos Meninos |

### Cartões e Dívidas

| Contém no extrato | Exemplo real | Item na planilha |
|-------------------|-------------|------------------|
| `IOF` | IOF (débito conta) | Juros/IOF |

### Lançamentos a IGNORAR (não lançar na planilha)

| Contém no extrato | Motivo |
|-------------------|---------|
| `PERS INFINIT` | Débito automático fatura Visa Infinite — já lançada separadamente |
| `ITAU BLACK` | Débito automático fatura Mastercard Black — já lançada separadamente |
| `TED 033.2062.LUIZ C N` | Transferência entre contas próprias |
| `PIX TRANSF LUIZ CO` | Transferência entre contas próprias |
| `REND PAGO APLIC AUT MAIS` | Rendimento de aplicação automática (não é despesa) |
| `JUROS LIMITE DA CONTA` | Juros de uso do cheque especial — lançar em Juros/IOF apenas se quiser rastrear |

### Outros padrões do extrato

| Contém no extrato | Suspeita | Item na planilha |
|-------------------|----------|------------------|
| `PIX QRS CAIXA INSTA` | Loteria instantânea Caixa | Loterias |
| `PIX QRS RECEITA FED` | eSocial da babá (encargo trabalhista) — **Paloma paga 50%** | Gastos Babá Isabela Esocial * (50% líquido) |
| `PAY ASSOC` | Mensalidade AABB clube (parcelas) | AABB — Mensalidade Clube *(novo item na planilha)* |
| `PIX TRANSF MARIO P` | Tratamento filho (Luiz Guilherme) — **Bradesco Saúde reembolsa** | IGNORAR (não lançar) |
| `SISPAG PIX DANIELA COKE` | Entrada de dinheiro — parente/conhecida | Receita eventual |

---

## Itens da Planilha e Como Mapear da Fatura

Para cada lançamento extraído do PDF, identifique a qual **Item** da planilha ele pertence e some ao valor acumulado daquele item no mês.

### Receitas
| Item na planilha | De onde vem | Vem do cartão? |
|------------------|-------------|----------------|
| Salário Mensal - Líquido | Holerite / conta corrente | Não |
| Auxílio creche + APAE / APADEX | Holerite | Não |
| VA + benefícios Alelo | Holerite | Não |
| Horas Extras | Holerite | Não |
| Férias | Holerite | Não |
| 13º salário + PPR + IR | Holerite | Não |
| FGTS | Holerite | Não |
| Outros | Eventuais | Não |

### Descontos Legais
| Item na planilha | De onde vem | Vem do cartão? |
|------------------|-------------|----------------|
| INSS | Holerite | Não |
| IR | Holerite | Não |
| Pensão alimentícia | Holerite / transferência | Não |
| Co-participação Bradesco Saúde | Holerite | Não |
| Plano de Saúde Dental | Holerite | Não |

### Casa / Moradia
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Financiamento Apt Lapa * | débito automático / transferência | Não (débito automático) |
| Condomínio | CONDOMINIO, boleto | Às vezes |
| IPTU | PREFEITURA, IPTU | Às vezes |
| Luz | ENEL, CPFL, LIGHT, CEMIG, ENERGIA | Às vezes |
| Conta Celular | CLARO, VIVO, TIM, OI, celular | Às vezes |
| Conta Internet + TV | NET, CLARO NET, SKY, VIVO FIBRA, internet | Às vezes |
| Casa Manutenção Apartamento | materiais, ferragens, manutenção, prestador | Às vezes |
| Casa Faxina semanal | faxina, limpeza, diarista | Às vezes |

### Filhos / Educação / Cuidados
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Gastos Meninos | escola, curso, material, livro, uniforme | Às vezes |
| Gastos Babá Isabela * | pediatra, babá, creche, atividade | Sim |

### Veículo / Transporte
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Carro IPVA + Licenciamento + Multa * | DETRAN, IPVA, multa | Às vezes |
| Carro Seguro - Porto Seguro 6x * R$434,73 | PORTO SEGURO, seguro auto | Sim (parcelado) |
| Carro Lavagem | lavagem, lava-jato | Sim |
| Carro Gasolina | POSTO, combustível, gasolina, etanol, Shell, BR, Ipiranga | Sim |
| Carro Estacionamento | ESTAPAR, MULTIPARK, estacionamento, parking | Sim |

### Alimentação
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| HiperMercado | EXTRA, CARREFOUR, BIG, ATACADAO, ASSAI, WALMART | Sim |
| Marmitas | marmita, rancho, entrega comida | Sim |
| Restaurantes | restaurante, churrascaria, pizzaria, lanchonete | Sim |
| Ifood + snacks + Padaria | IFOOD, padaria, cafeteria, snack | Sim |
| Mercadão + Bebidas | mercado municipal, bebidas, bar, distribuidora | Sim |

### Saúde
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Drogaria | DROGASIL, DROGARAIA, ULTRAFARMA, PANVEL, farmácia | Sim |

### Pessoal / Vestuário / Beleza
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Corte Cabelo | barbearia, cabelereiro, salão | Sim |
| Compras / Presentes | AMAZON, SHOPEE, MERCADO LIVRE, RENNER, C&A, ZARA | Sim |

### Cartões e Dívidas
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Juros/IOF | JUROS, IOF, ENCARGOS | Sim (na própria fatura) |

### Outros
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Uber - 99 / Estac / ConectCar | UBER, 99APP, CONECTCAR, 99POP | Sim |
| Lançamentos no cartão (final 3878) | tudo que não se encaixa acima | Sim |
| Loterias | CAIXA LOTERIAS, LOTERIA | Sim |
| Outros | qualquer outro lançamento não mapeado | Sim |

### Assinaturas
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| AMAZON PRIME BR - 12/12 | AMAZON PRIME, AMZN | Sim |
| Spotify | SPOTIFY | Sim |
| APPLE COM/BILL Cloud | APPLE, APPLE.COM | Sim |
| Netflix | NETFLIX | Sim |

### Lazer / Viagens
| Item na planilha | Palavras-chave no PDF | Vem do cartão? |
|------------------|----------------------|----------------|
| Lazer / Viagem | BOOKING, AIRBNB, hotel, passagem, cinema, show, parque | Sim |

### Investimentos / Poupança
| Item na planilha | De onde vem | Vem do cartão? |
|------------------|-------------|----------------|
| Fundo de Reserva | Transferência / aplicação | Não |

---

## Categorias da Planilha

| Categoria | Exemplos de estabelecimentos / lançamentos |
|-----------|---------------------------------------------|
| Alimentação | Supermercados, açougues, hortifrúti, IFood, restaurantes, lanchonetes |
| Assinaturas | Netflix, Spotify, Disney+, Amazon Prime, YouTube Premium, softwares |
| Cartões e Dívidas | Pagamento de fatura, parcelas de empréstimo, financiamentos |
| Casa / Moradia | Aluguel, condomínio, energia, água, gás, internet, materiais de construção |
| Descontos Legais | Descontos em folha, benefícios, abatimentos |
| Filhos / Educação / Cuidados | Escola, cursos, livros, material escolar, babá, pediatra |
| Investimentos / Poupança | Aportes em investimentos, previdência, poupança |
| Lazer / Viagens | Cinema, shows, hotéis, passagens, passeios, parques |
| Outros | Tudo que não se encaixa nas demais categorias |
| Pessoal / Vestuário / Beleza | Roupas, calçados, salão, barbearia, farmácia (higiene) |
| Receitas | Salário, freelances, rendimentos, estornos de receita |
| Saúde | Plano de saúde, consultas, exames, farmácia (medicamentos) |
| Veículo / Transporte | Combustível, Uber, pedágio, IPVA, seguro do carro, manutenção |
| Estornos | Devoluções e estornos de compras (valor negativo — entrada na planilha) |

---

## Dicas de Extração

- **Compras parceladas**: registre apenas o valor da parcela atual; some ao item correspondente (ex: Porto Seguro parcela 3/6 → some em "Carro Seguro").
- **Compras internacionais**: use o valor em BRL já convertido que aparece na fatura.
- **IOF e encargos**: some em "Juros/IOF" na categoria Cartões e Dívidas.
- **Estornos**: aparecem com sinal positivo na fatura — subtraia do item original ou registre em Estornos. Se houver qualquer estorno na fatura, calcule e apresente a **soma total dos estornos** (impacto real para o Luiz, já aplicando 50% do cartão 3878) ao final do resumo de reconciliação.
- **Lançamentos não identificados**: some em "Lançamentos no cartão (final 3878)" até conseguir identificar.
- **Esocial**: lançamento de folha, não vem do cartão.

---

## Checklist de Preenchimento Mensal

- [ ] Baixar PDF do Mastercard Black
- [ ] Baixar PDF do Visa Infinite
- [ ] Nomear arquivos no padrão `AAAA-MM-NOME_CARTAO.pdf`
- [ ] Mover para a pasta `gastos/AAAA-MM/`
- [ ] Extrair lançamentos do Mastercard Black para a planilha
- [ ] Extrair lançamentos do Visa Infinite para a planilha
- [ ] Categorizar cada lançamento
- [ ] Verificar se soma dos lançamentos bate com o total da fatura
- [ ] Marcar parcelas futuras para controle

---

## Histórico de Aprendizado

Use esta seção para anotar particularidades descobertas em cada fatura processada.

---

### 2026-04 — Visa Infinite (total R$ 1.344,23 | venc. 01/05/2026)

#### Padrões observados nesta fatura
- Fatura com dois cartões: **final 2587** (titular) = R$ 588,93 e **final 7396** (adicional) = R$ 755,30
- IFD* = iFood; 99Food * = delivery pelo app 99; Kee* = entrega direta do restaurante
- RDSAUDE ONLINE = RD Saúde (mesma rede Droga Raia) → categoria Saúde / Drogaria
- CAASP LAPA = Caixa de Assistência dos Advogados de SP → categoria Saúde / Drogaria
- Shopee*MeuLar = produtos para casa no Shopee → categoria Pessoal / Vestuário / Beleza
- ESKALA = loja de roupas → categoria Pessoal / Vestuário / Beleza
- CL PEDIATRICA LUCI = vacina / consulta pediatra → Filhos / Educação / Cuidados → Gastos Isabela*
- 99* (só dois caracteres) = corrida 99 → Veículo / Transporte

#### Lançamentos mapeados — cartão final 2587 (titular)

| Data | Estabelecimento | Parcela | Valor R$ | Item na planilha |
|------|----------------|---------|----------|------------------|
| 13/01 | CL PEDIATRICA LUCI | 03/05 | 220,80 | Filhos/Educação → Gastos Isabela* |
| 04/03 | RIACHUELO 366 | 02/02 | 35,00 | Pessoal/Vestuário → Compras/Presentes |
| 04/03 | RIACHUELO 366 (estorno) | — | -0,01 | Estornos |
| 25/03 | IFD*iFood | — | 59,09 | Alimentação → Ifood + snacks + Padaria |
| 29/03 | IFD*iFood | — | 12,90 | Alimentação → Ifood + snacks + Padaria |
| 08/04 | 99Food *Pizza Hut - Lap | — | 57,65 | Alimentação → Ifood + snacks + Padaria |
| 14/04 | DROGASIL1008 | 01/03 | 28,81 | Saúde → Drogaria |
| 14/04 | IFD*ARCOS DOURADOS COM | — | 59,09 | Alimentação → Ifood + snacks + Padaria |
| 14/04 | CAASP LAPA | 01/02 | 35,36 | Saúde → Drogaria |
| 17/04 | ESKALA 106 | — | 40,00 | Pessoal/Vestuário → Compras/Presentes |
| 22/04 | 99Food *Esfiha Imigrant | — | 40,24 | Alimentação → Ifood + snacks + Padaria |
| **Total** | | | **588,93** | |

#### Lançamentos mapeados — cartão final 7396 (adicional)

| Data | Estabelecimento | Parcela | Valor R$ | Item na planilha |
|------|----------------|---------|----------|------------------|
| 27/01 | PG *DROGARAIA | 03/03 | 71,33 | Saúde → Drogaria |
| 28/01 | RDSAUDE ONLINE | 03/03 | 119,89 | Saúde → Drogaria |
| 20/03 | SHOPEE *MRILOJA | 02/03 | 130,34 | Pessoal/Vestuário → Compras/Presentes |
| 20/03 | SHOPEE *MRILOJA (estorno) | — | -0,02 | Estornos |
| 24/03 | Shopee*SHOPEE*MeuLar | — | 66,00 | Pessoal/Vestuário → Compras/Presentes |
| 25/03 | Zara Brasil LTDA | 01/03 | 124,34 | Pessoal/Vestuário → Compras/Presentes |
| 31/03 | RENNER | 01/03 | 49,97 | Pessoal/Vestuário → Compras/Presentes |
| 31/03 | Kee*EMPORIO DAS PIZZ | — | 58,39 | Alimentação → Restaurantes |
| 10/04 | 99Food *O Burgus - Per | — | 65,00 | Alimentação → Restaurantes |
| 17/04 | 99Food *Pizza Hut - Vil | — | 63,09 | Alimentação → Restaurantes |
| 20/04 | 99* | — | 6,97 | Veículo/Transporte → Uber - 99 / Estac / ConectCar |
| **Total** | | | **755,30** | |

#### Resumo por item da planilha — Visa Infinite 2026-04

| Categoria | Item na planilha | Valor R$ |
|-----------|-----------------|----------|
| Alimentação | Ifood + snacks + Padaria | 415,45 |
| Alimentação | Restaurantes | 0,00 |
| Saúde | Drogaria | 255,39 |
| Filhos/Educação/Cuidados | Gastos Isabela* | 220,80 |
| Filhos/Educação/Cuidados | Gastos Babá Isabela * | 0,00 |
| Pessoal/Vestuário/Beleza | Compras / Presentes | 445,65 |
| Veículo / Transporte | Uber - 99 / Estac / ConectCar | 6,97 |
| Estornos | Estornos | -0,03 |
| **TOTAL** | | **1.344,23** |

#### Parcelas a cobrar nas próximas faturas (não entram no total acima)

| Estabelecimento | Próximas parcelas | Valor/parcela R$ |
|----------------|-------------------|------------------|
| CL PEDIATRICA LUCI | 04/05 e 05/05 | 220,80 |
| SHOPEE *MRILOJA | 03/03 | 130,34 |
| Zara Brasil LTDA | 02/03 e 03/03 | 124,34 |
| RENNER | 02/03 e 03/03 | 49,97 |
| DROGASIL1008 | 02/03 e 03/03 | 28,81 |
| CAASP LAPA | 02/02 | 35,36 |

---

### 2026-04 — Mastercard Black (total planilha R$ 7.016,77 | venc. 15/05/2026)

#### Cartões processados

| Cartão | Total fatura | Observação |
|--------|-------------|------------|
| Final 0539 (Luiz titular) | R$ 3.420,70 | Principal |
| Final 1929 (Luiz adicional) | R$ 614,66 | Adicional |
| Final 3878 (Paloma) | R$ 3.033,21 → 50% = R$ 1.516,61 | 50% apenas |

#### Resumo por item da planilha — Mastercard Black 2026-04

| Categoria | Item na planilha | Valor R$ |
|-----------|-----------------|----------|
| Lazer / Viagens | Lazer / Viagem (incl. Belém 3878 50%) | 1.349,15 |
| Alimentação | Ifood + snacks + Padaria | 403,21 |
| Alimentação | Restaurantes | 1.047,07 |
| Alimentação | HiperMercado | 16,93 |
| Saúde | Drogaria | 275,36 |
| Filhos/Educação/Cuidados | Gastos Isabela* (Wellhub) | 319,99 |
| Pessoal/Vestuário/Beleza | Corte Cabelo | 40,00 |
| Pessoal/Vestuário/Beleza | Compras / Presentes | 562,33 |
| Casa / Moradia | Casa Manutenção (TELHA NORTE) | 104,50 |
| Veículo / Transporte | Uber-99/Estac/ConectCar | 417,29 |
| Veículo / Transporte | Carro Gasolina | 510,84 |
| Veículo / Transporte | Outros veículo peças | 160,61 |
| Assinaturas | Assinaturas (Spotify + Apple) | 58,70 |
| Outros | Outros | 422,52 |
| Estornos | Estornos | -188,34 |
| **Subtotal Luiz + Belém 3878** | | **5.500,16** |
| Lançamentos no cartão (final 3878) | Paloma demais (50%) | 1.516,61 |
| **TOTAL planilha** | | **7.016,77** |

#### Padrões observados
- Viagem Belém 07/03–14/03: todos os lançamentos de Belém → Lazer/Viagens (ambos os cartões)
- WELLHUB LTDA = Gympass/academia → Gastos Isabela* (plano dela)
- ASSOCIACAO ATLETICA ≤ R$250 = almoço AABB (restaurante presencial)
- FUKUYA KANEMOTO = posto de gasolina (mesmo que banco categorize como veículos)
- Cartão 3878 (Paloma) → seção separada, 50% apenas

---

### 2026-04 — Extrato Conta Corrente

#### Resumo por item da planilha — Extrato Abril 2026

| Categoria | Item na planilha | Valor R$ |
|-----------|-----------------|----------|
| Casa / Moradia | Condomínio | 1.069,81 |
| Casa / Moradia | IPTU | 418,87 |
| Casa / Moradia | Luz | 382,32 |
| Casa / Moradia | Conta Internet + TV | 99,90 |
| Casa / Moradia | Conta Celular | 64,00 |
| Casa / Moradia | Casa Faxina semanal (5×R$220) | 1.100,00 |
| Filhos/Educação/Cuidados | Gastos Babá Isabela * (líquido 50%) | 1.072,61 |
| Filhos/Educação/Cuidados | Gastos Meninos | 210,00 |
| Cartões e Dívidas | Juros / IOF | 42,79 |
| **TOTAL mapeado** | | **6.508,54** |

#### Padrões observados
- Babá paga via PIX ANA VIT: valor integral, Paloma manda 50% de volta no mesmo dia → lançar líquido
- eSocial babá via PIX QRS RECEITA FED: valor integral, Paloma paga 50% → lançar líquido em Gastos Babá Isabela Esocial *
- Provisão 13º/férias babá: PIX TRANSF PALOMA -248,45 mensal → Paloma reembolsa 50% → lançar R$124,23 em Gastos Babá Isabela Esocial *
- **Regra geral Esocial:** todos os encargos trabalhistas da babá são divididos 50% com Paloma
- Financiamento Apt Lapa: PIX TRANSF PALOMA -1.219,50 mensal (30/útil do mês)
- Carro IPVA/Licenciamento: PIX TRANSF PALOMA -390,77 (anual, via Paloma)
- Porto Seguro auto: parcela R$434,73 total, Paloma paga 50% → lançar **R$217,37** na planilha
- Faxina = todos os PIX PALOMA de R$220,00 exatos (5 ocorrências em abril)
- PIX TRANSF Sonia = gastos com os meninos (pode ser positivo se troco/estorno)
- DA ELETROPAULO = Luz / Enel SP (mesma empresa)
- PIX TRANSF MARIO P = tratamento Luiz Guilherme (Bradesco Saúde reembolsa) → ignorar
- PIX PALOMA valores positivos (entrada) = reembolsos → não lançar como despesa
- PAY ASSOC = mensalidade AABB clube, parcelas → criar item AABB na planilha
- Ainda a confirmar: PIX PALOMA -390,77 (15/04, não identificado)

---

*Atualizado em: maio/2026*
