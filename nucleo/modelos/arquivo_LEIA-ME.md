# Arquivo Morto e Histórico de Longo Prazo (_arquivo/)

Esta pasta é o repositório de **arquivo morto e histórico de ciclos** da Central de Inteligência.

## 🎯 Por que esta pasta existe?
Os modelos de IA operam com mais velocidade, precisão e menor custo de tokens quando o contexto ativo é mantido enxuto.
Esta pasta implementa o princípio nativo de **Decaimento de Memória (Memory Pruning)**:
1. **Contexto Ativo Limpo:** Apenas o que é vivo e relevante para os próximos 14 dias permanece na raiz (`00_CURRENT_STATE.md`).
2. **Decaimento Temporal:** Sprints, ciclos operacionais, logs e tarefas de projetos fechados há mais de 14 dias saem dos arquivos de estado vivo e são arquivados aqui, organizados em subpastas cronológicas no formato `_arquivo/YYYY-MM/` (exemplo: `_arquivo/2026-10/`).
3. **Consulta Sob Demanda:** Os arquivos aqui não são lidos automaticamente na rotina diária padrão ("Bom dia"). A IA só os carrega na memória quando você solicitar explicitamente uma retrospectiva, resgate de contexto ou auditoria histórica.

## 📂 Como Usar
- Durante a rotina de "Boa Noite / Fim de Expediente" (habilidade `rotina-diaria`), a IA realiza a triagem e transfere itens concluídos com mais de 14 dias para `_arquivo/YYYY-MM/`.
- Se você precisar consultar tarefas ou decisões de meses anteriores, basta pedir: *"Consulte o histórico em `_arquivo/`..."*.
