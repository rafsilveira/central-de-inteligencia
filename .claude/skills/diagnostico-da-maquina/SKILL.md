---
name: diagnostico-da-maquina
description: Acha o bloco quebrado da máquina de vendas (marketing, atendimento, vendas, pós-venda, preço e margem, medição) com um número por bloco. Use quando o usuário pedir "qual bloco da minha máquina de vendas está quebrado?", "por que minhas vendas caíram?", "onde está o problema?", "faz o diagnóstico da empresa", "devo aumentar o anúncio?" ou parecido. Lê a Central primeiro e só pergunta o que faltar.
---

# Diagnóstico da máquina de vendas

Este é o método da Aula 1 do curso gratuito "Fábrica que Vende" (hebeld2c.com/curso/): dividir para conquistar. Quando a venda cai, quase todo mundo mexe no anúncio. Muitas vezes o problema nem estava ali. Em vez de procurar no todo, olhe bloco por bloco, cada um com o seu número, e ache o que está quebrado.

## Os blocos e o número de cada um

O cliente anda por quatro blocos: marketing, atendimento, vendas e pós-venda. Em volta ficam o preço e a medição.

| Bloco | O número |
|---|---|
| Marketing | contatos novos por mês e o custo de cada um |
| Atendimento | tempo até a primeira resposta |
| Vendas | taxa de fechamento (de cada 10 orçamentos, quantos fecham) e desconto médio |
| Pós-venda | recompra e indicação (quantos clientes compram de novo ou indicam) |
| Preço e margem | lucro real por venda |

A medição não tem número próprio: é ela que produz os outros. Se o dono não sabe o número de um bloco, esse já é o primeiro achado.

**Ligação entre os vizinhos:**
- Marketing manda gente para o atendimento. Mais contato do que o time atende faz o contato esfriar.
- Atendimento entrega para a venda um cliente entendido. Atendimento ruim entrega só um pedido de preço, e a venda vira briga de desconto.
- Venda promete, pós-venda cobra. Promessa não cumprida mata a recompra.
- Preço é o chão: se está errado, todos os blocos ficam apertados.

## Passo a passo

1. **Leia a Central primeiro:** `00_CURRENT_STATE.md`, `01 — Memória e Contexto/`, `02 — Dados Brutos/` (planilhas de vendas e contatos), `03 — Relatórios Mensais/` e `05 — Vendas e CRM/`. Procure cada número da tabela. Anote de onde veio cada um (arquivo e linha ou coluna) e se é **medido** (está nos dados) ou **estimado** (alguém disse, sem registro).
2. **Calcule o que dá para calcular** com os dados brutos. Taxa de fechamento = vendas ÷ orçamentos. Desconto médio vem da coluna de desconto. Lucro por venda: pela conta da habilidade `preco-certo`, se a Central tiver os custos. Lucro com desconto: lucro = novo preço − custo total − (imposto + comissão + cartão) × novo preço. Não subtraia o desconto inteiro do lucro, porque imposto e taxas também caem. Se um relatório da Central já traz esse número, confira com essa fórmula antes de apontar divergência.
3. **Pergunte só o que faltar, uma pergunta por vez.** Comece pelo bloco do caminho do cliente mais perto do começo. Se o dono não souber, não insista: marque "não medido".
4. **Compare com o período anterior** quando houver dado. Um número sozinho diz pouco; o que mudou aponta o bloco.
5. **Ache o bloco mais quebrado.** É o que piorou mais ou o que está pior em relação ao vizinho (por exemplo, contato subindo e resposta demorando). Diga o porquê com os números. Se a causa for hipótese, escreva "hipótese".
6. **Proponha as 3 primeiras ações**, no bloco quebrado e pequenas o bastante para começar esta semana.
7. **Ofereça gravar** o diagnóstico em `03 — Relatórios Mensais/` (nome `Diagnostico_AAAA-MM-DD.md`) e espere o OK.

## Formato da resposta

Seja rápido e concreto. Uma tela.

1. **O bloco mais quebrado** em uma frase, com o número que prova.
2. **Tabela:** bloco, número, mês anterior (se houver), medido ou estimado ou não medido, fonte.
3. **Por que esse bloco:** 2 a 4 linhas, ligando com os vizinhos.
4. **As 3 primeiras ações.**
5. **O que não foi medido** e o que registrar para medir no mês que vem. Número que falta é um achado, não uma falha sua.
6. A pergunta: "Posso gravar este diagnóstico em `03 — Relatórios Mensais/`?"

## O que NUNCA fazer

- **Nunca invente número.** Sem dado, escreva "não medido". Não arredonde de cabeça nem use média de mercado no lugar do número da empresa.
- Não misture medido com estimado na mesma coluna sem marcar.
- Não decida pelo dono. A IA aponta o bloco e sugere ações; quem escolhe é ele.
- Não recomende mais anúncio antes de olhar vendas e atendimento. IA e anúncio num bloco quebrado só fazem ele quebrar mais rápido.
- Não grave arquivo sem o OK do usuário.
- Não ponha nome nem telefone de cliente na resposta nem no arquivo. Use o código do cliente.
