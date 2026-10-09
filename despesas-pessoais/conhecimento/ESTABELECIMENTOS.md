# Classificação de estabelecimentos

Aplicar as decisões específicas abaixo antes do catálogo histórico. Comparar descritores completos e contexto; preferir correspondência mais específica. Uma regra de categoria não muda o cartão de origem nem autoriza rateio adicional. O modelo de linhas é [planilha.json](C:/github/personal/despesas-pessoais/modelos/planilha.json).

As hipóteses e decisões limitadas ao ciclo de agosto não são fatos permanentes. Estabelecimentos desconhecidos continuam em Outros; pedir apenas o que mudar a classificação ou o valor pessoal.

## Revisão de setembro/ciclo outubro — 09/10/2026

Decisões por ID em `periodos/2026-09/auditoria/dados/revisao_usuario.json`. Respostas “não sei” resolvem a pergunta de reconhecimento, mas não identificam o gasto; manter em Outros sem repetir a pergunta de rotina.

| Descritor | Decisão vigente | Escopo e confiança |
| --- | --- | --- |
| `WEI MOTORS` | Concessionária; R$ 140,55 correspondem à troca da lanterna do carro. Manutenção do carro em Outros básicos (46), pois não há linha própria no modelo. Não usar Carro Lavagem ou Gasolina. | Identidade da concessionária confirmada; finalidade limitada a MASTERCARD-021 deste ciclo. |
| `HAVAN OSASCO` | Compras para casa → Compras / Presentes (51), 01/02 de R$ 135,96. Não inferir reparo ou obra. | Compra confirmada em MASTERCARD-023 e suas parcelas seguintes; não generalizar a qualquer compra na Havan. |
| `CheiaDeManiasBarE` | Restaurantes (53), R$ 206,11. | Restaurante confirmado; padrão do descritor, respeitando cartão e contexto. |
| `SAPORE SA` | Almoço no zoológico → Lazer / Viagem (64), R$ 55,00. | Confirmação específica de VISA-009; não generalizar a todo SAPORE. |
| `Sala15`, `AnaluIntimates`, `CuorDiCrema` | Não reconhecidos por Luiz; manter em Outros (66). | Resposta deste ciclo, sem identificação confirmada. |
| `AOB UTENSILIOS DOMEST` | Duas compras de R$ 23,98 e R$ 7,98 no Visa de Luiz 2587; manter em Outros (66). | Luiz condicionou a hipótese de gasto para casa a ser cartão de Paloma; condição não atendida. Titular/cartão esclarecidos com a fatura. |
| `DESC ANTECIPA PARCELAS` | Crédito de R$ 31,48 em Outros (66); origem não reconhecida por Luiz. | MASTERCARD-010: não vincular ao Itaú Shop nem reclassificar por coincidência. |

Amazon Digital BR, R$ 34,90, MASTERCARD-040: Luiz confirmou em 09/10/2026 que foi filme e pediu Lazer/Viagem (64). Confirmação específica de setembro/ciclo outubro; não generalizar para toda cobrança Amazon nem alterar retroativamente a hipótese do ciclo anterior.

## Respostas dos 22 itens de cartão — 10/09/2026


Origem: respostas de Luiz aos 22 itens de revisão das faturas em `2026-08 (faturas 2026-09)`. As regras específicas abaixo têm precedência sobre padrões genéricos, como AMAZON e AMAZON PRIME. Comparar sem distinção de espaços, acentos e caixa, preservando a descrição original no relatório.

**Escopo e certeza:** `Padrão` registra a associação informada pelo usuário para futuras ocorrências desse descritor; verificar novamente se houver evidência de produto/serviço diferente. `2026-08 (faturas 2026-09)` limita a classificação provisória a este ciclo. Informações dadas com “acho” não foram promovidas a fatos confirmados. Valores monetários continuam sendo lidos da fatura; não reutilizar valores ou periodicidade como novas cobranças automáticas.

