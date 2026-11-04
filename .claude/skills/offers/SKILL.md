---
name: offers
description: "Monta ou melhora a oferta de uma fábrica ou importadora que vende direto ao cliente final: bônus que fecham objeção real, garantia por escrito, urgência real, conta do lucro por cenário de desconto e pendências para o dono decidir. Use quando o usuário pedir 'monta uma oferta', 'oferta para a linha X', 'que bônus eu dou?', 'como faço uma garantia?', 'promoção sem destruir a margem', 'minha oferta não converte' ou parecido. Também cobre, em inglês no corpo, o método geral de oferta: equação de valor, bônus, garantia, escassez, nome e pagamento."
metadata:
  version: 1.0.2
---
# Oferta para produto físico (fábrica ou importadora que vende direto)

Esta seção vale primeiro. O resto do arquivo é o método geral de oferta, em inglês, e serve de apoio. Adapte: o cliente compra uma coisa que ele vai ver, tocar e usar por anos, e o risco dele é pagar caro por algo que não é o que parecia.

## A oferta tem cinco partes

1. **O produto e o preço.** O preço vem da conta da habilidade `preco-certo` (custo, fixo, pró-labore, porcentagens do preço, lucro). Não invente preço nem custo: se faltar, vira pendência.
2. **Bônus que fecham objeção real.** Cada bônus responde a um medo ou a uma dúvida que o cliente de fato tem, e que aparece nas conversas e nos motivos de perda da Central. Exemplos: **revisão** depois da entrega (resolve "e se desregular?"), **guia de comparação** (resolve "como sei que é melhor que o outro orçamento?"), **prioridade de agenda** (resolve "e o prazo?"). Bônus que não responde a nenhuma objeção é enfeite. Dê preferência a bônus de custo baixo e valor alto para o cliente. Calcule o custo de cada bônus: ele entra no custo da venda.
3. **Garantia por escrito.** Diga o que cobre, por quanto tempo, o que o cliente faz para acionar e o que a empresa faz. Só prometa o que a fábrica já cumpre hoje e consegue pagar. Garantia que a empresa não cumpre mata a recompra.
4. **Urgência real.** Só o que existe: data de entrega, vaga na agenda de montagem, condição de pagamento com validade, preço que muda numa data marcada. Nunca relógio falso nem "últimas unidades" sem estoque.
5. **O que a empresa nunca faz.** Desconto fora da política da Central. Se a Central tem `Politica_de_Desconto.md`, siga.

## A conta do lucro por cenário

Desconto sai inteiro do lucro, e bônus e parcelamento têm custo. Para cada cenário da oferta, calcule o lucro com a conta do preço da Central:

lucro = preço da oferta − custo total (com o custo dos bônus) − (imposto + comissão + cartão) × preço da oferta

Mostre uma tabela com, no mínimo: preço cheio; a oferta proposta; 5% de desconto; 10% de desconto. Colunas: preço, custo, lucro em reais, lucro em % do preço, e quanto do lucro some em relação ao preço cheio. Se algum número faltar, escreva "pendente" na célula e não complete com palpite. Se a oferta deixar o lucro abaixo do que a Central define como mínimo, avise e proponha a versão sem desconto (bônus, prazo, condição de pagamento).

## Passo a passo

1. **Leia a Central:** produto e preço, política de desconto, quem compra, por que compra, como decide, garantia e prazo já praticados, motivos de perda em `05 — Vendas e CRM/` e `02 — Dados Brutos/`.
2. **Liste as objeções reais** da linha de produto (de onde saiu cada uma).
3. **Monte a oferta** nas cinco partes, em português simples, com o nome da oferta.
4. **Faça a tabela do lucro por cenário.**
5. **Liste as pendências para o dono decidir** (custo que faltou, taxa do cartão parcelado, garantia que ele aceita dar, data limite, quantas vagas na agenda).
6. **Entregue para revisão.** Nada vai ao ar, a anúncio ou a cliente sem o OK do dono.

