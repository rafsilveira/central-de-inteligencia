---
name: rotina-diaria
description: Protocolo de Bom dia e Boa noite da Central de Inteligência. Use quando o usuário abrir o dia com "Bom dia" ou fechar com "Boa noite" ou "Fim de expediente". Mantém o estado da Central em dia entre uma sessão e outra.
---

# Rotina diária da Central (Bom dia e Boa noite)

A Central só lembra do que está escrito nos arquivos. O Bom dia lê o que foi deixado e o Boa noite escreve o que aconteceu.
Siga os passos na ordem, sem pular. No Windows, o Python se chama `python`; no Mac e no Linux, `python3`.

Esta conversa é a **mestre**: ela decide, despacha e confere; o trabalho grande roda fora dela (ver "A conversa mestre",
nas regras do núcleo). Por isso ela abre vazia todo dia e é limpa no fim do dia — o que ela precisa lembrar fica escrito.

## Bom dia

1. Se existir `00_SESSAO_MESTRE.md` na raiz, **leia-o primeiro**. É o bilhete que a conversa de ontem deixou: o que está
   rodando, o que ficou na mão e o que espera o dono. Se não existir, não tem problema: o Boa noite de hoje cria.
2. Leia o `00_CURRENT_STATE.md` inteiro. Ele é a verdade sobre como a empresa e a infraestrutura estão agora.
3. Leia as regras da casa, no topo do `00_MASTER_GUIDELINE.md`.
4. Se existir `00_RETOMADA.md` na raiz, leia. É um bilhete deixado no meio de um trabalho (ver a habilidade `virar-contexto`).
5. Rode `git log -5 --format='%h %ad %s' --date=short` para ver o que mudou nas últimas sessões.
6. Rode `python nucleo/atualizar.py --verificar`. Ele confere no máximo uma vez por semana e só escreve algo quando há
   versão nova. Se escrever, inclua uma linha no resumo. Não atualize sem o dono pedir.
7. Quando esse passo tiver escrito algo (ou seja, uma vez por semana), rode também
   `python nucleo/ferramentas/mede_tokens.py` e diga em **uma linha** onde o uso de tokens foi na semana. Ele só lê.
8. Responda com um resumo curto: o estado em poucas linhas, o que ficou em voo no bilhete, o que mudou desde a última
   sessão, as pendências que dependem do dono e a pergunta "O que faremos hoje?".

Não comece nenhuma tarefa antes da resposta do dono. Tarefa com mais de uns cinco comandos não roda aqui: abra uma
conversa nova (ou um agente, se o plano do dono tiver) com instrução curta e peça o resultado em no máximo 15 linhas.

## Boa noite

1. **Atualize o `00_CURRENT_STATE.md`** só com o que mudou de verdade hoje: decisões, ferramentas ligadas ou desligadas,
   números medidos. Separe o que foi medido do que é estimativa. Atualize a data no rodapé.
2. **Higiene da memória (teto de 200 linhas no `00_CURRENT_STATE.md`):**
   - Se o estado passar de 200 linhas, mova registros **fechados** há mais de 14 dias para
     `01 — Memória e Contexto/Historico_Sprints.md`. Mova ciclos e tarefas encerrados para `_arquivo/AAAA-MM/`, usando o mês
     do encerramento.
   - **Mover, nunca apagar.** O que sai do estado vai palavra por palavra. Um resumo perde o caminho de volta, o ID e o
     comando que alguém vai procurar na hora do problema.
   - **O que está no ar fica.** Qualquer que seja a idade, continuam no estado o que ainda roda (como parar, como desfazer,
     IDs e caminhos de produção) e as pendências abertas. O prazo de 14 dias vale só para o que foi **fechado**.
   - **Confira antes do commit:**
     `python nucleo/guardrails/validador_base.py --conferir-enxugamento HEAD --skip-network`. Todo caminho, script e ID que
     estava no estado no último commit tem de existir em algum arquivo da Central.
3. **Registre no histórico do `00_MASTER_GUIDELINE.md`** uma entrada no formato do próprio arquivo: data, agente, ação
   (CRIOU, ATUALIZOU), o quê, arquivos e impacto. Não apague entradas antigas.
4. **Reescreva o bilhete `00_SESSAO_MESTRE.md`.** Se ele não existir, copie `nucleo/modelos/00_SESSAO_MESTRE.md` e
   preencha. Troque a seção "Em voo" inteira pelo que vale agora: o que está rodando neste instante, o que ficou na mão e
   em que passo parou, as decisões de hoje com as palavras do dono, o que espera o sim dele, o que não fazer e número
   medido que ainda não está em outro arquivo. Teto de 80 linhas: o que saiu de lá já está no estado ou no histórico.
5. **Releia os combinados do dia** e confira, um por um, que cada um está escrito em algum arquivo: o que vale para
   sempre nas regras da casa do `00_MASTER_GUIDELINE.md`, o que é estado no `00_CURRENT_STATE.md`, o que é de agora no
   bilhete. O que estiver só na conversa, escreva agora — a conversa vai ser limpa.
6. **Faça o commit** adicionando os arquivos alterados **pelo nome**. Nunca use `git add .` ou `git add -A`, porque outro
   agente pode estar trabalhando na mesma pasta. Mensagem: `Rotina de fim de dia — DD/MM/AAAA`.
7. **Cópia de segurança:** rode `python nucleo/atualizar.py --conferir-copia`.
   - Se ele terminar sem aviso (código 0), rode `git push origin`.
   - Se disser que não há cópia configurada, diga que ficou salvo só neste computador.
   - Se disser **PARE**, não envie. Explique ao dono o motivo que o script deu.
   - Nunca envie para o remote `semente`. Ele é a origem pública da Central e só recebe.
8. Responda: "Sessão salva. Até amanhã!", com uma linha sobre o que fica pendente para o próximo Bom dia, e avise que a
   conversa pode ser limpa agora (no Claude Code, `/clear`). Amanhã a mestre abre vazia e lê o bilhete. Não limpe antes
   de terminar os passos 1 a 7.

## Regras

- Não invente estado. Se não sabe se algo mudou, confira antes de escrever.
- Nunca grave senha, token ou chave em arquivo versionado. Credenciais ficam só em
  `06 — Scripts e Automações/Tokens e Configs/.env`.