| Contém no PDF | Categoria | Item na planilha | Status | Escopo | Descrição / orientação |
| --- | --- | --- | --- | --- | --- |
| `MICROSOFT*STORE` | Assinaturas | OneDrive — anual | Confirmada | Padrão | Assinatura anual do OneDrive; R$ 599,00 neste ciclo. Registrar integralmente na fatura atual, sem dividir por 12 nem repetir mensalmente. Microsoft Store também pode vender outros produtos: validar se o serviço mudar. |
| `OPENAI*CHATGPT SUBSCR` | Assinaturas | OpenAI — mensal | Confirmada | Padrão | Assinatura mensal OpenAI; manter as duas cobranças efetivas do ciclo, sem presumir duplicidade ou inventar preço mensal fixo. |
| `PE DE MANGA` | Alimentação | Restaurantes | Confirmada | Padrão | Restaurante. |
| `CasaDeCarnes` | Alimentação | HiperMercado | Confirmada | Padrão | Luiz pediu explicitamente HiperMercado. |
| `JIM.COM* MAGALI DA` | Filhos / Educação / Cuidados | Gastos Babá Isabela * | Confirmada | Padrão | Serviço que gerencia a nova babá. É serviço de gestão, não salário nem eSocial. Manter a parcela atual; não foi informado rateio ou reembolso específico desse serviço. |
| `LEVI S-SHOP.MORUMB` | Pessoal / Vestuário / Beleza | Compras / Presentes | Confirmada | Padrão | Roupas; o prefixo cobre a descrição truncada e sua variante terminada em MORUMBI. |
| `Drogaria_SP drogar` | Saúde | Drogaria | Confirmada | Padrão | Drogaria, confirmado pelo usuário. |
| `RESERVA PAULISTA ADMIN` | Lazer / Viagens | Lazer / Viagem | Confirmada | Padrão | Zoológico de São Paulo; aplicar às três ocorrências deste ciclo, respeitando o cartão de origem. |
| `DRUGSTORE LIBERDADE` | Saúde | Drogaria | Confirmada | Padrão | Drogaria. |
| `ZOOSPECOMMERCEPARQ` | Lazer / Viagens | Lazer / Viagem | Confirmada | Padrão | Zoológico de São Paulo. |
| `ACORES PARKS` | Outros | Reembolso empresa | Confirmada | Padrão | Estacionamento reembolsado pela empresa; cobre ACORES PARKS ES e ACORES PARKS-CT. Registrar na categoria de reembolso sem inventar um crédito na fatura. |
| `VERBO DIVINO RESTAURAN` | Alimentação | Restaurantes | Confirmada | Padrão | Restaurante do trabalho, mesmo tratamento de PRATUS VERBO DIVINO. |
| `MP*DAVIDELIRA` | Outros | Outros | Não identificado | Padrão | Usuário não reconheceu; pesquisa em 10/09/2026 não encontrou associação confiável com um estabelecimento. Manter em Outros, com identificação pendente. |
| `AGUA NA BOCA DOCEIRA L` | Alimentação | Ifood + snacks + Padaria | Confirmada | Padrão | Doceria / snack. |
| `OSASCO MARGINAL` | Alimentação | Ifood + snacks + Padaria | Provisória | 2026-08 (faturas 2026-09) | Luiz acha que foi sorvete no McDonald's. Aplicar provisoriamente neste ciclo; confirmar em ocorrências futuras. |
| `GOBR COMERCIO` | Outros | Outros | Não identificado | Padrão | Usuário não reconheceu. Manter em Outros, sem inferir atividade comercial pelo nome. |
| `Amazon Digital BR` | Lazer / Viagens | Lazer / Viagem | Provisória | 2026-08 (faturas 2026-09) | Luiz acha que foi compra de filme. Não tratar como assinatura por padrão; confirmar em ocorrências futuras. |
| `KIDSTOK` | Pessoal / Vestuário / Beleza | Compras / Presentes | Confirmada | Padrão | Presente, conforme o usuário. |
| `ROSSINI EVENTOS` | Alimentação | Ifood + snacks + Padaria | Confirmada | Padrão | Sorvete; não classificar como evento/lazer pelo nome. |
| `CdbAlberico2De` | Alimentação | Ifood + snacks + Padaria | Confirmada | Padrão | Padaria. |
| `ESTRADA ITAPECERICA` | Outros | Outros | Não identificado | Padrão | Usuário não reconheceu. Manter em Outros. |
| `Amazon Prime Aluguel` | Lazer / Viagens | Lazer / Viagem | Confirmada | Padrão | Aluguel de filme; tem precedência sobre a regra genérica AMAZON PRIME de assinatura. |

