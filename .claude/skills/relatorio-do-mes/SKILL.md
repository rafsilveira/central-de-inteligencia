---
name: relatorio-do-mes
description: Monta o relatório do mês a partir das planilhas de vendas, contatos e anúncios em 02 — Dados Brutos, com um número por bloco, comparação com o mês anterior, origem das vendas, custo por venda e "o que mudou e por quê" sem inventar causa. Use quando o usuário pedir "faz o relatório de setembro", "fecha o mês", "como foi o mês?", "de onde vieram as vendas?" ou "quanto custou cada venda?".
---

# Relatório do mês

A medição não faz nada sozinha: ela olha cada bloco da máquina de vendas e mostra qual está funcionando e qual está quebrado. A regra do curso gratuito "Fábrica que Vende" (hebeld2c.com/curso/) é **um número por bloco**. Este relatório é isso, todo mês, no mesmo formato, para dar para comparar.

## Entrada

As planilhas de `02 — Dados Brutos/`: vendas (data, projeto ou produto, valor, desconto, origem), contatos (data, origem, etapa, motivo de perda) e anúncios (gasto e resultado por período). Veja também `01 — Memória e Contexto/` (custos, preço, política de desconto), `03 — Relatórios Mensais/` (mês anterior) e `00_CURRENT_STATE.md`.

## O que o relatório traz

1. **Um número por bloco**, igual ao diagnóstico:
   - marketing: contatos novos no mês e custo por contato;
   - atendimento: tempo até a primeira resposta;
   - vendas: taxa de fechamento e desconto médio;
   - pós-venda: recompra e indicação;
   - preço e margem: lucro real por venda.
2. **Comparação com o mês anterior**, número a número, com a diferença.
3. **De onde veio cada venda** (origem): quantas vendas e quanto faturou cada origem.
4. **Custo por venda**, quando houver gasto com anúncio ou evento: gasto ÷ vendas atribuídas. Compare com o lucro por venda: se o custo por venda passa do lucro, cada venda dá prejuízo.
5. **O que mudou e por quê.** Separe em duas listas:
   - **Medido**: o que está nos números (a taxa caiu de X para Y).
   - **Hipótese**: possível causa, marcada como hipótese e com o que checar para confirmar.
6. **O que não pôde ser calculado** e o que registrar a partir de agora.

## Passo a passo

1. **Descubra o mês.** Se o usuário disser "setembro", use o ano mais recente nos dados. Confira que há planilha daquele mês; se não houver, diga isso e pare.
2. **Se já existir relatório daquele mês** em `03 — Relatórios Mensais/`, diga ao usuário. Leia o existente, refaça os cálculos dos dados brutos e aponte qualquer diferença. **Não sobrescreva.**
3. **Calcule com os dados brutos.** Total de vendas, faturamento, ticket médio, desconto médio, vendas e faturamento por origem, contatos por origem, taxa de fechamento. Confira os totais duas vezes.
4. **Compare com o mês anterior** (planilha anterior ou relatório anterior). Se não houver mês anterior, diga que a comparação fica para o mês que vem.
5. **Custo por venda:** use o gasto registrado. Se o gasto for rateado ou estimado, diga. Venda sem origem registrada não entra em nenhum canal: conte à parte.
6. **Escreva "o que mudou e por quê"** com a regra das duas listas. Atenção: se houve anúncio rodando junto com conteúdo orgânico, o alcance sobe por causa do anúncio. Não atribua o resultado ao canal errado.
7. **Liste o que falta** (origem em branco, tempo de resposta sem registro, recompra sem dado).
8. **Mostre o relatório ao usuário e espere o OK.** Só então grave em `03 — Relatórios Mensais/AAAA-MM.md` (por exemplo `2026-09.md`).

## Formato do arquivo

```
# Relatório de [mês/ano]
## Resumo (3 linhas)
## Um número por bloco (tabela: bloco, número, mês anterior, diferença, medido/estimado/não medido)
## Origem das vendas (tabela)
## Custo por venda
## O que mudou e por quê (Medido / Hipótese)
## Não foi possível calcular e o que registrar
```

## O que NUNCA fazer

- **Nunca invente número ou causa.** Sem dado, escreva "não medido". Hipótese sempre rotulada.
- Nunca grave sem o OK do usuário, nem sobrescreva relatório existente.
- Nunca decida pelo dono o que mudar. Sugira; ele decide.
- Nunca coloque nome, telefone ou endereço de cliente. Use só o código.
- Nunca misture dado de um mês com o de outro sem avisar.
