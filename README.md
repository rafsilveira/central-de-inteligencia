# Central de Inteligência

A Central de Inteligência é uma pasta que faz o Claude trabalhar como um funcionário da sua empresa. Ele lembra o que
aconteceu nas sessões anteriores, segue as regras que você definiu e já vem com habilidades de vendas e marketing.
Ela foi feita para quem fabrica ou importa e quer vender direto ao cliente final.

É gratuita e é a mesma base que a [Hebel D2C](https://hebeld2c.com) usa no dia a dia. O curso gratuito
[Fábrica que Vende](https://hebeld2c.com/curso/) ensina a usar, aula por aula.

## O que você precisa

- O **Claude Code**, no aplicativo do Claude para computador (aba Code) ou no terminal.
- O **git** e o **Python 3** instalados. Se faltar algum, a Central avisa e explica como instalar.

## Instalar

1. Escolha a pasta do computador onde a Central vai morar e rode:

   ```
   git clone https://github.com/rafsilveira/central-de-inteligencia.git "Minha Central"
   ```

   Se preferir, peça ao Claude: *"instale a Central de Inteligência de https://github.com/rafsilveira/central-de-inteligencia"*.
2. Abra a pasta no Claude Code e diga **iniciar**. A Central te entrevista sobre a empresa, uma pergunta por vez. Depois
   ela mostra o que entendeu e só grava depois do seu sim. Leva uns 20 minutos.

## Atualizar

Diga **atualizar a Central**. Ela mostra o que mudou na versão nova e pede o seu sim antes de trocar qualquer coisa.
No Bom dia, uma vez por semana, ela avisa quando sai versão nova. Ela nunca atualiza sozinha.

A atualização troca só os arquivos do núcleo. Os seus arquivos não são lidos nem escritos. Se você tiver mexido num
arquivo do núcleo, a sua versão é guardada em `_arquivo/` antes da troca. Para voltar à versão anterior, diga
*"volte a Central para a versão anterior"*.

Quem usa git também pode atualizar com `python nucleo/atualizar.py` (no Mac e no Linux, `python3`).

## O que é seu e o que é da Hebel

| Da Hebel (o núcleo, que se atualiza) | Seu (a atualização não toca) |
|---|---|
| `nucleo/`: regras, guias, moldes, guardrail e atualizador | `00_CURRENT_STATE.md`: o estado da empresa |
| `.claude/skills/`: as habilidades da lista abaixo | `00_MASTER_GUIDELINE.md`: as regras da casa e o histórico |
| `.claude/agents/`: a equipe da agência de marca | as pastas numeradas (`01 — Memória e Contexto` e as outras) |
| `CLAUDE.md`, `README.md`, `NOVIDADES.md`, `VERSAO`, `LICENSE`, `TERCEIROS.md` | `marca/`, `_arquivo/` e o `.env` com as suas chaves |
| | as suas habilidades, em `.claude/skills/casa-<nome>/` |

Para mudar o jeito da Central trabalhar, escreva a regra no `00_MASTER_GUIDELINE.md`. Não edite o núcleo.

## Guarde uma cópia, mas privada

A sua Central guarda dados da sua empresa. **Não faça fork público deste repositório.** Se quiser uma cópia de segurança
no GitHub, crie um repositório **privado** seu e peça à Central para usá-lo. Antes de enviar, o Boa noite confere se o
repositório é privado e se recusa a enviar para um público.

## O que vem dentro

As habilidades são acionadas quando o pedido combina com elas. Aqui a IA pensa com você usando os arquivos da Central.

Uma habilidade para cada bloco da máquina de vendas do curso:

- **diagnostico-da-maquina** (Aula 1): acha o bloco quebrado, com um número por bloco, e dá as 3 primeiras ações.
- **preco-certo** (Aula 2): faz a conta do preço com custo, fixo, pró-labore e porcentagens, e confere o lucro.
- **orcamento-e-objecoes** (Aula 3): monta o orçamento em cinco etapas e as respostas para "tá caro", "vou pensar" e
  "consegui mais barato". Mostra quanto o desconto custa no lucro.
- **pauta-do-cliente** (Aula 5): transforma as conversas com clientes nos 10 próximos assuntos de conteúdo.
- **relatorio-do-mes** (Medição): monta o relatório do mês, com um número por bloco, a origem das vendas e o custo por venda.
- **offers**: monta a oferta de produto físico, com bônus que respondem objeção real, garantia por escrito, urgência real
  e a conta do lucro por desconto. Origem: [marketingskills](https://github.com/coreyhaines31/marketingskills), de Corey
  Haines, licença MIT.
- **seo-audit**: audita o SEO do site: o que impede o Google de achar e mostrar as páginas, as páginas de produto, o
  contato no celular e o Perfil da Empresa no Google quando há loja ou showroom. Entrega o plano de ação em ordem de
  gravidade. Origem: [marketingskills](https://github.com/coreyhaines31/marketingskills), de Corey Haines, licença MIT.

E uma equipe inteira:

- **agencia-de-marca**: entrevista você como um designer sênior faria e passa o briefing para cinco agentes. Entrega o logo
  em vetor e em PNG, as variantes, a paleta com o contraste calculado, as fontes e o `Manual_de_Marca.pdf`. O passo a passo
  está em `nucleo/guias/Agencia_de_Marca.md`.

E as de rotina:

- **iniciar-central**: a entrevista que liga a Central.
- **rotina-diaria**: o Bom dia e o Boa noite, que mantêm o estado da Central em dia.
- **virar-contexto**: salva tudo em arquivo antes de compactar uma conversa longa.
- **atualizar-central**: traz a versão nova do núcleo sem mexer nos seus arquivos.

Guias: `nucleo/guias/Pratica_3_Meta_e_Google_Ads.md` explica como conectar o Meta Ads e o Google Ads sem cartão e com tudo
pausado.

## Licença

MIT. Pode usar, mudar e distribuir. O que mudou em cada versão está em `NOVIDADES.md`.
