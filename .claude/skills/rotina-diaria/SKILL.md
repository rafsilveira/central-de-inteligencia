---
name: rotina-diaria
description: Protocolo de Bom dia e Boa noite da Central de Inteligência. Use quando o usuário abrir o dia com "Bom dia" ou fechar com "Boa noite" ou "Fim de expediente". Mantém o estado da Central em dia entre uma sessão e outra.
---

# Rotina diária da Central (Bom dia e Boa noite)

A Central só lembra do que está escrito nos arquivos. O Bom dia lê o que foi deixado e o Boa noite escreve o que aconteceu.
Siga os passos na ordem, sem pular. No Windows, o Python se chama `python`; no Mac e no Linux, `python3`.

## Bom dia

1. Leia o `00_CURRENT_STATE.md` inteiro. Ele é a verdade sobre como a empresa e a infraestrutura estão agora.
2. Leia as regras da casa, no topo do `00_MASTER_GUIDELINE.md`.
3. Se existir `00_RETOMADA.md` na raiz, leia. É um bilhete deixado no meio de um trabalho (ver a habilidade `virar-contexto`).
4. Rode `git log -5 --format='%h %ad %s' --date=short` para ver o que mudou nas últimas sessões.
5. Rode `python nucleo/atualizar.py --verificar`. Ele confere no máximo uma vez por semana e só escreve algo quando há
   versão nova. Se escrever, inclua uma linha no resumo. Não atualize sem o dono pedir.
6. Responda com um resumo curto: o estado em poucas linhas, o que mudou desde a última sessão, as pendências que dependem do
   dono e a pergunta "O que faremos hoje?".

Não comece nenhuma tarefa antes da resposta do dono.

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
4. **Faça o commit** adicionando os arquivos alterados **pelo nome**. Nunca use `git add .` ou `git add -A`, porque outro
   agente pode estar trabalhando na mesma pasta. Mensagem: `Rotina de fim de dia — DD/MM/AAAA`.
5. **Cópia de segurança:** rode `python nucleo/atualizar.py --conferir-copia`.
   - Se ele terminar sem aviso (código 0), rode `git push origin`.
   - Se disser que não há cópia configurada, diga que ficou salvo só neste computador.
   - Se disser **PARE**, não envie. Explique ao dono o motivo que o script deu.
   - Nunca envie para o remote `semente`. Ele é a origem pública da Central e só recebe.
6. Responda: "Sessão salva. Até amanhã!", com uma linha sobre o que fica pendente para o próximo Bom dia.

## Regras

- Não invente estado. Se não sabe se algo mudou, confira antes de escrever.
- Nunca grave senha, token ou chave em arquivo versionado. Credenciais ficam só em
  `06 — Scripts e Automações/Tokens e Configs/.env`.
