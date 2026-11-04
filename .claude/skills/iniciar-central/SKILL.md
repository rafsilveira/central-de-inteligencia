---
name: iniciar-central
description: Liga a Central de Inteligência numa pasta nova. Entrevista o dono sobre a empresa e cria os arquivos dele (estado, regras da casa, pastas). Use quando o dono disser "iniciar", "começar a Central", "configurar a Central", ou quando a pasta não tiver 00_CURRENT_STATE.md.
---

# Iniciar a Central

A Central acabou de chegar ao computador do dono e ainda está vazia. A primeira tarefa não é nenhuma ação de negócio:
é **entrevistar o dono** para entender quem ele é, o que a empresa faz e como você deve se comportar. Só depois disso a
Central liga.

## 0. Antes da entrevista

1. Se já existe `00_CURRENT_STATE.md` na raiz, a Central já foi iniciada. Diga isso e pergunte se ele quer refazer a
   entrevista. Se ele quiser, você **acrescenta** e corrige. Não apague nada do que existe.
2. Rode `python nucleo/atualizar.py --preparar` (no Mac e no Linux, `python3`). Ele liga o git e deixa a semente só para
   receber atualizações. Se ele disser que falta o git ou o Python, explique ao dono como instalar e espere.
3. Se o resultado avisar que a cópia de segurança é **pública**, pare e explique ao dono: os dados da empresa ficariam
   abertos. Ele precisa tornar o repositório privado antes de continuar.

## 1. Regras da entrevista

1. **Uma pergunta por vez.** Nunca despeje uma lista de perguntas. Converse.
2. **Adapte-se às respostas.** Se uma resposta já responde a próxima pergunta, pule. Se abrir um assunto relevante,
   aprofunde antes de seguir.
3. **Não invente nada.** O que o dono ainda não sabe fica como `[EM DEFINIÇÃO]`. Um campo vazio e sincero vale mais que
   um preenchido para parecer completo.
4. **Mostre antes de escrever.** No fim, resuma o que entendeu, pergunte "posso registrar assim?" e só então crie os arquivos.

## 2. Roteiro (nesta ordem, com naturalidade)

**Bloco 1 — Identidade**
- Nome da empresa, o que ela vende ou faz, em que ramo atua.
- Quem é o dono: nome, e-mail, papel. Tem sócios?
- A empresa já tem CNPJ ou ainda é ideia em validação?

**Bloco 2 — Estágio e modelo de negócio**
- Já fatura? Há quanto tempo? Quantas pessoas trabalham nela?
- Como o dinheiro entra: venda direta ao consumidor (D2C), para empresas (B2B), varejo ou distribuidor, assinatura, serviço.
- Ticket médio e ciclo de venda: compra rápida ou decisão de semanas?

**Bloco 3 — Como vende e se comunica hoje**
- Onde estão os clientes hoje: redes sociais, indicação, tráfego pago, loja física?
- Tem CRM, planilha ou processo de vendas? Qual?
- Tem automação rodando (n8n, Zapier, Make)?
- Tem site ou landing page? Qual endereço?

**Bloco 4 — Prioridade**
- Se pudesse resolver **uma coisa** com ajuda da IA nas próximas semanas, qual seria? Isso vira o foco inicial.

**Bloco 5 — Regras e limites (não pule)**
- Que dados a IA nunca deve tocar ou expor?
- Existe **mais de um negócio ou marca** do dono? Cada negócio tem a sua Central, e esta nunca mistura dados, arquivos ou
  decisões de outro, nem para ajudar. Registre como regra explícita: é a proteção mais importante do sistema.
- Que ações a IA **nunca** deve tomar sozinha (postar, mandar mensagem a cliente, mexer em anúncio ativo)?

## 3. Depois do "pode registrar"

Crie só o que ainda não existe. **Nunca sobrescreva** um arquivo do dono.

1. `00_CURRENT_STATE.md`: copie `nucleo/modelos/00_CURRENT_STATE.md` e preencha com os Blocos 1 a 4, sem inventar.
2. `00_MASTER_GUIDELINE.md`: copie `nucleo/modelos/00_MASTER_GUIDELINE.md`, preencha as **regras da casa** com o Bloco 5
   e a primeira entrada do histórico com a data de hoje.
3. **Pastas da empresa.** Proponha as pastas numeradas e crie só depois do sim. Cada uma ganha um `LEIA-ME.md` de uma
   linha dizendo o que guarda. O ponto de partida que serve à maioria das empresas que fabricam ou importam é este:
   - `01 — Memória e Contexto` (empresa, produto, cliente, decisões). Dentro dela, copie `nucleo/modelos/Historico_Sprints.md`.
   - `02 — Dados Brutos` (planilhas e exportações, sem nome nem telefone de cliente)
   - `03 — Relatórios Mensais`
   - `04 — Campanhas e Criativos`
   - `05 — Vendas e CRM`
   - `06 — Scripts e Automações`. Dentro dela, crie `Tokens e Configs/` e copie para lá o `nucleo/modelos/.env.example`.
     O `.env` de verdade só nasce quando o dono for conectar uma ferramenta.

   Tire a pasta que não fizer sentido e acrescente a que a prioridade pedir (ex.: `08 — Licitações`). Registre a lista
   final na seção 4 do `00_CURRENT_STATE.md`.
4. `_arquivo/LEIA-ME.md`: copie de `nucleo/modelos/arquivo_LEIA-ME.md`.
5. Faça o commit adicionando cada arquivo pelo nome (`git add -- <arquivo>`), com a mensagem
   `Central iniciada — DD/MM/AAAA`.
6. Pergunte se ele quer uma **cópia de segurança** no GitHub. Se quiser, ele cria um repositório **privado** e te passa o
   endereço. Você roda `git remote add origin <endereço>` e depois `python nucleo/atualizar.py --conferir-copia`. Só
   envie se a conferência passar.
7. Feche com o resumo do que ficou registrado e a pergunta **"O que fazemos primeiro?"**, sugerindo a prioridade do Bloco 4.
   Se ele não souber por onde começar, sugira a `diagnostico-da-maquina`. Conte também que a agência de marca está aqui
   ("quero o manual da minha marca"). Ela precisa do Claude Code e do Chrome ou Chromium, e avisa antes de instalar o que faltar.
