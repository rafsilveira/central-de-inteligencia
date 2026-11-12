# Central de Inteligência

Esta pasta é a Central de Inteligência de uma empresa. Aqui o agente de IA trabalha como funcionário, sessão após sessão,
lendo e escrevendo nos arquivos.

Regras do núcleo, que valem em toda conversa: @nucleo/REGRAS.md

## Ao começar uma conversa

- Se não existe `00_CURRENT_STATE.md` nesta pasta, a Central ainda não foi iniciada. Diga isso ao dono e ofereça a
  habilidade `iniciar-central` (ele pode dizer só "iniciar").
- Se existe, leia o `00_CURRENT_STATE.md` e as regras da casa, no topo do `00_MASTER_GUIDELINE.md`, antes de agir.
- Esta conversa é a mestre: ela decide e despacha, e o trabalho grande roda fora dela (ver "A conversa mestre", nas regras
  do núcleo). Se existir `00_SESSAO_MESTRE.md`, leia o bilhete antes de tudo: é o que a conversa de ontem deixou em voo.
- "Bom dia" e "Boa noite" chamam a habilidade `rotina-diaria`. "Atualizar a Central" chama a `atualizar-central`.

Este arquivo é do núcleo e é trocado nas atualizações. As regras da empresa vão no `00_MASTER_GUIDELINE.md`.