**Pesquisa de MP*DAVIDELIRA:** foram consultadas variações do descritor literal e o contexto de Arapiraca indicado no PDF. Os resultados encontrados não comprovaram a identidade do estabelecimento; nenhuma pessoa ou empresa homônima foi vinculada à compra. Permanecem duas cobranças de R$ 20,00 no cartão 3878, total bruto R$ 40,00 e participação de Luiz R$ 20,00.

**Rateios e reembolsos:** aplicar 50% a todos os cartões identificados como de Paloma (3878 e 6553 conhecidos), conforme confirmação geral de 09/10/2026, inclusive AABB. Classificar o serviço de gestão da babá no cartão de Luiz não autoriza automaticamente rateio. Os estacionamentos ACORES passam ao item Reembolso empresa; o relatório preserva os débitos originais, sem criar recebimento.

---


## Catálogo vigente, com inconsistências corrigidas
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
| `STRIKEBAR` | STRIKEBAR | Bar / snack — valor baixo (< R$50) |
| `GABRIELLAFRANCES` | GABRIELLAFRANCES | Lanche / snack |
| `BOLOS` | BOLOSDALAPACOMERCIO | Confeitaria / padaria |
| `PRACAPANAMERICANA` | PRACAPANAMERICANA | Sorvete / snack McDonald's |
| `30220687Adriana` | 30220687Adriana | Churros / comida no clube |
| `CAFECREMECOMERCIO` | CAFECREMECOMERCIO | Snack / cafeteria / padaria |
| `BAFFSSANTACASA` | BAFFSSANTACASA | Comida / snack na lojinha do trabalho |
| `BANCADEFRUTAS` | BANCADEFRUTASMIGUEL | Banca de frutas |
| `FRUTAS` | FRUTAS NASSAI | Banca de frutas / frutaria |

### Alimentação — Restaurantes

> Jantar / almoço presencial em restaurante. Gastos maiores, ocasiões especiais (ex: Coco Bambu, Pecorino).

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `COCO BAMBU` | COCO BAMBU LAPA | Restaurante presencial |
| `BADARO` | BADARO | Restaurante presencial |
| `OUTBACK` | OUTBACKBOURBOUNSP | Restaurante presencial |
| `PECORINO` | PECORINO REST | Restaurante presencial |
| `RESTAURANTE` | RESTAURANTE DO JOSE | Use para estabelecimentos onde foi presencialmente |
| `CHURRASCARIA` | CHURRASCARIA BOI | |

> ⚠️ `99Food *` e `Kee*` = delivery → **Ifood + snacks + Padaria**, mesmo que o nome seja de restaurante.
> ⚠️ Valores **abaixo de R$ 50** em estabelecimentos de bar/lanche sem reserva → **Ifood + snacks + Padaria**, não Restaurantes.
> ⚠️ `ASSOCIACAO ATLETIC` com valor **acima de R$ 250** = mensalidade/outro → **Outros**.

### Alimentação — Trabalho - Restaurantes

| Contém no PDF | Exemplo real | Observação |
| --- | --- | --- |
| `PRATUS VERBO DIVINO` | PRATUS VERBO DIVINO | Almoço no escritório |
| `JOTASIFREITASLTDA` | JOTASIFREITASLTDA | Restaurante / refeicao no trabalho |
| `VERBO DIVINO RESTAURAN` | VERBO DIVINO RESTAURAN | Almoço no trabalho, linha 42 |

