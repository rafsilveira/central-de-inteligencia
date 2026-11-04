---
name: virar-contexto
description: Vira o contexto da conversa sem perder nada no meio de um trabalho. Salva tudo em arquivo, escreve um bilhete de retomada, pede a compactação e retoma lendo os arquivos. Use quando o contexto estiver cheio ("o contexto tá acabando", "vira o contexto", "compacta sem perder nada") ou antes de começar uma tarefa longa.
---

# Virar o contexto sem perder nada

Quando a conversa enche, a compactação automática resume por conta própria e perde detalhe: número medido, decisão recém-tomada, o que estava acontecendo naquele instante. A solução é inverter a ordem: primeiro escrever em arquivo, depois compactar. O que está no disco não depende do resumo.

## 1. Rode o Boa noite completo

Siga a habilidade `rotina-diaria`, parte Boa noite: estado, changelog e commit. Mesmo que não seja fim do dia.

## 2. Escreva o bilhete `00_RETOMADA.md` na raiz da Central

Escreva para alguém que não viu a conversa. Seções:

- **O que está rodando neste instante:** processos, agentes, automações ligadas hoje. Se nada, diga "nada".
- **O que estava na mão:** a tarefa em andamento, em que passo parou e qual era o próximo passo.
- **Decisões de hoje, com as palavras do usuário:** cite o que ele disse quando a decisão foi dele.
- **Perguntas em aberto:** o que ainda falta o usuário responder.
- **O que não fazer:** erros já cometidos ou caminhos já descartados nesta sessão.
- **Números medidos que ainda não estão em nenhum outro arquivo.**

Faça commit do bilhete.

## 3. Peça a compactação e retome

Diga ao usuário que o contexto pode ser compactado agora (no Claude Code, com `/compact`). Na volta, rode o Bom dia da `rotina-diaria`, que lê o bilhete, e continue do passo em que parou.

Apague o `00_RETOMADA.md` quando o assunto dele estiver fechado, registrando no changelog o que foi concluído. Um bilhete velho faz a próxima sessão retomar uma tarefa que já acabou.