## O que NUNCA fazer

- Nunca invente custo, prazo, garantia, estoque ou vaga de agenda.
- Nunca crie urgência falsa.
- Nunca ofereça desconto fora da política nem sem mostrar quanto do lucro some.
- Nunca decida a oferta pelo dono: monte, mostre os números e deixe as escolhas marcadas.
- Nunca grave nem publique sem o OK.

## Formato da resposta

1. O nome e a ideia da oferta em duas linhas.
2. As cinco partes.
3. A tabela do lucro por cenário.
4. As pendências para o dono decidir.

---

# Método geral de oferta (referência, em inglês)

# Offer Design

You are an expert in offer construction. Your goal is to help the user build offers that move — not by writing better copy on a worse offer, but by improving the offer itself.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

---

## Core Philosophy

**The offer is the thing, not the page.** Better copy on a weak offer compounds slowly. A stronger offer with average copy converts immediately. Most "we need better copy" requests are actually "we need a better offer" requests in disguise.

This skill exists because the rest of the repo handles the *expression* of an offer — `preco-certo` sets the price, `orcamento-e-objecoes` carries the offer into the sale. None of them ask the deeper question: **is the offer underneath any of that actually good?**

### When this skill matters

You sell:
- **Services** — consulting, freelance, agency retainers, productized services
- **Courses** — async, cohort-based, live
- **Coaching** — 1:1, group, mastermind
- **Info products** — guides, swipe files, templates, communities
- **High-ticket B2B** — $5K+ ACV with a sales conversation
- **Direct-response** — e-com promo offers, infomercial-style, paid-traffic-to-VSL

### When tier structure does more of the work

You sell:
- **Self-serve SaaS** with tiered subscriptions — the levers are mostly tier structure, value metric, and packaging; offer construction (bonuses, guarantees) is secondary
- **Marketplaces** — the offer is structural, not constructed

Skim this skill in those cases for the value equation framing, then focus on tier structure instead.

---

## The Value Equation

The single most useful frame for offer design. Originally from Alex Hormozi's *$100M Offers* — internalized broadly across direct-response and creator-economy training since.

```
              Dream Outcome  ×  Perceived Likelihood of Achievement
  Value  =  ─────────────────────────────────────────────────────────
              Time Delay     ×   Effort & Sacrifice
```

You move the four levers like this:

| Lever | What it means | How to increase value |
|-------|---------------|-----------------------|
| **Dream outcome** ↑ | What the customer actually wants | Connect to the bigger goal behind the surface ask. Specify and name it. |
| **Perceived likelihood** ↑ | Do they believe they'll get it | Proof (case studies, named customers, data), guarantees, methodology specificity |
| **Time delay** ↓ | How long until result | Faster onboarding, faster first win, faster end-to-end timeline |
| **Effort & sacrifice** ↓ | What it costs them in time/work/risk besides money | Done-for-you, simpler process, fewer decisions, lower learning curve |

**Implication for offer construction**: most "lower the price" requests are actually "raise the numerator or lower the denominator" requests. Price is the comparison, not the value.

**For the full framework, examples, and how to diagnose which lever is broken:** see [references/value-equation.md](references/value-equation.md)

---

## The Anatomy of a Complete Offer

A complete offer has six components. Skip any one and conversion suffers.

| # | Component | Question it answers |
|---|-----------|---------------------|
| 1 | **Core deliverable** | What do they get? |
| 2 | **Bonus stack** | What else do they get that makes the core feel undervalued? |
| 3 | **Guarantee** | What happens if it doesn't work? |
| 4 | **Scarcity / urgency** | Why now, not later? |
| 5 | **Name** | What is this thing called? |
| 6 | **Price + payment structure** | What do they pay and how? |

Most weak offers fail on bonuses (none), guarantees (none or wrong type), or scarcity (none, or fake). Most aggressive-to-the-point-of-cringe offers fail on guarantee (over-promising) or scarcity (fake countdown timers).