### Alimentação — HiperMercado

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `EXTRA` | EXTRA HIPERMERCADO | |
| `CARREFOUR` | CARREFOUR BARRA FUNDA | |
| `ATACADAO` | ATACADAO | |
| `ASSAI` | ASSAI ATACADISTA | |
| `AKKI` | AKKI ATACADISTA | Atacadista japonês / hipermercado |
| `DIABRASILLJ386` | DIABRASILLJ386 | Compra de mercado / supermercado |
| `PAODEACUCAR` | PAODEACUCAR-2408 | Pão de Açúcar (supermercado) |
| `PAO DE ACUCAR` | PAO DE ACUCAR | Pão de Açúcar |
| `WALMART` | WALMART | |
| `BIG` | BIG SUPERMERCADO | |
| `SONDA` | SONDA POMPEIA | Supermercado Sonda |

### Alimentação — Mercadão + Bebidas

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `MERCADO MUNICIPAL` | MERCADO MUNICIPAL SP | |
| `DISTRIBUIDORA` | DISTRIBUIDORA BEBIDAS | |
| `ADEGA` | ADEGA DO VINHO | |
| `ELTON BARROSO DE MELO` | ELTON BARROSO DE MELO | Feira de frutas |
| `EltonBarrosoDe` | EltonBarrosoDe | Feira de frutas (variante abreviada) |
| `JAPONESA PASTEIS` | JAPONESA PASTEIS | Feira de frutas |

### Alimentação — Refeições AABB

| Contém no PDF | Exemplo real | Observação |
| --- | --- | --- |
| `ASSOCIACAO ATLETICA` | ASSOCIACAO ATLETICA B | Restaurante AABB — **somente quando valor ≤ R$ 250** |
| `ASSOCIACAO ATLETIC` | ASSOCIACAO ATLETIC | Restaurante AABB — **somente quando valor ≤ R$ 250** |

Usar a linha 55 (Mercadão + feira + Bebida + rest. AABB) para as refeições de até R$ 250,00. Valor acima de R$ 250,00 continua em Outros até identificar a natureza; não confundir com a mensalidade bancária confirmada.

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
| `PAGUEMENOS` | PAGUEMENOS00209 | Farmácia Pague Menos |
| `CAASP` | CAASP LAPA | Drogaria / Saúde, conforme regra explícita e histórico |

### Pessoal / Vestuário / Beleza — Corte Cabelo

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `C.N.D. LOCACAO` | C.N.D. LOCACAO DE BEN | Cabeleireiro |
| `BARBEARIA` | BARBEARIA CENTRAL | |
| `CABELEREIRO` | CABELEREIRO JOAO | |
| `SALAO` | SALAO DE BELEZA | |
| `PERSONAL HAIR` | PERSONAL HAIR STUDIO L | Salão de beleza / cabelereiro |

### Filhos / Educação / Cuidados — Gastos Babá Isabela *

> Pagamentos da babá da Isabela. Normalmente não aparece no cartão (pago em dinheiro / transferência).

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `BABA` | PAGTO BABA | Pagamento babá se vier no cartão |

### Filhos / Educação / Cuidados — Gastos Isabela *

> Atividades, natação, cursos e demais gastos da Isabela (não babá). Normalmente no cartão da Paloma (3878) — aplicar 50%.

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `WellhubIsabelaPaixao` | WellhubIsabelaPaixao | Wellhub (natação / atividade física da Isabela) — cartão 3878, 50% |
| `WELLHUB LTDA` | WELLHUB LTDA | Plano da Isabela conforme aprendizado de abril; preservar o cartão e aplicar seu rateio uma única vez. |

