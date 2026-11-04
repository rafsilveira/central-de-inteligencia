---
name: preco-certo
description: Faz a conta do preço de um produto de fábrica ou importadora, com custo variável, parte do fixo, pró-labore, imposto, comissão, cartão e lucro. Use quando o usuário pedir "faz a conta do preço", "quanto devo cobrar?", "meu preço está certo?", "coloco 15% em cima do custo", "qual meu lucro nessa venda?" ou "o concorrente cobra menos". Substitui a habilidade genérica de preços.
---

# O preço certo

Este é o método da Aula 2 do curso gratuito "Fábrica que Vende" (hebeld2c.com/curso/). O preço é o chão da máquina de vendas: se está errado, todos os blocos ficam apertados e ninguém sabe de onde vem o aperto.

## A fórmula

**Preço = (custo variável + parte do fixo e do pró-labore) ÷ (1 − imposto − comissão − cartão − lucro)**

- **Custo variável:** o que só existe se vender. Matéria-prima, peças, embalagem, frete, montagem. Não vendeu, não gastou.
- **Custo fixo:** o que se paga vendendo ou não. Aluguel, salários, sistema, contador, energia.
- **Pró-labore:** o que o dono pagaria a alguém para fazer o trabalho dele. **É custo**, não o que sobra no fim do mês.
- **Imposto, comissão, cartão e lucro:** são porcentagens **do preço**, não do custo.

## As regras da conta

1. **As porcentagens são do preço e são somadas antes de dividir.** Divide-se uma vez só. Nunca uma taxa de cada vez. Nunca "custo + X%".
   - Custo de R$ 1.000, imposto de 10% e cartão de 5%: somando, 1.000 ÷ 0,85 = R$ 1.176,47 e sobram os R$ 1.000. Uma taxa de cada vez dá R$ 1.169,59, e faltam R$ 5,85.
2. **O fixo é dividido pelo que a empresa VENDE por mês, não pela capacidade da fábrica.** Parte do fixo por unidade = (fixo + pró-labore) ÷ unidades vendidas. Vendendo menos, cada unidade carrega mais.
3. **Pró-labore entra no fixo.** Sem ele, a conta esconde o prejuízo do trabalho do dono.
4. **Sempre confira.** Preço − (imposto + comissão + cartão) × preço − custo total tem que dar o lucro pedido. Se não der, a conta está errada. Mostre a conferência linha por linha.

## Passo a passo

1. **Leia a Central:** `01 — Memória e Contexto/` (produto e preço, política de desconto), `00_CURRENT_STATE.md` e `02 — Dados Brutos/`. Procure custo variável **do produto pedido**, custo fixo, pró-labore, unidades vendidas por mês, imposto, comissão, cartão e lucro desejado. Marque cada número como medido ou estimado.
2. **O que não estiver na Central, pergunte.** Uma pergunta por vez, começando pelo custo variável do produto. Se o dono não souber, **não use o custo de outro produto no lugar**. Marque a pendência ("custo variável do [produto]: não informado") e devolva a conta pronta com um espaço para ele preencher, ou uma conta de exemplo claramente rotulada como exemplo.
3. **Monte a conta** em quatro passos: fixo + pró-labore por unidade; custo total; soma das porcentagens e divisor; preço.
4. **Confira** com a tabela: preço, menos imposto, menos comissão e cartão, menos custo total, igual ao lucro. Diga o lucro em reais e em % do preço.
5. **Mostre a sensibilidade**, em uma linha cada: vendendo menos unidades por mês; 5% e 10% de desconto (o custo não cai; refaça a conta com o novo preço: lucro = novo preço − custo total − (imposto + comissão + cartão) × novo preço. Os impostos e taxas também caem com o preço, então não subtraia o desconto inteiro do lucro).
6. **Compare com o mercado só se o dono trouxer o preço do mercado.** Não invente preço de concorrente.

## Quando o usuário faz "custo + 15%"

Mostre o erro com os números dele. Exemplo: custo R$ 13.000, mais 15% = R$ 14.950. Imposto e comissão de 15% do preço levam R$ 2.242. Sobram R$ 12.708 para um custo de R$ 13.000: prejuízo de R$ 292 por venda, com a planilha mostrando "15% de margem". Imposto e comissão saem do preço, não do custo. A conta é de dividir, não de multiplicar.

## Quando o preço dá acima do mercado

Duas saídas honestas: **cortar custo** ou **vender mais com a mesma estrutura** (o fixo se espalha por mais unidades). **Nunca sugerir baixar o preço abaixo da conta.** Isso é quebrar devagar. Liste onde o custo pode ser olhado (custo variável maior, fixo parado), sem decidir pelo dono.

## Formato da resposta

1. Preço calculado (ou "pendente: falta X").
2. A conta em quatro passos, com os números e a fonte de cada um (medido, estimado ou pendente).
3. A conferência em tabela.
4. Sensibilidade em 2 a 3 linhas.
5. Pendências para o dono decidir (taxa do cartão parcelado, comissão de parceiro fora do divisor, lucro desejado).

## O que NUNCA fazer

- **Nunca invente custo, taxa ou unidades vendidas.** Sem o número, pergunte ou marque pendência.
- Nunca calcule porcentagem em cima do custo, nem divida taxa por taxa, nem divida o fixo pela capacidade.
- Nunca decida o lucro desejado nem o preço final pelo dono. Mostre a conta; ele escolhe.
- Nunca baixe o preço abaixo da conta para "fechar com o mercado".
- Não grave nem altere arquivo da Central sem o OK do usuário.