**For the full anatomy with worked examples:** see [references/offer-anatomy.md](references/offer-anatomy.md)

---

## Reference Library

| Reference | When to read |
|-----------|--------------|
| [value-equation.md](references/value-equation.md) | Diagnosing which lever is broken on a stuck offer |
| [offer-anatomy.md](references/offer-anatomy.md) | Building a complete offer from scratch |
| [guarantee-design.md](references/guarantee-design.md) | Picking the right type of guarantee for your business model |
| [bonus-stacking.md](references/bonus-stacking.md) | Adding bonuses that raise perceived value without devaluing the core |
| [scarcity-urgency.md](references/scarcity-urgency.md) | Creating *real* scarcity (and avoiding the fake patterns that destroy trust) |
| [offer-formats.md](references/offer-formats.md) | Format playbooks by business type — service, course, coaching, info product, SaaS lead magnet, agency retainer, high-ticket B2B |
| [saas-offers.md](references/saas-offers.md) | SaaS specifically — the discount trap (why discounting to acquire backfires) + four SaaS worked offers (AudienceTap, SaberSim, Teachable, Kit) |
| [examples.md](references/examples.md) | Anonymized worked examples — before/after for each business type |

---

## The Diagnostic Loop

When the user says "my offer isn't converting" or "I want to improve my offer":

1. **Identify the business type** — service, course, coaching, info product, SaaS, agency, B2B. The right playbook is type-specific.
2. **State the current offer in plain language** — name, price, what they get, guarantee, deadline. Write it down even if it lives in scattered places now.
3. **Run the value equation** — score each of the four levers 1–10. The lowest is the binding constraint.
4. **Audit the anatomy** — which of the six components is missing or weak?
5. **Pick one lever to fix this iteration** — don't rebuild everything. The biggest lever is usually the one currently scoring lowest.
6. **Draft the changed component** — new bonus, new guarantee, new scarcity, new name, new payment plan
7. **Project the lift, honestly** — most single-component changes deliver 10–40% conversion lift. Anyone promising 5x is selling something. Two consecutive iterations on different levers can stack to 2–3x.

---

## When NOT to Use Offer-Design Tactics

Some offer patterns work but cost more than they're worth:

- **Manipulative scarcity** — fake countdown timers, "only 3 spots left" lies. Short-term lift, long-term trust collapse. Don't.
- **Over-promising guarantees** — "double your revenue or refund + $1,000." Refund risk eats margin; the few cases that fail nuke your reputation publicly.
- **Bonus inflation** — stacking $50K of "bonuses" on a $497 product so it "feels like a steal." Sophisticated buyers see this. Treat bonuses as additive, not exaggerated.
- **Course-bro aesthetic on a serious product** — Gold logos, "secret method," fake urgency. Pattern-matches to scam. Wrong room.
- **Discounting to acquire** — discount-*askers* churn at ~2× the rate of full-price customers, and a coupon anchors the product as cheap. Discount only for upgrades/cross-sells (rewarding existing customers) or real seasonal windows — never to win a new one. Raise value with an offer instead. See [saas-offers.md](references/saas-offers.md).

The repo voice: opinionated, but honest. Building offers well doesn't mean building offers loud.

---

## Banned Vocabulary

When drafting offer language (sales pages, emails, headlines), avoid:

- **"Game-changing," "revolutionary," "disruptive," "next-level," "10x"** — pattern-matches to AI slop / course-bro
- **"Secret," "hidden," "what they don't want you to know"** — clickbait
- **"Limited time" with no actual time limit** — lying
- **"Worth $X" or "$Y value" with no comparable** — inflation
- **"100% guaranteed" without specifying conditions** — legally and brand-wise risky

Use specific numbers, named customers, concrete outcomes, real timelines. Specificity beats superlatives.

---

## Related Skills

- **preco-certo** — the price math that every offer scenario uses
- **orcamento-e-objecoes** — the quote steps, objection answers and discount rules
- **pauta-do-cliente** — where the real customer objections come from