> Vacinas, consultas médicas e despesas de saúde da Isabela.

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `CL PEDIATRICA` | CL PEDIATRICA LUCI | Vacinas / consultas pediatra |
| `PEDIATRIA` | CLINICA PEDIATRIA | |
| `VACINA` | CLINICA VACINA | |

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
| `AMAZON` | AMAZON.COM.BR | Compras apenas quando identificado varejo. AMAZON/AMZN genérico não identifica assinatura, filme ou aluguel; priorizar descritores específicos e a decisão do ciclo. |
| `AMAZONMKTPLC` | AMAZONMKTPLC*UPTEC | Amazon Marketplace — **Compras/Presentes**, não veículo |
| `ITAUSHOP` | ITAUSHOP | Compra parcelada via Itaú Shop (ex: iPhone 16 / celular) → **Compras/Presentes** |
| `RENNER` | RENNER | |
| `RIACHUELO` | RIACHUELO 366 | |
| `ZARA` | Zara Brasil LTDA | |
| `C&A` | C&A MODA | |
| `ESKALA` | ESKALA 106 | Loja de roupas |
| `HERING` | HERING STORE | |
| `PARATY ESPORTES` | PARATY ESPORTES LTDA | Loja de roupas esportivas |
| `LOCCITANE` | LOCCITANEBR | L'Occitane — cosméticos |
| `SamPedro` | SamPedro | Sapateiro da Lapa / conserto de calcados |
| `EDITORAWMFMARTINSF` | EDITORAWMFMARTINSF | Livro / compra pessoal |

### Pessoal / Vestuário / Beleza — Projetos pessoais

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `GITHUB,INC.` | GITHUB,INC. | Classificar como **Projetos pessoais** |

### Pessoal / Vestuário / Beleza — Compras / Presentes (marketplace casa)

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `Shopee*SHOPEE*MeuLar` | Shopee*SHOPEE*MeuLar | Produtos para casa no Shopee → **Compras / Presentes** |

### Casa / Moradia — Casa Manutenção Apartamento

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `LEROY` | LEROY MERLIN | Materiais de construção |
| `TELHANORTE` | TELHANORTE | |
| `CASAS BAHIA` | CASAS BAHIA | Eletrodomésticos/móveis |
| `TOK&STOK` | TOK&STOK | |
| `MP*ASSTECNICAELE` | MP*ASSTECNICAELE | Conserto da lava e seca → **Casa Manutenção Apartamento** |
| `SAMSUNGNOITAU` | SAMSUNGNOITAU | Lava e seca nova / eletrodoméstico → **Casa Manutenção Apartamento** |

### Veículo / Transporte — Uber - 99 / Estac / ConectCar

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `UBER` | UBER *TRIP | |
| `99*` | 99* | Corrida pelo app 99 (sem "Food") |
| `99APP` | 99APP | |
| `CONECTCAR` | CONECTCAR | Pedágio tag |
| `TagItau *LUIZNETO` | TagItau *LUIZNETO | ConectCar / tag de pedagio |
| `ESTAPAR` | ESTAPAR | Estacionamento |
| `MULTIPARK` | MULTIPARK | Estacionamento |
| `ZUL` | ZUL 1 cartao | App Zona Azul Digital (estacionamento rotativo) |
| `PolyGaragensE` | PolyGaragensE | Estacionamento fixo |
| `Estacionamento` | Estacionamento | Genérico |

> ⚠️ `99Food *` (com "Food") → **Alimentação → Ifood + snacks + Padaria**. Sem "Food" → **Transporte**.

### Veículo / Transporte — Carro Seguro

| Contém no PDF | Exemplo real | Observação |
| --- | --- | --- |
| `PORTO SEGURO` | PORTO SEGURO AUTO | Seguro do carro; usar parcela literal. No cartão 3878, integra a única metade da linha 56. |

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

### Veículo / Transporte — Carro Manutenção e Lavagem

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `H GARD` | H GARD | Manutenção e serviços para carro |

### Turismo e Entretenimento

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `ZIGPAY` | ZIGPAY | Pagamento cashless em eventos/festas (ZIG) |
| `ZIG*` | ZIG*SAO JOAO DE SP | **Lazer / Viagem** — Festival junino / festa junina (ZIG) |
| `PAG*Steam` | PAG*Steam | Jogo / plataforma Steam — **Lazer** |

### Assinaturas

| Contém no PDF | Item na planilha | Exemplo real |
|---------------|-----------------|-------------|
| `AMAZON PRIME` | AMAZON PRIME BR - 12/12 | AMAZON PRIME BR |
| `SPOTIFY` | Spotify | SPOTIFY |
| `APPLE.COM` | APPLE COM/BILL Cloud | APPLE.COM/BILL |
| `APPLE COM` | APPLE COM/BILL Cloud | APPLE COM/BILL |
| `NETFLIX` | Netflix | NETFLIX.COM |
| `DISNEY` | THE WALT DISNEY COMPAN | Disney+ |

### Cartões e Dívidas — Juros/IOF

| Contém no PDF | Exemplo real | Observação |
|---------------|-------------|------------|
| `JUROS` | JUROS ROTATIVO | |
| `IOF` | IOF FINANCIAMENTO | |
| `ENCARGOS` | ENCARGOS FINANCEIROS | |

### Outros

| Contém no PDF | Item na planilha | Exemplo real |
|---------------|-----------------|-------------|
| `SOLUCOGARAGENS` | Reembolso empresa | SOLUCOGARAGENS | Estacionamento reembolsado pela empresa |
| `CAIXA LOTERIAS` | Loterias | CAIXA LOTERIAS |
| `LOTERIA` | Loterias | LOTERIA FEDERAL |

---



## Critérios de uso

- As condições explícitas (como o limite da refeição AABB) fazem parte da regra. Heurísticas de valor baixo, bar, loja genérica ou palavras amplas são indícios, não confirmação universal.
- 99Food/Kee são delivery; ZUL é estacionamento; CAASP é Drogaria; pediatria é Gastos Isabela; Shopee MeuLar é Compras/Presentes; Porto Seguro é seguro. Estes pontos foram corrigidos no catálogo para eliminar destinos contraditórios.
- Os cartões de Paloma preservam estas categorias apenas no detalhamento; no resumo pessoal entram uma única vez na linha 56, com metade do total. A regra vale também para AABB e para o final 6553, conforme confirmação de 09/10/2026. Descritor desconhecido nunca muda o cartão de origem.
- Aprendizado novo: atualizar esta regra existente, com data, confirmação/hipótese e escopo, em vez de acrescentar uma segunda regra conflitante. Originais históricos ficam em `historico/`.

## Pistas complementares preservadas do modelo anterior

Usar quando o estabelecimento ainda não constar no catálogo, verificando o serviço e a linha correspondente. São pistas de identificação, não autorização para aplicar percentuais, criar cobranças recorrentes ou classificar todo PIX genérico.

| Linha / item | Pistas | Limite |
| --- | --- | --- |
| Condomínio (22) | CONDOMINIO, boleto de condomínio | Boleto genérico sozinho não identifica a despesa |
| IPTU (23) | IPTU, Prefeitura, DA PMSP | Confirmar o tributo; prefeitura pode cobrar outros serviços |
| Luz (24) | ENEL, ELETROPAULO, CPFL, LIGHT, CEMIG, energia | Usar conta efetivamente identificada |
| Conta Celular (25) | CLARO, VIVO, TIM, OI, celular | Separar telefonia móvel de internet/TV |
| Internet + TV (26) | NET, CLARO NET, SKY, VIVO FIBRA, internet | PIX AUT CLARO e INT/CLARO já mapeados como internet |
| Manutenção apartamento (27) | materiais, ferragens, manutenção, prestador | Descrição genérica exige contexto do serviço |
| Faxina (28) | faxina, limpeza, diarista | Regras específicas de Paloma e SOS DIA na referência bancária |
| Gastos Meninos (29) | escola, curso, material, livro, uniforme | Confirmar para qual filho quando ambíguo; pediatria da Isabela vai à linha 30 |
| IPVA/licenciamento/multa (34) | DETRAN, IPVA, multa | Não transformar todo PIX de mesmo valor em IPVA |
| Lavagem (36) | lavagem, lava-jato | Separar de conserto da casa |
| Transporte (52) | UBER, 99APP, 99POP, CONECTCAR | 99Food é alimentação; usar regra específica de estacionamento quando existente |
| Lazer/Viagem (64) | BOOKING, AIRBNB, hotel, passagem, cinema, show, parque | Confirmar consumo/viagem; não generalizar aluguel de filme como assinatura |

O histórico também identifica viagem a Belém em 07/03–14/03 no ciclo de 2026: naquela viagem, os gastos da localidade foram para Lazer/Viagem. Essa é uma exceção daquele período, não uma regra para todas as compras futuras em Belém.
